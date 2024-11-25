# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisPsauClearance(models.Model):
	_name = "esmis.psau.clearance"
	_description = "PSAU Clearance"
	_rec_name = 'clearance_date'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	clearance_date = fields.Date(string="Clearance Date", default=datetime.today())
	clearance_issue_place = fields.Char(string="Issued on")
	employee_ids = fields.One2many('esmis.psau.clearance.line', 'psau_clearance_id', string="Employee")

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"


class EsmisPsauClearanceLine(models.Model):
	_name = "esmis.psau.clearance.line"
	_description = "PSAU Clearance"

	psau_clearance_id = fields.Many2one('esmis.psau.clearance')
	employee_id = fields.Many2one('res.partner', string="Employee", domain="[('is_employee', '=', True)]")





