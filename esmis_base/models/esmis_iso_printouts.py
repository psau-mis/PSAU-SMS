# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisIsoPrintouts(models.Model):
	_name = "esmis.iso.printouts"
	_description = "ISO Printouts"

	name = fields.Char(string="Form:")
	iso = fields.Char(string="Position 1")
	signatories = fields.Many2many('esmis.signatories')
	

