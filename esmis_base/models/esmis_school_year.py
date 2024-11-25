# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisSchoolYear(models.Model):
	_name = "esmis.school.year"
	_description = "School Year"

	name = fields.Char(string="Name", compute="_compute_name", store=True)
	year_to = fields.Char(string="Year To", required=True)
	year_from = fields.Char(string="Year From", required=True)
	sem = fields.Selection([('1st Semester', '1st Semester'),('2nd Semester', '2nd Semester'),('Mid-Term', 'Mid-Term')],default='Mid-Term',string="Semester", required=True)
	state = fields.Selection([('Draft', 'Draft'),('Started', 'Started'),('Ended', 'Ended'),('Active', 'Active'),('Inactive', 'Inactive')],'Status', default="Draft")

	@api.depends('year_from', 'year_to', 'sem')
	def _compute_name(self):    
		for record in self:		
			record.name = str(record.year_from)+ "-" + str(record.year_to) + "(" + str(record.sem) +")"
			
	def set_active(self):
		self.state = "Active"

	def set_started(self):
		self.state = "Started"

	def set_inactive(self):
		self.state = "Inactive"

	def set_ended(self):
		self.state = "Ended"