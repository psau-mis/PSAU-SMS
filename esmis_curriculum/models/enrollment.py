# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISEnrollment(models.Model):
	_inherit = "esmis.enrollment"

	def _default_iso_printout(self):
		iso = self.env["ir.model.data"].search([("model", "=", "esmis.iso.printouts"),
												("name", "=", "esmis_iso_certificate_of_reg")])
		if iso:
			_logger.info(iso[0].res_id)
			iso_id = self.env["esmis.iso.printouts"].search([("id", "=", iso[0].res_id)])
			if iso_id:
				return iso_id[0]
		else:
			return None

	
	iso_printout_id = fields.Many2one("esmis.iso.printouts", default=_default_iso_printout)

	subject_enrolled = fields.One2many("esmis.subject.enrolled", "enrollment_id", "Subject Enrolled")
	curriculum_id = fields.Many2one("esmis.curriculum", domain="[('state', '=', 'Active')]")
	section_id = fields.Many2many("esmis.sections", domain="[('course_id', '=', course_id), ('year_id', '=', school_year_id),'&',('state', '=', 'Active'), ('year', '=', year_level)]")
	total_no_of_student = fields.Integer(related="section_id.total_no_of_student")
	total_units = fields.Integer(compute="_compute_total_units")
	total_subjects = fields.Integer(compute="_compute_total_subjects")
	total_lab_units = fields.Integer(compute="_compute_total_lab_units")
	total_lec_units = fields.Integer(compute="_compute_total_lec_units")

	def print_cor(self):
		for rec in self:
			return self.env.ref('esmis_curriculum.action_certificate_of_registration').report_action(rec)

	def print_bulk_cor(self):
		for rec in self:
			return self.env.ref('esmis_curriculum.action_bulk_certificate_of_registration').report_action(rec)

	@api.depends("subject_enrolled")
	def _compute_total_subjects(self):
		for rec in self:
			rec.total_subjects = len(rec.subject_enrolled)

	@api.depends("subject_enrolled")
	def _compute_total_units(self):
		for rec in self:
			total_units = 0
			if rec.subject_enrolled:
				for subjects in rec.subject_enrolled:
					total_units += subjects.subject_id.subject_id.subject_unit
			rec.total_units = total_units

	@api.depends("subject_enrolled")
	def _compute_total_lab_units(self):
		for rec in self:
			total_units = 0
			if rec.subject_enrolled:
				for subjects in rec.subject_enrolled:
					total_units += subjects.lab_hrs_week.unit
			rec.total_lab_units = total_units

	@api.depends("subject_enrolled")
	def _compute_total_lec_units(self):
		for rec in self:
			total_units = 0
			if rec.subject_enrolled:
				for subjects in rec.subject_enrolled:
					total_units += subjects.lec_hrs_week.unit
			rec.total_lec_units = total_units

	def fetch_from_section(self):
		for rec in self:
			for subjects in rec.section_id.subject_offerings:
				flag = True
				if not rec.subject_enrolled:
					flag = True
				else:
					if subjects.id in rec.subject_enrolled.subject_id.ids:
						flag = False

				if flag:
					vals = {
						"subject_id": subjects.id,
						"enrollment_id": rec.id
					}
					self.env["esmis.subject.enrolled"].create(vals)

	@api.onchange("section_id")
	def _onchange_section_id(self):
		for rec in self:
			for recs in rec.section_id:
				if rec.section_id:
					rec.curriculum_id = recs.curriculum_id.id

class eSMISSubjectOfferings(models.Model):
	_name = "esmis.subject.enrolled"
	_description = "Subject Enrolled"
	_order = "id asc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	enrollment_id = fields.Many2one("esmis.enrollment")
	student_name = fields.Char(related="enrollment_id.student_id.name")
	subject_id = fields.Many2one("esmis.subject.offerings")
	section_id = fields.Many2one("esmis.sections", related="subject_id.section_id")
	units = fields.Integer(related="subject_id.units")
	lec_hrs_week = fields.Many2one('esmis.lec.lab.maintenance', string="Lecture Hrs/Week", related="subject_id.lec_hrs_week_1")
	lab_hrs_week = fields.Many2one('esmis.lec.lab.maintenance', string="Lab Hrs/Week", related="subject_id.lab_hrs_week_1")
	sched_day = fields.Selection([("M", "M"),
								  ("T", "T"),
								  ("W", "W"),
								  ("Th", "Th"),
								  ("F", "F"),
								  ("S", "S"),
								  ("MWF", "MWF"),
								  ("TTh", "Tth"),
								  ("TThS", "TthS"), ], string="Days", related="subject_id.sched_day")
	sched_from = fields.Char("From", related="subject_id.sched_from")
	sched_to = fields.Char("To", related="subject_id.sched_to")
	sched_display = fields.Char("Schedule", compute="_compute_sched_display")
	teacher_id = fields.Many2one("hr.employee", string="Teacher", related="subject_id.teacher_id")
	room_id = fields.Many2one('esmis.room', string="Room", related="subject_id.room_id")


	@api.depends("sched_day", "sched_from", "sched_to")
	def _compute_sched_display(self):
		for rec in self:
			rec.sched_display = "{}:{}-{}".format(rec.sched_day or '',
												  rec.sched_from or '',
												  rec.sched_to or '')
