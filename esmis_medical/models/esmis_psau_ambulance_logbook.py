# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisPsauAmbulanceLogbook(models.Model):
	_name = "esmis.psau.ambulance.logbook"
	_description = "PSAU Ambulance Logbook"

	log_date = fields.Date(string="Date/Time", default=datetime.today())
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	course_department = fields.Char(string="Course - Year / Department - Designation")
	case = fields.Char(string="Case")
	destination = fields.Char(string="Destination")
	medical_staff_driver = fields.Char(string="Medical Staff / Driver")