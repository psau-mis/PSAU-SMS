from odoo import api, fields, models, tools, _


class ResBarangay(models.Model):
	_name = 'res.barangay'
	_description = 'Barangay Records'

	name = fields.Char(string='Name', required=True)
	city_id = fields.Many2one('res.city', string="City", required=True)
