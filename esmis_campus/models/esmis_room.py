# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisRoom(models.Model):
	_name = "esmis.room"
	_description = "Rooms"
	_rec_name = "bldng_room"

	bldng_room = fields.Char(string="blding room", compute="get_bldng_room_name")
	name = fields.Char(string="Room", required=True)
	campus_id = fields.Many2one("esmis.campus", string="Campus")
	building_id = fields.Many2one("esmis.building", string="Building")

	room_type = fields.Selection([('Classroom','Classroom'),('Office','Office'),('Gym','Gym')],string="Location")
	floor = fields.Integer(string="Floor")
	image = fields.Binary(string="Image")


	def get_bldng_room_name(self):
		for rec in self:
			rec.bldng_room =  rec.building_id.name + "-" + rec.name 
