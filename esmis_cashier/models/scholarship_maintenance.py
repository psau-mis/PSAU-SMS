# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisScohlarshipMaintenance(models.Model):
	_name = "esmis.scholarship.maintenance"
	_rec_name = "scholarship_type"

	code = fields.Char(string="Code", required=True)
	scholarship_type = fields.Char(string="Scholarship Type", required=True)
	provider = fields.Char(string="Provider", required=True)


