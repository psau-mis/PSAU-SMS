import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)

   
class EsmisGrade(models.Model):
	_name = "esmis.grade.management"
	_description = "Grades"
	_rec_name = "section_id"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	status = fields.Selection([("draft", "Draft"),	   
							   ("validated", "Validated"),
							   ("posted", "Posted")], default="draft")

	section_id = fields.Many2one('esmis.sections', string="Section", required=True)
	school_year_id = fields.Many2one('esmis.school.year', required=True)
	subject_id = fields.Many2one('esmis.subjects', string="Subject", required=True)
	grade_lines = fields.One2many('esmis.grade.management.line', 'grade_id')
	term = fields.Selection([('midterm', 'Midterm'),('final', 'Final')], string="Term")
	date_posted = fields.Date(string="Date Posted")

	@api.constrains('section_id', 'school_year_id', 'subject_id')
	def constrainst_section_subject_sy(self):
		constraints_id = self.env['esmis.grade.management'].search([('school_year_id', '=', self.school_year_id.id),('section_id', '=', self.section_id.id),('subject_id', '=', self.subject_id.id)])

		if len(constraints_id) > 1:
			raise ValidationError(_("You've already have a record that matches school year, section and subject"))
	

	@api.onchange('school_year_id')
	def _get_sections(self):
		self.section_id = False
		hr_employee_id = self.env['hr.employee'].search([('user_id', '=', self._uid)])
		
		section_id = self.env['esmis.sections'].search([('year_id', '=', self.school_year_id.id)])

		section_list = []
		for sec_id in section_id:
			section_list.append(sec_id.id)
		subject_offerings_id = self.env['esmis.subject.offerings'].search([('teacher_id', '=', hr_employee_id.id), ('section_id', 'in', section_list)])

		section_ids = []
	
		for rec in subject_offerings_id:
			section_ids.append(rec.section_id.id)
	
		return {'domain':{'section_id': [('id', 'in', section_ids)]}}

	@api.onchange('section_id')
	def _get_subjects(self):
		self.subject_id = False
		hr_employee_id = self.env['hr.employee'].search([('user_id', '=', self._uid)])
	
		section_id = self.env['esmis.sections'].search([('year_id', '=', self.school_year_id.id)])
		section_list = []
		for sec_id in section_id:
			section_list.append(sec_id.id)
		subject_offerings_id = self.env['esmis.subject.offerings'].search([('teacher_id', '=', hr_employee_id.id), ('section_id', '=', self.section_id.id)])

		
		subject_ids = []
		for rec in subject_offerings_id:
			subject_ids.append(rec.subject_id.id)
		return {'domain':{'subject_id': [('id', 'in', subject_ids)]}}

	@api.onchange('section_id', 'subject_id')
	def _get_students(self):
		for recs in self:
			recs.grade_lines = None
			if recs.section_id:
				hr_employee_id = self.env['hr.employee'].search([('user_id', '=', recs._uid)])
				enrollment_ids = self.env['esmis.enrollment'].search([('school_year_id', '=', recs.school_year_id.id),('section_id', '=', recs.section_id.id),('subject_enrolled.teacher_id', '=', hr_employee_id.id),('status', '=', 'enrolled')])
				vals = []

				for enrollment_id in enrollment_ids:
					student_ids = self.env['res.partner'].search([('id', '=', enrollment_id.student_id.id)])
					for rec in student_ids:
						student_val = {
							"student_id": rec.id,
							"gender": rec.gender

						}
					
						vals.append((Command.create(student_val)))

				recs.update({"grade_lines": vals})

	def on_validate(self):
		for rec in self.grade_lines:
			if rec.final:
				pass
			else:
				raise ValidationError("Fill up all Final ratings")

		self.status = "validated"

	def on_posted(self):
		for rec in self:
			rec.date_posted = datetime.today()

			for recs in rec.grade_lines:
				recs.status = 'posted'

		self.status = "posted"




