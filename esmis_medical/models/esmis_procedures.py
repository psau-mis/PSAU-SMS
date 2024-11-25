# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisProcedureType(models.Model):
	_name = "esmis.procedures"
	_description = "Procedure"

	procedure_type_id = fields.Many2one('esmis.procedure.type' ,string="Document Title", required=True)
	document_number = fields.Char(string="Document Number")
	dcn_number = fields.Char(string="DCN Number")
	revision_number = fields.Integer(string="Revision Number")
	date_originated = fields.Date(string="Date Originated", default=datetime.today())
	effective_date = fields.Date(string="Effective Date", default=datetime.today())

	from_revision = fields.Text(string="From")
	to_revision = fields.Text(string="To")
	details = fields.Text(string="Details")




