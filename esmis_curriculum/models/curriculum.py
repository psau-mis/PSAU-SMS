# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISCurriculum(models.Model):
	_name = "esmis.curriculum"
	_description = "Curriculum"
	_order = "id desc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	year_sem = ["1st_1st", "1st_2nd", "1st_3rd",
				"2nd_1st", "2nd_2nd", "2nd_3rd",
				"3rd_1st", "3rd_2nd", "3rd_3rd",
				"4th_1st", "4th_2nd", "4th_3rd",
				"5th_1st", "5th_2nd", "5th_3rd",
				"6th_1st", "6th_2nd", "6th_3rd",
				"7th_1st", "7th_2nd", "7th_3rd",
				"8th_1st", "8th_2nd", "8th_3rd",
				"9th_1st", "9th_2nd", "9th_3rd"]
	total_type = ["lec", "lab", "unit"]

	def _default_iso_printout(self):
		iso = self.env["ir.model.data"].search([("model", "=", "esmis.iso.printouts"),
												("name", "=", "esmis_iso_curriculum")])
		if iso:
			_logger.info(iso[0].res_id)
			iso_id = self.env["esmis.iso.printouts"].search([("id", "=", iso[0].res_id)])
			if iso_id:
				return iso_id[0]
		else:
			return None

	name = fields.Char('Curriculum', compute="_compute_name", store=True)
	iso_printout_id = fields.Many2one("esmis.iso.printouts", default=_default_iso_printout)
	department_id = fields.Many2one('esmis.department', "School/College", required=True)
	year_id = fields.Many2one('esmis.school.year', "School Year Start", required=True, domain="[('state', '=', 'Active')]")
	course_id = fields.Many2one('esmis.course', "Program", required=True, domain="[('department_id', '=', department_id)]")
	major = fields.Char(related="course_id.major")
	state = fields.Selection([("Draft", "Draft"),
							  ("Active", "Active"),
							  ("Done", "Done"),
							  ("Cancelled", "Cancelled")], default="Draft")
	section_ids = fields.One2many("esmis.sections", "curriculum_id")
	rec_1st_1st = fields.One2many('esmis.curriculum.1st.1st', 'curriculum_id', string="1st Year - 1st Semester")
	rec_1st_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_1st_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_1st_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_1st_2nd = fields.One2many('esmis.curriculum.1st.2nd', 'curriculum_id', string="1st Year - 2nd Semester")
	rec_1st_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_1st_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_1st_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_1st_3rd = fields.One2many('esmis.curriculum.1st.3rd', 'curriculum_id', string="1st Year - Mid Year")
	rec_1st_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_1st_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_1st_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_2nd_1st = fields.One2many('esmis.curriculum.2nd.1st', 'curriculum_id', string="2nd Year - 1st Semester")
	rec_2nd_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_2nd_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_2nd_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_2nd_2nd = fields.One2many('esmis.curriculum.2nd.2nd', 'curriculum_id', string="2nd Year - 2nd Semester")
	rec_2nd_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_2nd_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_2nd_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_2nd_3rd = fields.One2many('esmis.curriculum.2nd.3rd', 'curriculum_id', string="2nd Year - Mid Year")
	rec_2nd_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_2nd_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_2nd_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_3rd_1st = fields.One2many('esmis.curriculum.3rd.1st', 'curriculum_id', string="3rd Year - 1st Semester")
	rec_3rd_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_3rd_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_3rd_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_3rd_2nd = fields.One2many('esmis.curriculum.3rd.2nd', 'curriculum_id', string="3rd Year - 2nd Semester")
	rec_3rd_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_3rd_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_3rd_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_3rd_3rd = fields.One2many('esmis.curriculum.3rd.3rd', 'curriculum_id', string="3rd Year - Mid Year")
	rec_3rd_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_3rd_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_3rd_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_4th_1st = fields.One2many('esmis.curriculum.4th.1st', 'curriculum_id', string="4th Year - 1st Semester")
	rec_4th_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_4th_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_4th_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_4th_2nd = fields.One2many('esmis.curriculum.4th.2nd', 'curriculum_id', string="4th Year - 2nd Semester")
	rec_4th_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_4th_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_4th_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_4th_3rd = fields.One2many('esmis.curriculum.4th.3rd', 'curriculum_id', string="4th Year - Mid Year")
	rec_4th_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_4th_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_4th_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_5th_1st = fields.One2many('esmis.curriculum.5th.1st', 'curriculum_id', string="5th Year - 1st Semester")
	rec_5th_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_5th_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_5th_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_5th_2nd = fields.One2many('esmis.curriculum.5th.2nd', 'curriculum_id', string="5th Year - 2nd Semester")
	rec_5th_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_5th_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_5th_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_5th_3rd = fields.One2many('esmis.curriculum.5th.3rd', 'curriculum_id', string="5th Year - Mid Year")
	rec_5th_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_5th_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_5th_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_6th_1st = fields.One2many('esmis.curriculum.6th.1st', 'curriculum_id', string="6th Year - 1st Semester")
	rec_6th_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_6th_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_6th_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_6th_2nd = fields.One2many('esmis.curriculum.6th.2nd', 'curriculum_id', string="6th Year - 2nd Semester")
	rec_6th_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_6th_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_6th_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_6th_3rd = fields.One2many('esmis.curriculum.6th.3rd', 'curriculum_id', string="6th Year - Mid Year")
	rec_6th_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_6th_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_6th_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_7th_1st = fields.One2many('esmis.curriculum.7th.1st', 'curriculum_id', string="7th Year - 1st Semester")
	rec_7th_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_7th_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_7th_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_7th_2nd = fields.One2many('esmis.curriculum.7th.2nd', 'curriculum_id', string="7th Year - 2nd Semester")
	rec_7th_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_7th_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_7th_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_7th_3rd = fields.One2many('esmis.curriculum.7th.3rd', 'curriculum_id', string="7th Year - Mid Year")
	rec_7th_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_7th_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_7th_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_8th_1st = fields.One2many('esmis.curriculum.8th.1st', 'curriculum_id', string="8th Year - 1st Semester")
	rec_8th_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_8th_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_8th_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_8th_2nd = fields.One2many('esmis.curriculum.8th.2nd', 'curriculum_id', string="8th Year - 2nd Semester")
	rec_8th_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_8th_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_8th_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_8th_3rd = fields.One2many('esmis.curriculum.8th.3rd', 'curriculum_id', string="8th Year - Mid Year")
	rec_8th_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_8th_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_8th_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_9th_1st = fields.One2many('esmis.curriculum.9th.1st', 'curriculum_id', string="9th Year - 1st Semester")
	rec_9th_1st_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_9th_1st_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_9th_1st_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_9th_2nd = fields.One2many('esmis.curriculum.9th.2nd', 'curriculum_id', string="9th Year - 2nd Semester")
	rec_9th_2nd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_9th_2nd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_9th_2nd_total_unit = fields.Float("Total Units",
											compute="_compute_total")

	rec_9th_3rd = fields.One2many('esmis.curriculum.9th.3rd', 'curriculum_id', string="9th Year - Mid Year")
	rec_9th_3rd_total_lec = fields.Float("Total Lecture Hours/Week",
										   compute="_compute_total")
	rec_9th_3rd_total_lab = fields.Float("Total Laboratory Hours/Week",
										   compute="_compute_total")
	rec_9th_3rd_total_unit = fields.Float("Total Units",
											compute="_compute_total")


	total_lec = fields.Float("Total Lectures", compute="_compute_total_lec")
	total_lab = fields.Float("Total Lab", compute="_compute_total_lab")
	total_unit = fields.Float("Total Unites", compute="_compute_total_unit")

	def _compute_total_lec(self):
		for rec in self:
			total_lec = rec.rec_1st_1st_total_lec + rec.rec_1st_2nd_total_lec + rec.rec_1st_3rd_total_lec + rec.rec_2nd_1st_total_lec + rec.rec_2nd_2nd_total_lec + rec.rec_2nd_3rd_total_lec + rec.rec_3rd_1st_total_lec + rec.rec_3rd_2nd_total_lec + rec.rec_3rd_3rd_total_lec + rec.rec_4th_1st_total_lec + rec.rec_4th_2nd_total_lec + rec.rec_4th_3rd_total_lec + rec.rec_5th_1st_total_lec + rec.rec_5th_2nd_total_lec + rec.rec_5th_3rd_total_lec + rec.rec_6th_1st_total_lec + rec.rec_6th_2nd_total_lec + rec.rec_6th_3rd_total_lec
			rec.total_lec = total_lec

	def _compute_total_lab(self):
		for rec in self:
			total_lab = rec.rec_1st_1st_total_lab + rec.rec_1st_2nd_total_lab + rec.rec_1st_3rd_total_lab + rec.rec_2nd_1st_total_lab + rec.rec_2nd_2nd_total_lab + rec.rec_2nd_3rd_total_lab + rec.rec_3rd_1st_total_lab + rec.rec_3rd_2nd_total_lab + rec.rec_3rd_3rd_total_lab + rec.rec_4th_1st_total_lab + rec.rec_4th_2nd_total_lab + rec.rec_4th_3rd_total_lab + rec.rec_5th_1st_total_lab + rec.rec_5th_2nd_total_lab + rec.rec_5th_3rd_total_lab + rec.rec_6th_1st_total_lab + rec.rec_6th_2nd_total_lab + rec.rec_6th_3rd_total_lab
			rec.total_lab = total_lab

	def _compute_total_unit(self):
		for rec in self:
			total_unit = rec.rec_1st_1st_total_unit + rec.rec_1st_2nd_total_unit + rec.rec_1st_3rd_total_unit + rec.rec_2nd_1st_total_unit + rec.rec_2nd_2nd_total_unit + rec.rec_2nd_3rd_total_unit + rec.rec_3rd_1st_total_unit + rec.rec_3rd_2nd_total_unit + rec.rec_3rd_3rd_total_unit + rec.rec_4th_1st_total_unit + rec.rec_4th_2nd_total_unit + rec.rec_4th_3rd_total_unit + rec.rec_5th_1st_total_unit + rec.rec_5th_2nd_total_unit + rec.rec_5th_3rd_total_unit + rec.rec_6th_1st_total_unit + rec.rec_6th_2nd_total_unit + rec.rec_6th_3rd_total_unit
			rec.total_unit = total_unit

	@api.depends("course_id", "year_id")
	def _compute_name(self):
		for rec in self:
			rec.name = "{} {}".format(rec.course_id.acronym or '', rec.year_id.name or '')

	def _compute_total(self):
		for rec in self:
			for ys in self.year_sem:
				model_name = "esmis.curriculum.{}".format(ys.replace("_", "."))
				rec_lines = self.env[model_name].search([("curriculum_id", "=", rec.id)])
				for tt in self.total_type:
					total = 0
					for rec_line in rec_lines:
						if tt == "lec":
							total += rec_line.lec_hrs_week_1.unit
						if tt == "lab":
							total += rec_line.lab_hrs_week_1.unit
						if tt == "unit":
							total += rec_line.subject_id.subject_unit
					field_key = "rec_{}_total_{}".format(ys, tt)
					rec[field_key] = total

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

	def print_curriculum(self):
		for rec in self:
			return self.env.ref('esmis_curriculum.action_report_curriculum').report_action(rec)

