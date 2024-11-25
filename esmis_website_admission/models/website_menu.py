from odoo import models


class WebsiteMenu(models.Model):
	_inherit = 'website.menu'

	def _compute_visible(self):
		super(WebsiteMenu, self)._compute_visible()
		for menu in self:
			cancelled_admission = menu.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_admission')
			if cancelled_admission:
				try:
					admission_menu = menu.env.ref('esmis_website_admission.esmis_main_admission_web_menu')
					if admission_menu.url == menu.url:
						menu.is_visible = False
				except Exception as e:
					pass
			