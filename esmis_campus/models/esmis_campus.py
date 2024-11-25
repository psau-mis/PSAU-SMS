# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisCampus(models.Model):
	_name = "esmis.campus"
	_description = "Campus"

	name = fields.Char(string="Campus", required=True)
	location = fields.Text(string="Location")
	total_buildings = fields.Integer(string="Total Buildings")
	image = fields.Binary(string="Image")
	building_ids = fields.One2many('esmis.building','campus_id')


