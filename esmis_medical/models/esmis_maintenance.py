# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
# from datetime import date,datetime,timedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _



   
class EsmisProcedureType(models.Model):
	_name = "esmis.procedure.type"
	_description = "Procedure Type"

	name = fields.Char(string="Procedure Name", required=True)


class EsmisMedicalIllnes(models.Model):
	_name = "esmis.medical.illness"
	_description = "Medical Illness"

	name = fields.Char(string="Name", required=True)


class EsmisDentalComplaintType(models.Model):
	_name = "esmis.dental.complaint.type"
	_description = "Dental Complaint Type"

	name = fields.Char(string="Type", required=True)


class EsmisDentalProcedure(models.Model):
	_name = "esmis.dental.procedure"
	_description = "Dental Procedure"

	name = fields.Char(string="Procedure", required=True)


class EsmisMedicine(models.Model):
	_name = "esmis.medicine"
	_description = "Medicine"

	name = fields.Char(string="Medicine", required=True)
	price = fields.Float(string="Price", required=True)
	stock = fields.Integer(string="Stock")