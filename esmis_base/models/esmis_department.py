# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisDepartment(models.Model):
	_name = "esmis.department"
	_description = "Department"

	logo = fields.Binary(string="Logo")

	name = fields.Char(string="School/College:", required=True)
	acronym = fields.Char(string="Acronym", required=True)
	
	current_dean_id = fields.Many2one('hr.employee', string="Current Dean/Head")
	email = fields.Char(string="Email Address")
	mobile_number = fields.Char(string="Mobile Phone Number")

	website = fields.Char(string="Website")
	phone_number = fields.Char(string="Office Phone Number")