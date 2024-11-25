# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisRxPad(models.Model):
	_name = "esmis.rx.pad"
	_description = "RX Pad"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	prescription_date = fields.Date(string="Prescription Date", default=datetime.today())
	line_ids = fields.One2many('esmis.rx.pad.line', 'rx_id') 


	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"


class EsmisRxPadLine(models.Model):
	_name = "esmis.rx.pad.line"
	# _description = "PSAU Clearance"

	rx_id = fields.Many2one('esmis.rx.pad')
	quantity = fields.Integer(string="QTY")
	medicine_id = fields.Many2one('esmis.medicine', string="Medicine")
	frequency = fields.Char(string="Frequency")





