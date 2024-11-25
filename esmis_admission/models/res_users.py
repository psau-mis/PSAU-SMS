from odoo import api, fields, models, tools, _


class ResUsers(models.Model):
	_inherit = 'res.users'

	course_ids = fields.Many2many('esmis.course', string="Program/s", help="Restrict Program")
	department_ids = fields.Many2many('esmis.department', string="School/College", help="Restrict School/College")

	@api.constrains('course_ids')
	def _set_groups_course(self):
		course_group = self.env.ref('esmis_admission.group_has_course') or False
		if course_group:
			if len(self.course_ids):
				course_group.write({
					'users': [(4, self.id)]
					})
			else:
				course_group.write({
					'users': [(3, self.id)]
					})

	@api.constrains('department_ids')
	def _set_groups_department(self):
		dept_group = self.env.ref('esmis_admission.group_has_department') or False
		if dept_group:
			if len(self.department_ids):
				dept_group.write({
					'users': [(4, self.id)]
					})
			else:
				dept_group.write({
					'users': [(3, self.id)]
					})
