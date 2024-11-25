# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisCashRemittance(models.Model):
	_name = "esmis.cash.remittance"
	_description = "Cash Remittance"

	remittance_date = fields.Date(string="Date", default=datetime.today())
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	procedure_id = fields.Many2one('esmis.dental.procedure', string="Procedures", required=True)
	sale_invoice = fields.Char(string="Sale Invoice", required=True)
	amount = fields.Float(string="Amount")	