# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisWorkFromHomeRequest(models.Model):
	_name = "esmis.work.from.home.request"
	_description = "Work From Home Request"
	_rec_name = 'employee_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	employee_id = fields.Many2one('res.partner', string="Employee", required=True, domain="[('is_employee', '=', True)]")
	request_date = fields.Date(string="Request Date")
	reason = fields.Text(string="Reason")

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"



