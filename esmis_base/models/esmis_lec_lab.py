# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisLecLabMaintenance(models.Model):
	_name = "esmis.lec.lab.maintenance"
	_rec_name = "unit"

	unit = fields.Float(string="Unit(s)", required=True)
	unit_char = fields.Char(string="Unit(s)", compute="_get_unit")

	def _get_unit(self):
		for rec in self:
			rec.unit_char = rec.unit
	

