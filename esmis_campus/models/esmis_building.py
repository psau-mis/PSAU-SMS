# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisBuilding(models.Model):
	_name = "esmis.building"
	_description = "Buildings"

	name = fields.Char(string="Building", required=True)
	campus_id = fields.Many2one("esmis.campus", string="Campus")
	floors = fields.Integer(string="Floor")
	total_rooms = fields.Integer(string="Total Rooms")
	image = fields.Binary(string="Image")
	room_ids = fields.One2many('esmis.room', 'building_id')

