# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisSubjects(models.Model):
	_name = "esmis.subjects"
	_description = "Subjects"
	_rec_name = "subject"

	subject = fields.Char(string="Subject", required=True)
	descriptive_title = fields.Char(string="Descriptive Title", required=True)
	subject_unit = fields.Integer(string="Units", required=True)

	