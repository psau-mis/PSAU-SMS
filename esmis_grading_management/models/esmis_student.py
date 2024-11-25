from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,Warning



class InheritEsmisStudents(models.Model):
	_inherit = 'res.partner'

	grades_ids = fields.Many2many('esmis.grade.management.line', string="Grade Record", compute="_compute_student_grades")

	def _compute_student_grades(self):
		for rec in self:
			# student_number = rec.env['res.partner'].search([('student_no_undg', '=', rec.student_no_undg),('student_no_grad', '=', rec.student_no_grad)])
			# for recs in student_number:
			student_grade = rec.env['esmis.grade.management.line'].search([('student_id', '=', rec.id)])
			rec.grades_ids = [(4, grades.id) for grades in student_grade]

	def print_cog(self):
		for rec in self:
			return self.env.ref('esmis_grading_management.action_certificate_of_grades').report_action(rec)
