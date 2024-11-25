from odoo import api, fields, models, tools, _


class eSMISDepartment(models.Model):
	_inherit = 'esmis.department'

	level = fields.Selection([('undergrad', 'Undergraduate'),
		('graduate', 'Graduate'),
		('techvoc', 'Vocational'),
		('basiced', 'Basic Education')], string="Academic Level", required=True, default="undergrad")
