from odoo import models, fields


class eSMISStudents(models.Model):
	_inherit = 'res.partner'

	barangay_id = fields.Many2one('res.barangay', string="Barangay")
