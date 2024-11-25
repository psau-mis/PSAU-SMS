from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, Warning
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime
from functools import reduce


class InheritEsmisStudents(models.Model):
	_inherit = 'res.partner'

	grades_ids = fields.Many2many('esmis.grade.management.line', string="Grade Record", compute="_compute_student_grades")

	def _compute_student_grades(self):
		for rec in self:
			# student_number = rec.env['res.partner'].search([('student_no_undg', '=', rec.student_no_undg),('student_no_grad', '=', rec.student_no_grad)])
			# for recs in student_number:
			student_grade = rec.env['esmis.grade.management.line'].search([('student_id', '=', rec.id), ('grade_id.status', '=', 'posted')])
			rec.grades_ids = [(4, grades.id) for grades in student_grade]

	def print_cog(self):
		for rec in self:
			return self.env.ref('esmis_grading_management.action_certificate_of_grades').report_action(rec)

	@api.model
	def get_date_issued(self, given_date=False):
		if given_date:
			try:
				return datetime.strptime(str(given_date), DATE_FORMAT).strftime('%B %d, %Y')
			except Exception as e:
				return ""
		return datetime.today().strftime('%B %d, %Y')

	@api.model
	def get_tor_remarks(self):
		remarks = "GRADUATED with the degree of %s on %s, as per Board Resolution No. 23-59. PSAU is chartered State University; hence, Special Order is not issued to graduates." %(self.current_course_id.name, self.get_date_issued(self.date_of_graduation))
		paragraphs = {1: '', 2: '', 3: '', 4: ''}
		current_paragraph = 1
		for wr in remarks.split(' '):
			if current_paragraph >= 4:
				break
			current_paragraph_length = reduce(lambda x, y: x + 1 if y == ' ' else x, paragraphs[current_paragraph], 1)
			if current_paragraph_length > 15:
				current_paragraph = current_paragraph + 1
			paragraphs[current_paragraph] = paragraphs[current_paragraph] + ' ' + wr

		return paragraphs
