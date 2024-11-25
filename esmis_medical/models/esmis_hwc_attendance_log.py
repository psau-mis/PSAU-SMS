# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisHealthWellnessCenterMembershipLogbook(models.Model):
	_name = "esmis.health.wellness.center.attendance.logbook"
	_description = "HWC Attendance Logbook"
	_rec_name = 'name'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	name = fields.Char(string="Name", compute="_compute_name", store=True)
	log_date = fields.Date(string="Date", default=datetime.today())
	log_line_ids = fields.One2many('esmis.hwc.attendance.logbook.line', 'hwc_id') 

	@api.depends('log_date')
	def _compute_name(self):    
		for record in self:   
			record.name = "Health and Wellness Center Daily Attendance Logbook - " + str(record.log_date)

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"


class EsmisHealthWellnessCenterMembershipLogbookLine(models.Model):
	_name = "esmis.hwc.attendance.logbook.line"
	# _description = "PSAU Clearance"

	hwc_id = fields.Many2one('esmis.health.wellness.center.attendance.logbook')
	employee_id = fields.Many2one('res.partner', string="Employee", required=True, domain="[('is_employee', '=', True)]")
	employee_type = fields.Selection([('CAS', 'CAS'),('CAST', 'CAST'),('CHEFS', 'CHEFS'),('COECS', 'COECS'),('COED', 'COED'),('CVM', 'CVM'),('ADMIN', 'ADMIN')], string="Membership")
	membership = fields.Selection([('Monthly', 'Monthly'),('Daily', 'Daily')], string="Membership")
	time_in = fields.Char(string="Time In")
	time_out = fields.Char(string="Time Out")


