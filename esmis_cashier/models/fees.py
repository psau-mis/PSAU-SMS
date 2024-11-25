# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISFees(models.Model):
	_name = "esmis.fees"
	_description = "Fees"
	_order = "id desc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	name = fields.Char('Fee')
	course_ids = fields.Many2many('esmis.course')
	line_ids = fields.One2many("esmis.fees.lines", "fee_id")
	school_year_id = fields.Many2one('esmis.school.year', string="School Year", domain="[('state','=','Active')]")
	state = fields.Selection([('new', 'Draft'),
							  ('active', 'Active'),
							  ('inactive', 'Inactive'),
							  ('cancel', 'Cancelled')], "Status", required=True, default='new')

	course_year_level = fields.One2many('esmis.course.year.level',"fee_id")

	def unlink(self):
		for rec in self:
			external_identifier = self.env["ir.model.data"].search(
				[("res_id", "=", rec.id), ("model", "=", "esmis.fees")]
			)
			if external_identifier and external_identifier.name:
				raise ValidationError(_("Can't delete default Fees"))
			return super(eSMISFees, self).unlink()

	def on_active(self):
		self.state = "active"

	def on_inactive(self):
		self.state = "inactive"

	def on_cancel(self):
		self.state = "cancel"



class eSMISFeesLines(models.Model):
	_name = "esmis.fees.lines"
	_description = "Fees Lines"
	_order = "sequence asc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	sequence = fields.Integer()
	fee_id = fields.Many2one("esmis.fees")
	coa_fee_id = fields.Many2one("esmis.coa", string="Fees")
	coa_fee_code = fields.Char(string="Code", related="coa_fee_id.code")
	amount = fields.Float()

	# @api.onchange("coa_fee_id")
	# def _name_onchange(self):
	#     for rec in self:
	#         rec.amount = rec.coa_fee_id.amount




class eSMISFeesTypes(models.Model):
	_name = "esmis.fees.types"
	_description = "Fees Types"
	_order = "id asc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	code = fields.Char("Code")
	fund_code = fields.Many2one("esmis.fees.fund")
	name = fields.Char("Fee Type")
	amount = fields.Float(default=0)


class eSMISFeesFund(models.Model):
	_name = "esmis.fees.fund"
	_description = "Fees Fund"
	_order = "id asc"

	name = fields.Char("Fund Code")
	description = fields.Char("Description")
	# fees_type_ids = fields.One2many("esmis.coa", "fund_code")
	# fees_coa = fields.One2many

class eSMISFeesCourseYearLevel(models.Model):
	_name = "esmis.course.year.level"
	_description = "Fees Course Year Level"
	_order = "id asc"

	fee_id = fields.Many2one("esmis.fees")
	course_id = fields.Many2one('esmis.course', string="Course")
	year_level = fields.Selection([("1st", "1st Year"),
						 ("2nd", "2nd Year"),
						 ("3rd", "3rd Year"),
						 ("4th", "4th Year"),
						 ("5th", "5th Year"),
						 ("6th", "6th Year"),
						 ("7th", "7th Year"),
						 ("8th", "8th Year"),
						 ("9th", "9th Year")], required=True)