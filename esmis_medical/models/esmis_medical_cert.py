# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisMedicalCertificate(models.Model):
	_name = "esmis.medical.certificate"
	_description = "Medical Certificate"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	age = fields.Char(string="Age", related="client_id.age")
	gender = fields.Selection([('Male', 'Male'),('Female', 'Female')], string="Gender", related="client_id.gender")
	department_id = fields.Many2one('esmis.department')
	examine_date = fields.Date(string="Examine Date", default=datetime.today())
	diagnosis = fields.Text(string="Diagnosis")
	recommendation = fields.Text(string="Recommendation")
	requestor = fields.Char(string="Requestor")
	purpose = fields.Char(string="Purpose of Certificate")

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"


