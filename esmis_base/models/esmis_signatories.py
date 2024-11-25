# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisSignatories(models.Model):
	_name = "esmis.signatories"
	_description = "Signatories"

	name = fields.Char(string="Signatories:", required=True)
	position = fields.Char(string="Position 1", required=True)
	position2 = fields.Char(string="Position 2")
	e_signature = fields.Image(string="Signature")