class EsmisGradeLine(models.Model):
	_name = "esmis.grade.management.line"

	grade_id = fields.Many2one('esmis.grade.management')
	student_id = fields.Many2one("res.partner", domain="[('is_student','=',True)]")
	gender = fields.Selection([('Male', 'Male'),('Female', 'Female')], string="Gender")
	midterm_grade = fields.Char(string="Midterm")
	midterm_eq = fields.Char(string="Midterm EQ", compute="_compute_midterm_grade_calc", store=True)
	midterm_remarks = fields.Text(string="Midterm Remarks", compute="_compute_midterm_grade_calc", store=True)
	final = fields.Char(string="Final Rating")
	final_1 = fields.Float(string="Final")
	final_rating = fields.Float(string="Final Rating")
	final_eq = fields.Char(string="Final EQ", compute="_compute_final_grade_calc", store=True)
	remarks = fields.Text(string="Remarks", compute="_compute_final_grade_calc", store=True)
	actual_final_ave = fields.Char(string="Actual Final Average", related="final_eq")
	# date_posted = fields.Date(string="Date Posted")
	note = fields.Text(string="Note")

	section_id = fields.Many2one('esmis.sections', string="Section", related="grade_id.section_id")
	school_year_id = fields.Many2one('esmis.school.year', related="grade_id.school_year_id")
	subject_id = fields.Many2one('esmis.subjects', string="Subject", related="grade_id.subject_id")
	date_posted = fields.Date(string="Date Posted", related="grade_id.date_posted")
	date_re_posted = fields.Date(string="Date Re-Posted")

	re_exam = fields.Char(string="Re-exam")
	status = fields.Selection([("unpost", "Unpost"),
							   ("posted", "Posted")], default="unpost")

	

	@api.depends("final")
	def _compute_final_grade_calc(self):
		for rec in self:
			grade_eq_ids = rec.env['esmis.grade.eq'].search([('is_active', '=', True)], limit=1)
			if rec.final:
				if rec.final.isdigit():
					if float(rec.final) <=100 and float(rec.final) >=0:
						final_eq = grade_eq_ids.get_eq_from_grade(float(rec.final))
						if not final_eq:
							raise ValidationError("Invalid Grade")
						# raise ValidationError(final_eq)
						rec.final_eq = str(final_eq)
						if float(rec.final_eq) >= 4:
							rec.remarks = "FAILED"
						if float(rec.final_eq) <= 3 and float(rec.final) >=1:
							rec.remarks = "PASSED"
					else:
						raise ValidationError("Invalid Input")
				else:
					# raise ValidationError("nope")
					if rec.final.upper() == "INC":
						rec.final_eq = "INC"
						rec.remarks = "INCOMPLETE"
					elif rec.final.upper() == "NJ":
						rec.final_eq = "NJ"
						rec.remarks = "NO PROJECT"
					elif rec.final.upper() == "UD":
						rec.final_eq = "UD"
						rec.remarks = "UNOFFICIALLY DROP"
					elif rec.final.upper() == "OD":
						rec.final_eq = "OD"
						rec.remarks = "OFFICIALLY DROP"
					elif rec.final.upper() == "NE":
						rec.final_eq = "NE"
						rec.remarks = "NO EXAM"
					elif rec.final.upper() == "NA":
						rec.final_eq = "NA"
						rec.remarks = "NOT ATTENDING"
					else:
						raise ValidationError("Invalid Input")

	@api.depends("midterm_grade")
	def _compute_midterm_grade_calc(self):
		for rec in self:
			grade_eq_ids = rec.env['esmis.grade.eq'].search([('is_active', '=', True)], limit=1)
			if rec.midterm_grade:
				if rec.midterm_grade.isdigit():
					if float(rec.midterm_grade) <=100 and float(rec.midterm_grade) >=0:
						midterm_eq = grade_eq_ids.get_eq_from_grade(float(rec.midterm_grade))
						if not midterm_eq:
							raise ValidationError("Invalid Grade")
						# raise ValidationError(final_eq)
						rec.midterm_eq = str(midterm_eq)
						if float(rec.midterm_eq) >= 4:
							rec.midterm_remarks = "FAILED"
						if float(rec.midterm_eq) <= 3 and float(rec.midterm_grade) >=1:
							rec.midterm_remarks = "PASSED"
					else:
						raise ValidationError("Invalid Input")
				else:
					# raise ValidationError("nope")
					if rec.midterm_grade.upper() == "INC":
						rec.midterm_eq = "INC"
						rec.midterm_remarks = "INCOMPLETE"
					elif rec.midterm_grade.upper() == "NJ":
						rec.midterm_eq = "NJ"
						rec.midterm_remarks = "NO PROJECT"
					elif rec.midterm_grade.upper() == "UD":
						rec.midterm_eq = "UD"
						rec.midterm_remarks = "UNOFFICIALLY DROP"
					elif rec.midterm_grade.upper() == "OD":
						rec.midterm_eq = "OD"
						rec.midterm_remarks = "OFFICIALLY DROP"
					elif rec.midterm_grade.upper() == "NE":
						rec.midterm_eq = "NE"
						rec.midterm_remarks = "NO EXAM"
					elif rec.midterm_grade.upper() == "NA":
						rec.midterm_eq = "NA"
						rec.midterm_remarks = "NOT ATTENDING"
					else:
						raise ValidationError("Invalid Input")

	def re_post(self):
		self.date_re_posted = datetime.today()
		for rec in self:
			rec.status = 'posted'

	def unpost_grade(self):
		for rec in self:
			# rec.grades_id.status = "draft"
			rec.status = 'unpost'