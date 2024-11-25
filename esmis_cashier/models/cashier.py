# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,UserError,Warning

_logger = logging.getLogger(__name__)


class eSMISCashier(models.Model):
	_name = "esmis.cashier"
	_description = "Cashier"
	_order = "id desc"
	_inherit = ["mail.thread", "mail.activity.mixin"]
	_rec_name = 'or_no'

	def _default_or_no(self):
		latest_or_no = self.env["esmis.cashier.or"].search([], order='name desc')
		if latest_or_no:
			# Get only the first in recordset
			or_no = latest_or_no[0].name
			or_no = str(int(or_no) + 1)
			return or_no
		else:
			return ""

	def _default_or_no_1(self):
		or_no = "103"
		cashier_ids = self.env["esmis.cashier"].search([])
		for recs in cashier_ids:

			# or_no = "104"
			# if recs.or_no:
			# 	# raise ValidationError("Asd")
			# 	or_no = "104"
			# else:
			# raise ValidationError("Asdasdasd")
			latest_or_no = self.env["esmis.cashier"].search([], order='or_no asc')
			# raise ValidationError(str(latest_or_no.or_no))
			ctr = 1
			or_list = []
			for rec in latest_or_no:
				if rec.or_no:
					or_list.append(int(rec.or_no))
			or_list.sort()
			# raise ValidationError(str(or_list))

			for rec in or_list:
				if rec:
					if int(rec) <= ctr:
						ctr+=1

					else:
						# recs.or_no = str(ctr)
						sequence_id = self.env['ir.sequence'].search([('code', '=', 'esmis.cashier.or')])
						sequence_id.number_next_actual = ctr
						# recs.or_no = self.env['ir.sequence'].next_by_code('esmis.cashier.or')
						or_no =  self.env['ir.sequence'].next_by_code('esmis.cashier.or')
							# raise ValidationError(or_no)
		return or_no


	@api.model
	def _default_currency(self):
		return self.env.user.company_id.currency_id

	currency_id = fields.Many2one('res.currency', string='Currency', default=_default_currency,track_visibility='always')

	name = fields.Char(default=lambda self: _('New'), string="Invoice #")
	or_no = fields.Char(string="O.R. #", default=_default_or_no_1)
	or_date = fields.Datetime(default=fields.Datetime.now())
	or_date_mode = fields.Selection([("server", "Server Time"),
									 ("manual", "Set Manually")], default="server")
	or_id = fields.Many2one("esmis.cashier.or", string="O.R. #")
	invoice_date = fields.Date(default=fields.Date.today())
	cashier_line_ids = fields.One2many("esmis.cashier.line", "cashier_id")
	transaction_mode = fields.Selection([("student", "Student"),
										 ("other_payer", "Other Payer")
										 ], default="student")
	status = fields.Selection([("draft", "Draft"),	   
							   ("paid", "Paid"),
							   ("voided", "Voided")], default="draft")
	sub_total = fields.Float(compute="_compute_subtotal", store=True, string="Subtotal")
	total = fields.Float(compute="_compute_total", store=True)
	total_amount_paid = fields.Float()
	total_discount = fields.Float(compute="_compute_discount", store=True, string="Discount")
	student_id = fields.Many2one("res.partner", domain="[('is_student','=',True)]")
	school_year_id = fields.Many2one("esmis.school.year")
	campus = fields.Many2one("esmis.campus")
	transaction_type = fields.Many2many("esmis.fees")
	payment_enrollment = fields.Float()
	payment_midterm = fields.Float()
	payment_prefinal = fields.Float()
	cashier_payment_ids = fields.One2many("esmis.cashier.payment", "cashier_id")

	enrollment_id = fields.Many2one('esmis.enrollment')
	total_flag = fields.Boolean(default=False, compute="compute_total_flag")

	active = fields.Boolean(default=True)

	other_payer_name = fields.Char(string="Name")
	payer_name = fields.Char(string="Name", compute="_get_name")

	def _get_name(self):
		for rec in self:
			if rec.transaction_mode == 'student':
				rec.payer_name = rec.student_id.full_name
			else:
				rec.payer_name = rec.other_payer_name



	# @api.onchange('cashier_line_ids.fees_id')
	# def _filter_fees(self):
	# 	fee_ids = []
	# 	for rec in seld.cashier_line_ids:
	# 		fee_ids = rec.fees_id
		
	# 	fees_list = []
	# 	fees_id = self.env['esmis.coa'].search([('id', 'not in', fee_ids)])
	# 	if fees_id:
	# 		for fee in fees_id:
	# 			fees_list.append(fee.id)
	# 		if fees_list:
	# 			domain =[('id', 'in', fees_list)]
	# 			return domain
	# 		return domain



	def unlink(self):
		for rec in self:
			if rec.active == False:
				raise UserError(_("You are not allowed to delete this record"))
			else:
				cashier_id = self.env['esmis.cashier'].search([('student_id', '=', self.student_id.id),('school_year_id', '=', self.school_year_id.id),('status', '=', 'paid')])
				if len(cashier_id) == 1:
					enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', self.student_id.id),('school_year_id', '=', self.school_year_id.id),('status', '=', 'enrolled')])
					if enrollment_id:
						for recstat in enrollment_id:
							recstat.status = 'validate'
		return super(eSMISCashier, self).unlink()

	def on_void(self):
		for rec in self:
			if rec.active == False:
				raise UserError(_("You are not allowed to void this record"))
			else:
				cashier_id = self.env['esmis.cashier'].search([('student_id', '=', self.student_id.id),('school_year_id', '=', self.school_year_id.id),('status', '=', 'paid')])
				if len(cashier_id) == 1:
					enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', self.student_id.id),('school_year_id', '=', self.school_year_id.id),('status', '=', 'enrolled')])
					if enrollment_id:
						for recstat in enrollment_id:
							recstat.status = 'validate'
			rec.status = "voided"

	def compute_total_flag(self):
		for rec in self:
			if rec.total <= 0:
				rec.total_flag = True
			else:
				rec.total_flag = False


	@api.onchange("student_id", 'school_year_id')
	def _onchange_school_year_id(self):
		for rec in self:
			rec.cashier_line_ids = None
			if rec.school_year_id:
				enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', rec.student_id.id),('status', 'in', ('validate', 'enrolled')),('school_year_id','=',rec.school_year_id.id),('full_paid_flag','=',False),('partial_paid_flag','=',True),('scholar1','=',False)], limit=1)
				# enrollment = rec.school_year_id
				# if enrollment.must_pay:
				vals = []
				total_amount = 0
				for fees in enrollment_id.fee_line_ids:
					total_amount = total_amount + fees.amount

				if total_amount > 0:
					

					for fees in enrollment_id.fee_line_ids:
						if enrollment_id.scholar1:
							fee_val = {
								"sequence": fees.sequence,
								"fee_id": fees.name,
								"fee_amount": 0

							}
						else:
							fee_val = {
								"sequence": fees.sequence,
								"fee_id": fees.name,
								"fee_amount": (fees.amount - fees.aid) - fees.amount_paid_copy

							}
						vals.append((Command.create(fee_val)))

				rec.enrollment_id = enrollment_id
				rec.update({"cashier_line_ids": vals})

	@api.depends("invoice_date", "student_id")
	def _compute_name(self):
		for rec in self:
			rec.name = self.env['ir.sequence'].next_by_code('esmis.cashier')


	@api.depends("cashier_line_ids.fee_amount")
	def _compute_subtotal(self):
		for rec in self:
			sub_total = 0
			if rec.cashier_line_ids:
				for line in rec.cashier_line_ids:
					sub_total += line.fee_amount

			rec.sub_total = sub_total

	# @api.depends("cashier_line_ids.fee_amount")
	# def _compute_total_amount_paid(self):
	# 	for rec in self:
	# 		total = 0
	# 		if rec.cashier_line_ids:
	# 			for line in rec.cashier_line_ids:
	# 				total += line.amount_paid

	# 		rec.total_amount_paid = total

	@api.depends("cashier_line_ids.fee_amount")
	def _compute_total(self):
		for rec in self:
			total = 0
			if rec.cashier_line_ids:
				for line in rec.cashier_line_ids:
					total += line.total

			rec.total = total

	@api.depends("cashier_line_ids.fee_amount")
	def _compute_discount(self):
		for rec in self:
			total_discount = 0
			if rec.cashier_line_ids:
				for line in rec.cashier_line_ids:
					total_discount += line.discount

			rec.total_discount = total_discount

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'esmis.cashier') or _('New')
		res = super(eSMISCashier, self).create(vals)
		for rec in res.enrollment_id:
			rec.cashier_rec_id = res.id

		return res

	
	

	def on_validate(self):
		for rec in self:
			rec.status = "validated"

	def on_paid(self):
		# for rec in self:
		# 	rec.status = "paid"
		view = self.env.ref("esmis_cashier.esmis_mode_of_payment_form_view")
		wiz = self.env["esmis.mode.of.payment"].create({"cashier_id": self.id, "amount_paid": self.total, "transaction_mode": self.transaction_mode})
		return {
			"name": _("Mode of Payment"),
			"type": "ir.actions.act_window",
			"view_type": "form",
			"view_mode": "form",
			"res_model": "esmis.mode.of.payment",
			"views": [(view.id, "form")],
			"view_id": view.id,
			"target": "new",
			"res_id": wiz.id,
			"context": self.env.context,
		}

	def view_info(self):
		# for rec in self:
		# 	rec.status = "paid"
		view = self.id
		# wiz = self.env["esmis.mode.of.payment"].create({"cashier_id": self.id, "amount_paid": self.total, "transaction_mode": self.transaction_mode})
		wiz = self.env["esmis.mode.of.payment"].search([('cashier_id', '=', self.id)], limit=1)
		return {
			"name": _("Mode of Payment"),
			"type": "ir.actions.act_window",
			"view_type": "form",
			"view_mode": "form",
			"res_model": "esmis.mode.of.payment",
			"view_id": self.env.ref("esmis_cashier.esmis_mode_of_payment_form_view_1").id,
			"target": "new",
			"res_id": wiz.id,
			"context": self.env.context,
	
		}




	def on_cancelled(self):
		for rec in self:
			rec.status = "cancelled"

	def get_fees(self):
		for rec in self:
			if rec.transaction_type:
				vals = []
				for fees in rec.transaction_type.line_ids:
					fee_val = {
						"fee_id": fees.name.id,
						"fee_amount": fees.amount - fees.amount_paid

					}
					vals.append((Command.create(fee_val))[::-1])

				rec.update({"cashier_line_ids": vals})

	def set_as_free(self):
		if self.cashier_line_ids:
			for rec in self.cashier_line_ids:
				rec.fee_amount = 0

	def open_set_or_wizard(self):
		view = self.env.ref("esmis_cashier.esmis_set_or_wizard_form_view")
		wiz = self.env["esmis.set.or.wizard"].create({"name": self.or_no, "cashier_id": self.id})
		return {
			"name": _("OR Number set-up"),
			"type": "ir.actions.act_window",
			"view_type": "form",
			"view_mode": "form",
			"res_model": "esmis.set.or.wizard",
			"views": [(view.id, "form")],
			"view_id": view.id,
			"target": "new",
			"res_id": wiz.id,
			"context": self.env.context,
		}

	# def open_mop_wizard(self):
	# 	view = self.env.ref("esmis_cashier.esmis_mode_of_payment_form_view")
	# 	wiz = self.env["esmis.set.or.wizard"].create()
	# 	return {
	# 		"name": _("OR Number set-up"),
	# 		"type": "ir.actions.act_window",
	# 		"view_type": "form",
	# 		"view_mode": "form",
	# 		"res_model": "esmis.mode.of.payment",
	# 		"views": [(view.id, "form")], q
	# 		"view_id": view.id,
	# 		"target": "new",
	# 		"res_id": wiz.id,
	# 		"context": self.env.context,
	# 	}


class eSMISCashierPayment(models.Model):
	_name = "esmis.cashier.payment"
	_description = "Cashier Payment"
	_order = "id desc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	name = fields.Char()
	amount_paid = fields.Float()
	or_no = fields.Char(string="O.R. #")
	payment_datetime = fields.Datetime("Date Paid")
	cashier_id = fields.Many2one("esmis.cashier")

class eSMISORNumbers(models.Model):
	_name = "esmis.cashier.or"
	_description = "Cashier OR"
	_order = "id asc"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	name = fields.Integer(string="O.R. #")
	or_date = fields.Datetime(default=fields.Datetime.now())
