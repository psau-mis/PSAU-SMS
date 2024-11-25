# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)


class eSMISEnrollment(models.Model):
	_inherit = "esmis.enrollment"

	fee_id = fields.Many2many("esmis.fees", compute="_compute_fee_id", store=True, string="Fee")
	fee_line_ids = fields.One2many("esmis.enrollment.fees", "enrollment_id")
	must_pay = fields.Boolean(default=False)
	cashier_rec_id = fields.Many2one("esmis.cashier")
	cashier_rec_status = fields.Selection(related="cashier_rec_id.status")
	cashier_line_ids = fields.One2many(related="cashier_rec_id.cashier_line_ids")
	total_fee = fields.Float(compute="_compute_total_fee")
	total_cashier_fee = fields.Float(string="Total Fees", compute="_compute_total_cashier_fee")
	total_cashier_total = fields.Float(string="Total", compute="_compute_total_cashier_total")
	total_discount = fields.Float(string="Total Discount", compute="_compute_total_discount")

	partial_paid_flag = fields.Boolean(compute="_compute_paid_flag")
	full_paid_flag = fields.Boolean(compute="_compute_paid_flag")

	total_fee_price = fields.Float(compute="_compute_total_fee")

	new_scholarship = fields.Many2one('esmis.scholarship.maintenance',string="Scholarship")
	new_scholar_code = fields.Char(string="Code", related="new_scholarship.code")
	new_scholar_provider = fields.Char(string="Provider", related="new_scholarship.provider")
	# financial_aid = fields.Float(string="Financial Aid")
	new_scholar_type = fields.Selection([('fixed', 'Fixed'),
										('percentage', 'Percentage')], string="Type")
	fix_amount = fields.Float(string="Amount")
	percent_amount = fields.Float(string="Percent")



	# @api.onchange('new_scholarship')
	# def ched_scholar(self):
	# 	# for rec in self:
		
			
	# 	if str(self.new_scholarship.scholarship_type).lower() == 'ched':
	# 		vals = []
	# 		self.new_scholar_type = 'percentage'
	# 		self.percent_amount = 1
			
	# 		for rec in self.fee_line_ids:
	# 			rec.write({'computed_aid': rec.amount*self.percent_amount})


	# def get_computed_aid(self):
	# 	for rec in self:
	# 		vals = []
	# 		for recs in rec.fee_line_ids:
	# 			computed_aid= recs.amount*rec.percent_amount
	# 			fee_val = {
	# 				"computed_aid": recs.amount*rec.percent_amount,
		
	# 			}
	# 			vals.append((Command.create(fee_val)))

	# 		rec.update({"fee_line_ids": vals})


	# @api.model
	def apply_scholar(self):

		feeline_sudo = self.env['esmis.enrollment.fees'].search([])
		# fee_lines = feeline_sudo.browse(selected_list)
		# raise ValidationError("Ads")
		amount_to_deduct = 0
		for line in feeline_sudo:
			# line.enrollment_id.write()
			# line.computed_aid = 1
			if line.checkbox_select == True:
				if line.enrollment_id.new_scholar_type == 'fixed':
					if line.enrollment_id.fix_amount - amount_to_deduct >= line.amount:
						line.computed_aid = line.amount
						amount_to_deduct += line.amount
					else:
						line.computed_aid = line.enrollment_id.fix_amount - amount_to_deduct
						amount_to_deduct += line.computed_aid

				else:
					line.computed_aid = line.amount*line.enrollment_id.percent_amount

		for line in feeline_sudo:
			line.checkbox_select = False


	@api.onchange('new_scholar_type')
	def onchange_scholar_type(self):
		for rec in self:
			if rec.new_scholar_type == 'fixed':
				rec.percent_amount = 0
			else:
				rec.fix_amount = 0
			

	def reset_scholar(self):
		for rec in self:
			rec.new_scholar_type = False
			rec.percent_amount = 0
			rec.fix_amount = 0
			for recs in rec.fee_line_ids:
				recs.aid = 0
				recs.computed_aid = 0
				recs.checkbox_select = False

	def select_all(self):
		for rec in self:
			for recs in rec.fee_line_ids:
				recs.checkbox_select = True

	def unselect_all(self):
		for rec in self:
			for recs in rec.fee_line_ids:
				recs.checkbox_select = False


	def _compute_paid_flag(self):
		for rec in self:
			total = 0
			for recs in rec.fee_line_ids:
				total = total + recs.amount_paid_copy
			if total > 0:
				rec.partial_paid_flag = True
			else:
				rec.partial_paid_flag = False

			
			if rec.total_fee <= 0:
				rec.full_paid_flag = True
				rec.partial_paid_flag = True
				# rec.partial_paid_flag = False
			else:
				rec.full_paid_flag = False

	def name_get(self):
		for rec in self:
			result = []

			enrollment_cashier_fees_name = "{}-{}".format(rec.enrollment_no or False, rec.school_year_id.name or False)
			result.append((rec.id, enrollment_cashier_fees_name))
			return result

	@api.depends("fee_line_ids")
	def _compute_total_discount(self):
		total_discount = 0
		if self.cashier_rec_id:
			for rec in self.cashier_rec_id.cashier_line_ids:
				total_discount += rec.discount

		self.total_discount = total_discount

	@api.depends("fee_line_ids")
	def _compute_total_fee(self):

		for rec in self:
			total_amount = 0
			total_amount_price = 0
			for record in rec.fee_line_ids:
				
				total_amount_price += record.amount
			rec.total_fee_price = total_amount_price

			for record in rec.fee_line_ids: 
			
				product_lines = []
				cashier_records = rec.env['esmis.cashier'].search([('student_id', '=', rec.student_id.id),('school_year_id', '=', rec.school_year_id.id),('status', '=', 'paid')])
				# rec.assessment_fee = [(4, enrollment.id) for enrollment in student_enrollment.fee_line_ids]
				# rec.student_image = student_enrollment.student_image
				if cashier_records:
					total_paid = 0
					for recs in cashier_records:
						total_paid = total_paid + recs.total_amount_paid

					percent_per_line = (record.amount/rec.total_fee_price)*100
					record.amount_paid_copy = total_paid*(percent_per_line/100)
				else:
					record.amount_paid_copy = 0

				total_amount += (record.amount - record.aid) - record.amount_paid_copy
		
			rec.total_fee = total_amount
		

	@api.depends("cashier_line_ids")
	def _compute_total_cashier_fee(self):
		total_cashier_fee = 0
		for rec in self.cashier_line_ids:
			total_cashier_fee += rec.fee_amount

		self.total_cashier_fee = total_cashier_fee

	@api.depends("cashier_line_ids")
	def _compute_total_cashier_total(self):
		total_cashier_total = 0
		for rec in self.cashier_line_ids:
			total_cashier_total += rec.total

		self.total_cashier_total = total_cashier_total

	@api.depends("course_id", "year_level")
	def _compute_fee_id(self):
		vals = []
		self.fee_id = None
		self.fee_line_ids = None
		for rec in self:
			course_fees = self.env['esmis.course.year.level'].search([('course_id', '=', self.course_id.id),('year_level','=',self.year_level)])
			
			if course_fees:
				for record in course_fees:
					fees_setup_id = self.env['esmis.fees'].search([('id', '=', record.fee_id.id),('state', '=', 'active')])
					if fees_setup_id:
						vals.append(fees_setup_id.id)

					rec.fee_id = vals
					rec.fee_line_ids = None
					rec.assess_fees()


	def assess_fees(self):
		for rec in self:
			if rec.fee_id:
				vals = []
				for recs in rec.fee_id:
					for fees in recs.line_ids:
						fee_val = {
							"enrollment_id": rec.id,
							"sequence": fees.sequence,
							"fee_id": fees.fee_id.id,
							"name": fees.coa_fee_id.id,
							"amount": fees.amount

						}
						vals.append((Command.create(fee_val)))

				rec.update({"fee_line_ids": vals})

	def post_fees(self):
		for rec in self:
			admission_id = rec.env['esmis.admission'].search([('id','=', rec.admission_id.id)])
			student_id = rec.env['res.partner'].search([('student_no_grad','=', admission_id.student_no_grad),('student_no_undg','=', admission_id.student_no_undg)])
			val = []
			for records in rec.course_id.fee_id:
				val.append(records.id)
			vals = {
				"student_id": student_id.id,
				"school_year_id": rec.school_year_id.id,
				"transaction_type": [(6, 0, val)]
			}
			cashier_rec_id = self.env["esmis.cashier"].create(vals)
			rec.cashier_rec_id = cashier_rec_id.id
			fees = []
			for fee in rec.fee_line_ids:
				fee_vals = {
					"fee_id": fee.name.id,
					"fee_amount": fee.amount
				}
				if not rec.must_pay:
					fee_vals.update({"discount": fee.amount})

				fees.append((Command.create(fee_vals)))

			cashier_rec_id.update({"cashier_line_ids": fees})
			if not rec.must_pay:
				cashier_rec_id.on_submit()
				cashier_rec_id.on_validate()
				cashier_rec_id.on_paid()

	def on_validate(self):
		for rec in self:
			if len(self.fee_line_ids) <= 0:
			
				raise ValidationError("The selected program has no fees. Go to Fees setup to configure.")
			for recs in rec.fee_line_ids:
				recs.aid = recs.computed_aid
			rec.status = "validate"
			rec.validate_by_id = self.env.user.id
			rec.validate_datetime = fields.datetime.now()
			
		

	def set_as_free(self):
		if self.fee_line_ids:
			for rec in self.fee_line_ids:
				rec.amount = 0

	# def check_if_scholar(self):

	# 	for recs in self:
			
	# 		student_ledger_id = self.env['esmis.student.ledger'].search([('student_id', '=', recs.student_id.id)])
	# 		if student_ledger_id:
	# 			# if recs.total == student_ledger_id.balance:
	# 			student_ledger_id.write({
	# 		    'student_ledger_lines': [(0,0,{
	# 									'school_year_id':recs.school_year_id.id,
	# 									'trans_date':datetime.today(),	
	# 									'credit':recs.total_fee
				
	# 									}
	# 								)],
	# 							})
	# 			# if recs.total > (student_ledger_id.balance + recs.total_amount_paid):
	# 				# raise ValidationError(recs.tota + " - " (student_ledger_id.balance + recs.total_amount_paid))
	# 			student_ledger_id.write({
	# 		    'student_ledger_lines': [(0,0,{
	# 									'school_year_id':recs.school_year_id.id,
	# 									'trans_date':datetime.today(),
	# 									'debit':recs.total_fee
									
	# 									}
	# 								)],
	# 							})

	# 		else:
	# 			vals = {
	# 				'student_id': recs.student_id.id,
	# 				# 'school_year_id': recs.school_year_id.id,
	# 				# 'cashier_id': recs.id,
	# 				'student_ledger_lines':[(0,0,{
	# 										'school_year_id':recs.school_year_id.id,
	# 										'trans_date':datetime.today(),
	# 										'credit':recs.total_fee

	# 										}
	# 									)],
	# 					}
	# 			self.env['esmis.student.ledger'].sudo().create(vals)

	# 			student_ledger_id = self.env['esmis.student.ledger'].search([('student_id', '=', recs.student_id.id)])
	# 			student_ledger_id.write({
	# 			    'student_ledger_lines': [(0,0,{
	# 										'school_year_id':recs.school_year_id.id,
	# 										'trans_date':datetime.today(),
	# 										'debit': recs.total_fee

	# 										}
	# 									)],
	# 								})	

	def check_if_scholar(self):

		for recs in self:
			vals = {}
			
			student_ledger_id = self.env['esmis.student.ledger'].search([('student_id', '=', recs.student_id.id)])
			if student_ledger_id:
				pass
			else:
				vals = {
					'student_id': recs.student_id.id,
					# 'school_year_id': recs.school_year_id.id,
					# 'cashier_id': recs.id,
					
						}
				self.env['esmis.student.ledger'].sudo().create(vals)

			
				# if recs.total == student_ledger_id.balance:
			vals = {
				'student_id': recs.student_id.id,
				'school_year_id': recs.school_year_id.id,
				'status': 'paid',
				'active': False,

				# 'cashier_line_ids':[(0,0,{
				# 						'fee_id':rec.name.id,
				# 						'fee_amount':rec.amount,
				# 						'amount_paid':rec.amount,

				# 						}
				# 					)],
					}
			self.env['esmis.cashier'].sudo().create(vals)
			student_cashier_id = self.env['esmis.cashier'].search([('student_id', '=', recs.student_id.id), ('school_year_id', '=', recs.school_year_id.id), ('active', '=', False)])
			total_amount_paid = 0
			for rec in recs.fee_line_ids:
				total_amount_paid += rec.amount
				student_cashier_id.write({
					'cashier_line_ids':[(0,0,{
										'fee_id':rec.name.id,
										'fee_amount':rec.amount,
										'amount_paid':rec.amount,

										}
									)],
					'total_amount_paid':total_amount_paid,

								})
	def check_if_new_scholar(self):

		for recs in self:
			vals = {}
			
			student_ledger_id = self.env['esmis.student.ledger'].search([('student_id', '=', recs.student_id.id)])
			if student_ledger_id:
				pass
			else:
				vals = {
					'student_id': recs.student_id.id,
					# 'school_year_id': recs.school_year_id.id,
					# 'cashier_id': recs.id,
					
						}
				self.env['esmis.student.ledger'].sudo().create(vals)

			
				# if recs.total == student_ledger_id.balance:
			vals = {
				'student_id': recs.student_id.id,
				'school_year_id': recs.school_year_id.id,
				'status': 'paid',
				'active': False,

				# 'cashier_line_ids':[(0,0,{
				# 						'fee_id':rec.name.id,
				# 						'fee_amount':rec.amount,
				# 						'amount_paid':rec.amount,

				# 						}
				# 					)],
					}
			self.env['esmis.cashier'].sudo().create(vals)
			student_cashier_id = self.env['esmis.cashier'].search([('student_id', '=', recs.student_id.id), ('school_year_id', '=', recs.school_year_id.id), ('active', '=', False)])
			total_amount_paid = 0
			for rec in recs.fee_line_ids:
				total_amount_paid += rec.aid
				student_cashier_id.write({
					'cashier_line_ids':[(0,0,{
										'fee_id':rec.name.id,
										'fee_amount':rec.amount,
										'amount_paid':rec.aid,

										}
									)],
					'total_amount_paid':total_amount_paid,

								})
			



	def on_enrolled(self):
		enrollment = super(eSMISEnrollment, self).on_enrolled()
		if self.scholar1:
			self.check_if_scholar()
		if self.new_scholarship:
			self.check_if_new_scholar()

				
		return enrollment



