# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisHealthServicesLogbook(models.Model):
	_name = "esmis.health.services.logbook"
	_description = "Health Services Logbook"
	_rec_name = 'name'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	log_line_ids = fields.One2many('esmis.health.services.logbook.line', 'health_services')
	log_date = fields.Date(string="Date", default=datetime.today()) 
	name = fields.Char(string="Name")


	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"

	def create_lines_wizard(self):
	
		wiz = self.env['esmis.health.services.logbook.wiz'].with_context(default_log_id = self.id).create({})
		return {
			"name": "Create Record",
			"view_mode": "form",
			"res_model": "esmis.health.services.logbook.wiz",
			"view_id": self.env.ref(
				"esmis_medical.esmis_health_services_logbook_wizard_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			'res_id': self.id,
			# 'context': self.env.context,
			'context':{'default_log_id': self.id},
			
		}


class EsmisHealthServicesLogbookLine(models.Model):
	_name = "esmis.health.services.logbook.line"
	# _description = "PSAU Clearance"

	health_services = fields.Many2one('esmis.health.services.logbook')
	log_time = fields.Datetime(string="Time")
	name = fields.Char(string="Client Name")
	client_type = fields.Selection([('Employee', 'Employee'),('Student', 'Student'),('Outsider', 'Outsider')], 'Client Type', default="Student")
	type_field = fields.Char(string="Type")
	purpose = fields.Selection([('Medical', 'Mecical'),('Dental', 'Dental')], 'Purpose', default="Medical")
	dx = fields.Text(string="DX")




