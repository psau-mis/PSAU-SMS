# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisDentalRecord(models.Model):
	_name = "esmis.dental"
	_description = "Dental record"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	is_outsider = fields.Boolean(string='Is Outsider')
	is_student = fields.Boolean(readonly=True, related="client_id.is_student")
	examine_date = fields.Date(string="Examine Date", default=datetime.today())

	# basic info
	employee_type = fields.Selection([('Faculty', 'Faculty'),('Administration', 'Administration')],'Employee Type', default="Faculty")
	office_college = fields.Many2one('esmis.department', string="Office College")

	course = fields.Many2one('esmis.course', string="Course")
	year = fields.Integer(string="Year")

	last_name = fields.Char(string="Last Name")
	first_name = fields.Char(string="First Name")
	name_extension = fields.Char(string="Name Extension")
	middle_name = fields.Char(string="Middle Name")
	email_address = fields.Char(string="Email Address")
	complete_address = fields.Char(string="Complete Address")
	person_emergency = fields.Char(string="Person to be notified in case of emergency")
	person_emergency_number = fields.Char(string="Contact Number")
	civil_status = fields.Selection([('Single', 'Single'),('Married', 'Married'),('Widow/er', 'Widow/er')],'Civil Status', default="Single")
	age = fields.Integer(string="Age")
	birth_date = fields.Date(string="Birthday", default=datetime.today())
	gender = fields.Selection([('Male', 'Male'),('Female', 'Female')],'Gender', default="Male")
	contact_number = fields.Char(string="Contact Number")

	# dental rec
	dental_assessment = fields.Text(string="Dental Assessment")
	past_procedures = fields.Many2many('esmis.dental.procedure', string="Past Procedures")
	date_last_visit = fields.Date(string="Date of last dental visit", default=datetime.today())
	previous_complications = fields.Text(string="Previous complications after dental treatment/s")
	past_complaints = fields.Many2many('esmis.dental.complaint.type', string="Past Complaints")

	treatment_ids= fields.One2many('esmis.dental.line', 'dental_id')

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"



class EsmisDentalRecordLine(models.Model):
	_name = "esmis.dental.line"
	_description = "Dental Record Line"


	dental_id = fields.Many2one('esmis.dental')
	treatment_date = fields.Date(string="Date of last dental visit", default=datetime.today())
	intra_extra_oral_examination = fields.Text(string="Intra Extra Oral Examination")
	assessment_treatment_plan = fields.Text(string="Assessment/Treatment Plan")
	services_rendered = fields.Many2many('esmis.dental.procedure', string="Services Rendered")
	amount_paid = fields.Float(string="Amount Paid")
	sales_invoice = fields.Char(string="Sale Invoice")
	sales_invoice_type = fields.Selection([('Cash', 'Cash'),('Credit', 'Credit')],'SI Type', default="Cash")