class eSMISEnrollmentFees(models.Model):
	_name = "esmis.enrollment.fees"
	_description = "Enrollment Fees"
	_order = "sequence asc"
	_inherit = ["mail.thread", "mail.activity.mixin"]


	enrollment_id = fields.Many2one("esmis.enrollment")
	sequence = fields.Integer()
	fee_id = fields.Many2one("esmis.fees")
	name = fields.Many2one("esmis.coa")
	amount = fields.Float()
	amount_paid = fields.Float()
	amount_paid_copy = fields.Float(compute="_compute_amount_paid")
	aid = fields.Float(string="Aid")
	computed_aid = fields.Float(string="Computed Aid")

	checkbox_select = fields.Boolean()


	def get_computed_aid(self):
		for rec in self:
			rec.computed_aid = rec.amount*rec.enrollment_id.percent_amount


	def reset_scholar(self):
		for rec in self:
			rec.enrollment_id.new_scholar_type = False
			rec.enrollment_id.percent_amount = 0
			rec.enrollment_id.fix_amount = 0

	def _compute_amount_paid(self):
		for rec in self:
			rec.amount_paid_copy = 0

		for rec in self:
			for record in rec.enrollment_id: 
			
				product_lines = []
				cashier_records = rec.env['esmis.cashier'].search([('student_id', '=', record.student_id.id),('school_year_id', '=', record.school_year_id.id),('status', '=', 'paid')])
				# rec.assessment_fee = [(4, enrollment.id) for enrollment in student_enrollment.fee_line_ids]
				# rec.student_image = student_enrollment.student_image
				if cashier_records:
					# total_paid = 0
					# for recs in cashier_records:
					# 	total_paid = total_paid + recs.total_amount_paid

					# percent_per_line = (rec.amount/record.total_fee_price)*100
					# rec.amount_paid_copy = total_paid*(percent_per_line/100)

					for recs in cashier_records:
						for records in recs.cashier_line_ids:
							if rec.name == records.fee_id:
								rec.amount_paid_copy = rec.amount_paid_copy + records.amount_paid
							# else:
							# 	rec.amount_paid_copy = 0
				else:
					rec.amount_paid_copy = 0




			