class eSMISCurriculumSourceMixin(models.AbstractModel):
	_name = "esmis.curriculum.mixin"
	_description = "Change Request Data Source Mixin"

	curriculum_id = fields.Many2one('esmis.curriculum', "Curriculum")
	subject_id = fields.Many2one('esmis.subjects', "Subject Code", required=True)
	descriptive_title = fields.Char(related="subject_id.descriptive_title")
	lec_hrs_week = fields.Integer("Lecture Hrs/Week")
	lab_hrs_week = fields.Integer("Lab Hrs/Week")
	lec_hrs_week_1 = fields.Many2one('esmis.lec.lab.maintenance',string="Lecture Hrs/Week")
	lab_hrs_week_1 = fields.Many2one('esmis.lec.lab.maintenance',string="Lab Hrs/Week")
	subject_unit = fields.Integer("Units", related="subject_id.subject_unit")
	prerequisite = fields.Many2many('esmis.subjects')


class eSMISCurriculum1stYear1stSem(models.Model):
	_name = "esmis.curriculum.1st.1st"
	_description = "Curriculum 1st Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum1stYear2ndSem(models.Model):
	_name = "esmis.curriculum.1st.2nd"
	_description = "Curriculum 1st Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum1stYearMidYear(models.Model):
	_name = "esmis.curriculum.1st.3rd"
	_description = "Curriculum 1st Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum2ndYear1stSem(models.Model):
	_name = "esmis.curriculum.2nd.1st"
	_description = "Curriculum 2nd Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum2ndYear2ndSem(models.Model):
	_name = "esmis.curriculum.2nd.2nd"
	_description = "Curriculum 2nd Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum2ndYearMidYear(models.Model):
	_name = "esmis.curriculum.2nd.3rd"
	_description = "Curriculum 2nd Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum3rdYear1stSem(models.Model):
	_name = "esmis.curriculum.3rd.1st"
	_description = "Curriculum 3rd Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum3rdYear2ndSem(models.Model):
	_name = "esmis.curriculum.3rd.2nd"
	_description = "Curriculum 3rd Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum3rdYearMidYear(models.Model):
	_name = "esmis.curriculum.3rd.3rd"
	_description = "Curriculum 3rd Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum4thYear1stSem(models.Model):
	_name = "esmis.curriculum.4th.1st"
	_description = "Curriculum 4th Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum4thYear2ndSem(models.Model):
	_name = "esmis.curriculum.4th.2nd"
	_description = "Curriculum 4th Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum4thYearMidYear(models.Model):
	_name = "esmis.curriculum.4th.3rd"
	_description = "Curriculum 4th Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum5thYear1stSem(models.Model):
	_name = "esmis.curriculum.5th.1st"
	_description = "Curriculum 5th Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum5thYear2ndSem(models.Model):
	_name = "esmis.curriculum.5th.2nd"
	_description = "Curriculum 5th Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum5thYearMidYear(models.Model):
	_name = "esmis.curriculum.5th.3rd"
	_description = "Curriculum 5th Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum6thYear1stSem(models.Model):
	_name = "esmis.curriculum.6th.1st"
	_description = "Curriculum 6th Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum6thYear2ndSem(models.Model):
	_name = "esmis.curriculum.6th.2nd"
	_description = "Curriculum 6th Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


