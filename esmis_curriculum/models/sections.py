# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISSections(models.Model):
	_name = "esmis.sections"
	_description = "Sections"
	_order = "sequence asc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	name = fields.Char("Section")
	department_id = fields.Many2one('esmis.department', "School/College", required=True)
	year_id = fields.Many2one('esmis.school.year', "School Year", required=True, domain="[('state', '=', 'Active')]")
	course_id = fields.Many2one('esmis.course', "Course", required=True,
								domain="[('department_id', '=', department_id)]")
	curriculum_id = fields.Many2one('esmis.curriculum', "Curriculum", required=True,
									domain="[('year_id', '=', year_id), ('course_id', '=', course_id),('state', '=', 'Active')]")
	subject_offerings = fields.One2many("esmis.subject.offerings", "section_id", "Subject Offerings")
	state = fields.Selection([("Draft", "Draft"),
							  ("Active", "Active"),
							  ("Done", "Done"),
							  ("Cancelled", "Cancelled")], default="Draft")
	year = fields.Selection([("1st", "1st Year"),
							 ("2nd", "2nd Year"),
							 ("3rd", "3rd Year"),
							 ("4th", "4th Year"),
							 ("5th", "5th Year"),
							 ("6th", "6th Year"),
							 ("7th", "7th Year"),
							 ("8th", "8th Year"),
							 ("9th", "9th Year"),], required=True)
	semester = fields.Selection([("1st", "1st Semester"), ("2nd", "2nd Semester"),("3rd", "Mid Year")], required=True)
	enrollment_ids = fields.Many2many("esmis.enrollment")
	total_no_of_student = fields.Integer(compute="_compute_total_no_of_student")
	reach_max = fields.Boolean(compute="_compute_reach_max")
	reach_max_description = fields.Char(compute="_compute_reach_max")
	sequence = fields.Integer()

	@api.depends("subject_offerings")
	def _compute_reach_max(self):
		for rec in self:
			reach_max = False
			reach_max_description = ""
			for subjects in rec.subject_offerings:
				if subjects.reach_max:
					reach_max = True
					if not reach_max_description:
						if subjects.subject_id.subject:
							reach_max_description = reach_max_description + ", " + subjects.subject_id.subject
					else:
						reach_max_description = subjects.subject_id.subject

			rec.reach_max = reach_max
			rec.reach_max_description = reach_max_description

	@api.depends("enrollment_ids")
	def _compute_total_no_of_student(self):
		for rec in self:
			ctr = 0
			for enrollment in rec.enrollment_ids:
				for secs in enrollment.section_id:
					if secs.id == rec.id:
						if enrollment.status not in ('complete', 'drop', 'cancelled'):
							ctr += 1

			rec.total_no_of_student = ctr

	def on_active(self):
		for rec in self:
			if rec.state == "Draft":
				rec.state = "Active"

	def on_cancel(self):
		for rec in self:
			if rec.state == "Draft":
				rec.state = "Cancelled"

	def on_done(self):
		for rec in self:
			if rec.state == "Active":
				rec.state = "Done"

	def fetch_from_curriculum(self):
		for rec in self:
			field_key = "rec_{}_{}".format(rec.year, rec.semester)
			for curriculum in rec.curriculum_id[field_key]:
				flag = True
				if not rec.subject_offerings:
					flag = True
				else:
					for subject in rec.subject_offerings:
						if curriculum.subject_id.id == subject.subject_id.id:
							flag = False
							vals = {
								"lec_hrs_week_1": curriculum.lec_hrs_week_1.id,
								"lab_hrs_week_1": curriculum.lab_hrs_week_1.id,
							}
							subject.update(vals)
							break

				if flag:
					vals = {
						"subject_id": curriculum.subject_id.id,
						"section_id": rec.id,
						"lec_hrs_week_1": curriculum.lec_hrs_week_1.id,
						"lab_hrs_week_1": curriculum.lab_hrs_week_1.id,
					}
					self.env["esmis.subject.offerings"].create(vals)



class eSMISSubjectOfferings(models.Model):
	_name = "esmis.subject.offerings"
	_description = "Subject Offerings"
	_order = "id asc"
	_rec_name = "subject_id"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	section_id = fields.Many2one("esmis.sections")
	subject_id = fields.Many2one("esmis.subjects")
	units = fields.Integer(related="subject_id.subject_unit")
	sched_day = fields.Selection([("M", "M"),
								  ("T", "T"),
								  ("W", "W"),
								  ("Th", "Th"),
								  ("F", "F"),
								  ("S", "S"),
								  ("MWF", "MWF"),
								  ("TTh", "Tth"),
								  ("TThS", "TthS"), ], string="Days")
	sched_from = fields.Char("From")
	sched_to = fields.Char("To")
	sched_display = fields.Char("Schedule", compute="_compute_sched_display")
	lec_hrs_week = fields.Integer("Lecture Hrs/Week")
	lab_hrs_week = fields.Integer("Lab Hrs/Week")
	lec_hrs_week_1 = fields.Many2one('esmis.lec.lab.maintenance',string="Lecture Hrs/Week")
	lab_hrs_week_1 = fields.Many2one('esmis.lec.lab.maintenance',string="Lab Hrs/Week")
	teacher_id = fields.Many2one("hr.employee", string="Teacher", domain="[('job_id.name', '=', 'Teacher')]")
	maximum_slots = fields.Integer("Maximum Students")

	lock = fields.Boolean("Lock", default=False)
	enrollment_ids = fields.One2many("esmis.subject.enrolled", "subject_id")
	total_no_of_student = fields.Integer(compute="_compute_total_no_of_student")
	reach_max = fields.Boolean(compute="_compute_reach_max")
	room_id = fields.Many2one('esmis.room', string="Room")

	@api.depends("total_no_of_student", "maximum_slots")
	def _compute_reach_max(self):
		for rec in self:
			reach_max = False
			if rec.maximum_slots == rec.total_no_of_student:
				reach_max = True

			rec.reach_max = reach_max

	@api.depends("enrollment_ids")
	def _compute_total_no_of_student(self):
		for rec in self:
			ctr = 0
			for enrollment in rec.enrollment_ids:
				if enrollment.enrollment_id.status not in ('complete', 'drop', 'cancelled'):
					ctr += 1

			rec.total_no_of_student = ctr

	@api.depends("sched_day", "sched_from", "sched_to")
	def _compute_sched_display(self):
		for rec in self:
			rec.sched_display = "{}:{}-{}".format(rec.sched_day or '',
												  rec.sched_from or '',
												  rec.sched_to or '')