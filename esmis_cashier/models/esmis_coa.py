# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)


class eSMISCOA(models.Model):
	_name = "esmis.coa"
	_rec_name = "name"

	account_id = fields.Char(string="Account Code")
	code = fields.Char(string=" Parent Code")
	parent_code = fields.Many2one('esmis.coa', string=" Parent Code")
	name = fields.Char(string="Name")
	amount = fields.Float(string="Amount")
	short_name = fields.Char(string="Short Name")
	fund_group = fields.Many2one('esmis.fees.fund', string="Fund Group")
	classification = fields.Char(string="Classification")
	type_coa = fields.Selection([("Asset", "Asset"),
								("Income", "Income"),
								("Liabilities", "Liabilities"),
								("Revenue", "Revenue"),
								("Expense", "Expense")], string="Type")


class eSMISCOA1(models.Model):
	_name = "esmis.coa.main"
	_rec_name = "name"

	account_id = fields.Char(string="Account Code")
	code = fields.Char(string="Parent Code")
	name = fields.Char(string="Name")
	short_name = fields.Char(string="Short Name")
	fund_group = fields.Many2one('esmis.fees.fund', string="Fund Group")
	classification = fields.Char(string="Classification")
	type_coa = fields.Selection([("Income", "Income"),
								("Liability", "Liability"),
								("Expense", "Expense")], string="Type")