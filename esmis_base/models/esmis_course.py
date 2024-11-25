# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisCourse(models.Model):
	_name = "esmis.course"
	_description = "Course"

	name = fields.Char(string="Program Title:", required=True, tracking=True)
	acronym = fields.Char(string="Acronym", required=True, tracking=True)
	major = fields.Char(string="Major", compute="_major_name", inverse="_inverse_major_name", store=True, tracking=True)
	department_id = fields.Many2one('esmis.department', string="School/College", required=True, tracking=True)
	level = fields.Selection([('Undergraduate', 'Undergraduate'),
		('Graduate', 'Graduate'),
		('Masteral', 'Masteral'),
		('Doctorate', 'Doctorate'),
		('Vocational', 'Vocational'),
		('Basic Education', 'Basic Education')],string="Academic Level", required=True, tracking=True)
	course_desc = fields.Text(tracking=True)
	major_flag = fields.Boolean()

	# @api.depends('major')
	def _major_name(self):
		for rec in self:
			if rec.major_flag == False:
				rec.major = rec.name
			

	# @api.depends('major')
	def _inverse_major_name(self):
		for rec in self:
			if rec.major:
				if rec.major != rec.name:
					rec.major_flag = True
				else:
					rec.major_flag = False
			else:
				rec.major = rec.name
				rec.major_flag = False