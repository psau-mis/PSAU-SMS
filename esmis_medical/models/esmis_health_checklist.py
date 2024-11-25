# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisHealthChecklist(models.Model):
	_name = "esmis.health.checklist"
	_description = "Health Checklist"
	_rec_name = 'name'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	name = fields.Char(string="Client Name", compute="_compute_name", store=True)
	client_type = fields.Selection([('Employee', 'Employee'),('Student', 'Student'),  ('Visitor', 'Visitor')], 'Client Type', default="Employee")
	checklist_date = fields.Date(string="Checklist Date", default=datetime.today())
	employee_id = fields.Many2one('res.partner', string="Employee Name", domain="[('is_employee', '=', True)]")
	student_id = fields.Many2one('res.partner', string="Student Name", domain="[('is_student', '=', True)]")
	temp = fields.Char(string="Temperature")

	visitor_name = fields.Char(string="Visitor Name")
	visitor_gender = fields.Selection([('Male', 'Male'),('Female', 'Female')], 'Visitor Sex', default="Male")
	visitor_age = fields.Integer(string="Visitor Age")
	visitor_contact_number = fields.Char(string="Visitor Contact Number") 

	q1 = fields.Boolean('Are you experiencing sore throat / cough / colds?')
	q2 = fields.Boolean('Are you experiencing body pains?')
	q3 = fields.Boolean('Are you experiencing headache?')
	q4 = fields.Boolean('Are you experiencing fever for the past few days?')
	q5 = fields.Boolean('Are you experiencing diarrhea?')
	q6 = fields.Boolean('Have you worked together or stayed in the same close environment of a confirmed COVID-19 case?')
	q7 = fields.Boolean('Have you had any contact with anyone with fever, cough, colds, and sore throat in the past 2 weeks?')
	q8 = fields.Boolean('Have you travelled outside of the Philippines in the last 14 days?')
	q9 = fields.Boolean('Have you travelled to any area under ECQ, MECQ, and GCQ aside from your home?')
	q10 = fields.Boolean('Do you have any underlying medical problem?')
	q11 = fields.Boolean('Are you pregnant?')

	@api.depends('client_type', 'student_id', 'employee_id', 'visitor_name')
	def _compute_name(self):    
		for record in self:
			if record.client_type == "Employee":   
				record.name = record.employee_id.name
			elif record.client_type == "Student":
				record.name = record.student_id.name
			else:
				record.name = record.visitor_name

	@api.onchange('client_type')
	def onchange_client_type(self):
		if self.client_type == "Student":
			self.employee_id = False
			self.visitor_name = ""
		elif self.client_type == "Employee":
			self.student_id = False
			self.visitor_name = ""
		else:
			self.employee_id = False
			self.student_id = False

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"








