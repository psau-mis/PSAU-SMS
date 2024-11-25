# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisMedicalCovidCloseContact1b(models.Model):
	_name = "esmis.covid.1b"
	_description = "Close Contact 1B"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]")
	report_date = fields.Date(string="Date Reported", default=datetime.today())

	with_symptoms = fields.Boolean(string="With Symptoms")
	place_of_contact = fields.Char(string="Place of Contact")
	contact_date = fields.Date(string="Date of Contact", default=datetime.today())
	contact_duration = fields.Integer(string="Duration of Contact")

	contact_ids= fields.One2many('esmis.covid.1b.line', 'contact_1b_id')
	covid_vac_ids = fields.One2many('esmis.medical.covid.vaccination', 'contact_1b_id', string="Create Covid-19 Vaccinations")



	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"



class EsmisMedicalCovidCloseContact1bLine(models.Model):
	_name = "esmis.covid.1b.line"
	_description = "Close Contact 1B Line"


	contact_1b_id = fields.Many2one('esmis.covid.1b')
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]")
	client_type = fields.Selection([('PSAU Student', 'PSAU Student'),('PSAU Employee', 'PSAU Employee'),('Outsider', 'Outsider')], 'Client Type', default="PSAU Employee")
	face_distance = fields.Boolean(string="Face to face distance of 6 feet or 2 meters")
	with_mask = fields.Boolean(string="With Mask")
	atleast_minutes = fields.Boolean(string="At least 15 minutes(cumulative) in 1 day")
	date_exposure = fields.Date(string="Date of Exposure", default=datetime.today())


class EsmisInheritCovidVax(models.Model):
	_inherit = 'esmis.medical.covid.vaccination'

	contact_1b_id = fields.Many2one('esmis.covid.1b')