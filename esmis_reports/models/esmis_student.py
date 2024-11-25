import logging
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class InheritEsmisStudents(models.Model):
	_inherit = 'res.partner'

	def _default_iso_printout(self):
		iso = self.env["ir.model.data"].search([("model", "=", "esmis.iso.printouts"),
												("name", "=", "esmis_iso_certification")])
		if iso:
			_logger.info(iso[0].res_id)
			iso_id = self.env["esmis.iso.printouts"].search([("id", "=", iso[0].res_id)])
			if iso_id:
				return iso_id[0]
		else:
			return None

	
	iso_printout_id = fields.Many2one("esmis.iso.printouts", default=_default_iso_printout)