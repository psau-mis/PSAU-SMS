# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisDentalCertificate(models.Model):
	_name = "esmis.dental.certificate"
	_description = "Dental Certificate"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),
								('Validated', 'Validated'),
								('Printed', 'Printed'),
								('Cancelled', 'Cancelled')],'Status', default="Draft")

	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]")

	certificate_date = fields.Date(string="Certificate Date", default=datetime.today())
	
	diagnosis = fields.Text()
	is_recommendation = fields.Boolean(string="Is Recommendation")
	is_rendered = fields.Boolean(string="Is Rendered")
	recommendation_rendered = fields.Text(string="Recommendation/Rendered")
	medical_history = fields.Text()
	patient_is = fields.Selection([('Fit to Work', 'Fit to Work'), 
									('Not Fit to Work', 'Not Fit to Work'), 
									('Fit to Work if finished with recommended treatment', 'Fit to Work if finished with recommended treatment')],
									 'Patient Is')
	certified_by = fields.Many2one('hr.employee', string="Certified By", required=True)
	certificate_purpose = fields.Text(string="Certificate Purpose")

	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"


