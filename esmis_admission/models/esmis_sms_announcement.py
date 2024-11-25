from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from .m360_request import M360Request


class SmsAnnouncement(models.Model):
	_name = 'esmis.sms.announcement'
	_description = "SMS Announement"

	name = fields.Char(string="Name", required=True)
	partner_ids = fields.Many2many('res.partner', string="Contacts")
	category_id = fields.Many2one('res.partner.category', string="Contact Tags")
	category_ids = fields.Many2many('res.partner.category', string="Contact Tags")
	message = fields.Text(string="Message", required=True)
	response = fields.Text(string="Response")

	def send_sms(self):

		def check_partner_mobile(res_partner):
			mobile = ""
			if res_partner.mobile_number:
				mobile = res_partner.mobile_number.replace(' ', '')
			if res_partner.mobile:
				mobile = res_partner.mobile.replace(' ', '')
			return mobile

		if not len(self.partner_ids) and not len(self.category_ids):
			raise ValidationError(_('Please select either a Contact/s or Contact Tags.'))

		app_key = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.sms_app_key')
		app_secret = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.sms_app_secret')
		shortcode_mask = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.sms_shortcode_mask')
		m360_sms = M360Request(app_key, app_secret, shortcode_mask)
		response = ""
		contacts = []
		for partner in self.partner_ids:
			partner_no = check_partner_mobile(partner)
			contacts.append(partner_no)

		if len(self.category_ids):
			partner_with_categ_id = self.env['res.partner'].search([('category_id', 'in', self.category_ids.ids)])
			for contact in partner_with_categ_id:
				partner_no = check_partner_mobile(partner)
				contacts.append(partner_no)

		for contact in contacts:
			m360_response = m360_sms.send_sms(self.message, contact)
			response = response + '\n' + str(m360_response)

		self.response = response

	@api.model
	def update_partner_category(self):
		partner_ids = self.env['res.partner'].search([('category_id', '=', False)], limit=80)
		for partner in partner_ids:
			if partner.is_student:
				partner.write({'category_id': [(4, self.env.ref('esmis_admission.partner_categ_student').id)]})
			elif partner.is_parent:
				partner.write({'category_id': [(4, self.env.ref('esmis_admission.partner_categ_parent').id)]})
			else:
				partner.write({'category_id': [(4, self.env.ref('esmis_admission.partner_categ_internal_users').id)]})