class eSMISCurriculum6thYearMidYear(models.Model):
	_name = "esmis.curriculum.6th.3rd"
	_description = "Curriculum 6th Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum7thYear1stSem(models.Model):
	_name = "esmis.curriculum.7th.1st"
	_description = "Curriculum 7th Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum7thYear2ndSem(models.Model):
	_name = "esmis.curriculum.7th.2nd"
	_description = "Curriculum 7th Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum7thYearMidYear(models.Model):
	_name = "esmis.curriculum.7th.3rd"
	_description = "Curriculum 7th Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum8thYear1stSem(models.Model):
	_name = "esmis.curriculum.8th.1st"
	_description = "Curriculum 8th Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum8thYear2ndSem(models.Model):
	_name = "esmis.curriculum.8th.2nd"
	_description = "Curriculum 8th Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum8thYearMidYear(models.Model):
	_name = "esmis.curriculum.8th.3rd"
	_description = "Curriculum 8th Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum9thYear1stSem(models.Model):
	_name = "esmis.curriculum.9th.1st"
	_description = "Curriculum 9th Year 1st Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum9thYear2ndSem(models.Model):
	_name = "esmis.curriculum.9th.2nd"
	_description = "Curriculum 9th Year 2nd Semester"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]

class eSMISCurriculum9thYearMidYear(models.Model):
	_name = "esmis.curriculum.9th.3rd"
	_description = "Curriculum 9th Year Mid Year"
	_order = "id asc"
	_inherit = ["esmis.curriculum.mixin", "mail.thread", "mail.activity.mixin"]


