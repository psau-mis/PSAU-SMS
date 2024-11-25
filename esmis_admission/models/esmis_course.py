from odoo import api, fields, models, tools, _


class eSMISCourse(models.Model):
	_inherit = 'esmis.course'

	responsible_user_ids = fields.Many2many('res.users', string="Responsible", required=True)
	confirmation_password = fields.Char(string="Confirmation Password", required=True)

	@api.constrains('responsible_user_ids')
	def update_responsible_admission_exam(self):
		admissions = self.env['esmis.admission'].search([('state', 'not in', ['admitted', 'cancelled']), ('active_course_id', '=', self.id)])
		for rec in admissions:
			rec.update({
				'user_evaluation_responsible_ids': [(6, 0, self.responsible_user_ids.ids)],
				})

