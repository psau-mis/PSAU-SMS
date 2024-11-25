# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError


class Attendance(models.Model):
	_inherit = 'hr.attendance'

	#fields declaration
	user_id = fields.Many2one('res.users', string="User", required=True)
	employee_id = fields.Many2one(required=False)
	
	@api.constrains('check_in', 'check_out', 'employee_id')
	def _check_validity(self):
		return