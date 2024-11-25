from odoo import api, fields, models, tools, _


class ESMISSignatories(models.Model):
	_inherit = "esmis.signatories"

	honorific = fields.Char(string="Honorific Title")
