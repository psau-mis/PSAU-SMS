from odoo import models


class ResCountry(models.Model):
	_inherit = 'res.country'

	def get_esmis_countries(self):
		return self.sudo().search([])

	def get_esmis_states(self):
		return self.sudo().state_ids

	def get_esmis_cities(self):
		return self.env['res.city'].sudo().search([('country_id', '=', self.id)])

class ResCountryStates(models.Model):
	_inherit = 'res.country.state'

	def get_esmis_cities_on_states(self):
		return self.env['res.city'].sudo().search([('state_id', '=', self.id)])

class ResCity(models.Model):
	_inherit = 'res.city'

	def get_esmis_barangay_on_city(self):
		return self.env['res.barangay'].sudo().search([('city_id', '=', self.id)])
