# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisMedicalHealthRecord(models.Model):
	_name = "esmis.medical.health.record"
	_description = "Health Record"
	_rec_name = 'client_id'

	state = fields.Selection([('Draft', 'Draft'),('Validated', 'Validated'),('Printed', 'Printed'),('Cancelled', 'Cancelled')],'Status', default="Draft")
	client_id = fields.Many2one('res.partner', string="Client Name", domain="['|',('is_student', '=', True),('is_employee', '=', True)]", required=True)
	consented_medical_treatment = fields.Boolean(string="Consented for Medical Treatment")
	consented_medications = fields.Boolean(string="Consented for Medication")

	# covid vax
	covid_vac_ids = fields.Many2many('esmis.medical.covid.vaccination', string="Covid Vaccination", compute="_compute_covid_vax")

	# basic info
	birthdate = fields.Date(string="Date of Birth", default=datetime.today(), related="client_id.birthdate")
	gender = fields.Selection([('Male', 'Male'),('Female', 'Female')], string="Gender", related="client_id.gender")
	mobile = fields.Char(string="Contact No.", related="client_id.mobile_number")
	nationality = fields.Char(string="Nationality", related="client_id.nationality")
	religion = fields.Char(string="Religon", related="client_id.religion")

	# emergency info
	contact_person_emergency = fields.Char(string="Name")
	contact_person_emergency_contact = fields.Char(string="Contact Number")
	contact_person_emergency_address = fields.Text(string="Complete Address")
	contact_person_emergency_relation = fields.Char(string="Relation to Client")

	hospital_choice = fields.Char(string="Hospital")
	hospital_choice_address = fields.Text(string="Address")
	doctor_choice = fields.Char(string="Doctor to be informed")
	doctor_contact = fields.Char(string="Contact Number")

	# family history
	family_history_ids = fields.One2many('esmis.medical.family.history', 'medical_health_record_id')

	# medical history
	medical_history_ids = fields.One2many('esmis.medical.history', 'medical_health_record_id')

	# obstetrical history
	fmp = fields.Integer(string="Age first menstruated")
	lmp = fields.Char(string="Day last menstruated")
	dysmenorrhea = fields.Boolean(string="Dysmenorrhea")
	regular_cycle = fields.Boolean(string="Regular Cycle")
	obstetrical_index = fields.Char(string="Obstetrical Index")
	normal_spontaneous_delivery = fields.Boolean(string="Normal Spontaneous Delivery")
	delivery_how_many_times = fields.Integer(string="How many times")
	caesarian_section = fields.Boolean(string="Caesarain Section")
	caesarian_how_many_times = fields.Integer(string="How many times")
	caesarian_reason = fields.Char(string="Why")

	# for male only	
	circumcision = fields.Boolean(string="Circumcision")

	# psychosocial history
	smoker = fields.Boolean(string="Smoker")
	smoker_sticks_per_day = fields.Integer(string="Sticks per day")
	alcoholic_beverage_drinker = fields.Boolean(string="Alcoholic Beverage Drinker")
	alcoholic_bottles = fields.Integer(string="Bottles per occasion")



	def on_validate(self):
		self.state = "Validated"

	def on_print(self):
		self.state = "Printed"

	def on_cancel(self):
		self.state = "Cancelled"

	def _compute_covid_vax(self):
		for rec in self:
			covid_vax = rec.env['esmis.medical.covid.vaccination'].search([('client_id', '=', rec.client_id.id)])
			rec.covid_vac_ids = [(4, covid_vax.id) for recs in covid_vax]




class EsmisMedicalFamilyHistory(models.Model):
	_name = "esmis.medical.family.history"
	# _description = "PSAU Clearance"

	medical_health_record_id = fields.Many2one('esmis.medical.health.record')
	illness_id = fields.Many2one('esmis.medical.illness')
	relation_to_client = fields.Char(string="Relation to Client")

class EsmisMedicalHistory(models.Model):
	_name = "esmis.medical.history"
	# _description = "PSAU Clearance"

	medical_health_record_id = fields.Many2one('esmis.medical.health.record')
	illness_id = fields.Many2one('esmis.medical.illness')




