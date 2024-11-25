from odoo import api, fields, models, tools, _
from .m360_request import M360Request
from odoo.exceptions import ValidationError
import pytz


class Meeting(models.Model):
	_inherit = 'calendar.event'

	category_id = fields.Many2one('res.partner.category', string="Contact Tags")
	category_ids = fields.Many2many('res.partner.category', string="Contact Tags")

	def action_send_m360_sms(self):
		def check_partner_mobile(res_partner):
			mobile = ""
			if res_partner.mobile_number:
				mobile = res_partner.mobile_number.replace(' ', '')
			if res_partner.mobile:
				mobile = res_partner.mobile.replace(' ', '')
			return mobile

		app_key = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.sms_app_key')
		app_secret = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.sms_app_secret')
		shortcode_mask = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.sms_shortcode_mask')
		m360_sms = M360Request(app_key, app_secret, shortcode_mask)
		partner_ids_list = []
		if len(self.partner_ids):
			partner_ids_list = partner_ids_list + self.partner_ids.ids
		if len(self.category_ids):
			partner_with_categ_id = self.env['res.partner'].search([('category_id', 'in', self.category_ids.ids)])
			partner_ids_list = partner_ids_list + partner_with_categ_id.ids
		partner_ids = self.env['res.partner'].browse(partner_ids_list)
		for partner in partner_ids:
			mobile_number = check_partner_mobile(partner)
			body = f"""Good day!

You've been invited to {self.name} on {self.start.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Manila'))} to {self.stop.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Manila'))}. Please check your PSAU portal for more details."""

			response = m360_sms.send_sms(body, mobile_number)
			self.message_post(body=str(response))

	def action_send_sms(self):
		self.action_send_m360_sms()
