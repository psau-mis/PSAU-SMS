# Part of eSMIS App. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class eSMISSetORWizard(models.TransientModel):
	_name = "esmis.set.or.wizard"
	_description = "Set OR Wizard"

	cashier_id = fields.Many2one("esmis.cashier")
	name = fields.Char("O.R. #")
	or_date_mode = fields.Selection([("server", "Server Time"),
									 ("manual", "Set Manually")], default="server")
	or_date = fields.Datetime(default=fields.Datetime.now())

	# @api.constrains('category_name')
	# def _check_unique(self):
	# 	self._cr.execute("SELECT * FROM category_maintenance WHERE lower(category_name) = '"+self.category_name.lower()+"'")
	# 	result = self.env.cr.fetchall()
	# 	if len(result)>1:
	# 		raise ValidationError("Category Name already exists!")

	def set_cashier_or(self):
		try:
			float(self.name)
		except Exception as e:
			raise UserError(_('Invalid O.R. #'))

		for rec in self:
			if rec.cashier_id.or_no:
				if rec.cashier_id.status != 'draft':
					raise UserError("Can't edit O.R # at this point.")

		cashier_or = self.env['esmis.cashier'].search([])
		or_list = []
		already_exist = False
		for rec in cashier_or:
			if rec.or_no:
				or_list.append(int(rec.or_no))
		or_list.sort()
		for rec in or_list:
			if rec:
				if int(rec) == int(self.name):
					
					already_exist = True
		if already_exist == True:
			raise UserError('O.R # already exist')
		else:
			for rec in self:
				sequence_id = self.env['ir.sequence'].search([('code', '=', 'esmis.cashier.or')])
				sequence_id.number_next_actual = int(rec.name)
				rec.cashier_id.or_no = self.env['ir.sequence'].next_by_code('esmis.cashier.or')

				# rec.cashier_id.or_no = rec.name
				rec.cashier_id.or_date_mode = rec.or_date_mode
				rec.cashier_id.or_date = rec.or_date

				message = _("%s OR was successfully set.", rec.name)
				kind = "success"
				return {
					"type": "ir.actions.client",
					"tag": "display_notification",
					"params": {
						"title": _("OR Number set-up"),
						"message": message,
						"sticky": False,
						"type": kind,
						"next": {
							"type": "ir.actions.act_window_close",
						},
					},
				}