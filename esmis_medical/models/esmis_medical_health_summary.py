# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisMedicalHealthSummary(models.Model):
	_name = "esmis.medical.health.summary"
	_description = "Health Record"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)

	# covid vax
	covid_vac_ids = fields.Many2many('esmis.medical.covid.vaccination', string="Covid Vaccination", compute="_compute_covid_vax")

	# family history
	line_ids = fields.One2many('esmis.medical.health.summary.line', 'medical_health_summary_id')




	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"

	def _compute_covid_vax(self):
		for rec in self:
			covid_vax = rec.env['esmis.medical.covid.vaccination'].search([('client_id', '=', rec.client_id.id)])
			rec.covid_vac_ids = [(4, covid_vax.id) for recs in covid_vax]




class EsmisMedicalHealthSummaryLine(models.Model):
	_name = "esmis.medical.health.summary.line"
	# _description = "PSAU Clearance"

	medical_health_summary_id = fields.Many2one('smis.medical.health.summary')
	date = fields.Date(string="Date", default=datetime.today())
	bp = fields.Char(string="BP")
	test = fields.Char(string="Test")
	result = fields.Char(string="Result")	



