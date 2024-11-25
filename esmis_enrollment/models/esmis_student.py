from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,Warning



class InheritEsmisStudents(models.Model):
	_inherit = 'res.partner'

	enrollment_ids = fields.Many2many('esmis.enrollment', string="Enrollment Record", compute="_compute_student_enrollment")

	def _compute_student_enrollment(self):
		for rec in self:
			# student_number = rec.env['res.partner'].search([('student_no_undg', '=', rec.student_no_undg),('student_no_grad', '=', rec.student_no_grad)])
			# for recs in student_number:
			student_enrollment = rec.env['esmis.enrollment'].search([('student_id', '=', rec.id)])
			rec.enrollment_ids = [(4, enrollment.id) for enrollment in student_enrollment]
