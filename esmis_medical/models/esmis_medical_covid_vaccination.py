# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisMedicalCovidVaccination(models.Model):
	_name = "esmis.medical.covid.vaccination"
	_description = "Medical Covid Vaccination"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")

	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]")

	vac_date = fields.Date(string="Date", default=datetime.today(), required=True)
	dose = fields.Char(string="Dose", required=True)
	brand = fields.Char(string="Brand", required=True)
	administering_agency = fields.Char(string="Administering Agency", required=True)

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"



