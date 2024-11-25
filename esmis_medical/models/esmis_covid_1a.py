# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisMedicalCovidCloseContact1a(models.Model):
	_name = "esmis.covid.1a"
	_description = "Close Contact 1a"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]")
	test_date = fields.Date(string="Date test was done", default=datetime.today())

	with_symptoms = fields.Boolean(string="With Symptoms")
	result_date = fields.Date(string="Date of result", default=datetime.today())
	date_symptoms = fields.Date(string="Date of first symptom/s", default=datetime.today())
	contact_ids= fields.One2many('esmis.covid.1a.line', 'contact_1a_id')
	covid_vac_ids = fields.One2many('esmis.medical.covid.vaccination', 'contact_1a_id', string="Create Covid-19 Vaccinations")


	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"



class EsmisMedicalCovidCloseContact1aLine(models.Model):
	_name = "esmis.covid.1a.line"
	_description = "Close Contact 1A Line"


	contact_1a_id = fields.Many2one('esmis.covid.1a')
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]")
	client_type = fields.Selection([('PSAU Student', 'PSAU Student'),('PSAU Employee', 'PSAU Employee'),('Outsider', 'Outsider')], 'Client Type', default="PSAU Employee")
	face_distance = fields.Boolean(string="Face to face distance of 6 feet or 2 meters")
	with_mask = fields.Boolean(string="With Mask")
	atleast_minutes = fields.Boolean(string="At least 15 minutes(cumulative) in 1 day")
	date_exposure = fields.Date(string="Date of Exposure", default=datetime.today())
	for_quarantine = fields.Boolean(string="For Quarantine")

class EsmisInheritCovidVax1A(models.Model):
	_inherit = 'esmis.medical.covid.vaccination'

	contact_1a_id = fields.Many2one('esmis.covid.1a')