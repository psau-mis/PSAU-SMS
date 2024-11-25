# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisDentalRecommendation(models.Model):
	_name = "esmis.dental.recommendation"
	_description = "Dental Recommendation"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	recommendation_date = fields.Date(string="Date", default=datetime.today())
	line_ids = fields.One2many('esmis.dental.recommendation.line', 'dental_rec_id')


	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"



class EsmisDentalRecommendationLine(models.Model):
	_name = "esmis.dental.recommendation.line"
	_description = "Close Contact 1A Line"


	dental_rec_id = fields.Many2one('esmis.dental.recommendation')
	procedure_id = fields.Many2one('esmis.dental.procedure', string="Recommended Treatment")
	tooth_remarks = fields.Text(string="Tooth No./Remarks")