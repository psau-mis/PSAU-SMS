# Part of eSMIS App. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import datetime

_logger = logging.getLogger(__name__)


class eSMISMOP(models.Model):
	_name = "esmis.mode.of.payment"
	# _description = "Set OR Wizard"

	cashier_id = fields.Many2one("esmis.cashier", store=True)
	mode_of_payment = fields.Selection([("cash", "Cash"),
									 ("bank", "Bank"),
									 ("check", "Check")], default="cash", store=True)
	bank_account_number = fields.Char(string="Account Number", store=True)
	bank_mode = fields.Selection([("1", "Inter-Fund Transfer",),
									 ("2", "Credit Memo")], string="Bank Mode", store=True)
	bank_branch = fields.Char(string="Bank Branch")

	amount_paid = fields.Float(string="Amount", store=True)
	paid_date = fields.Datetime(default=fields.Datetime.now(), store=True)
	transaction_mode = fields.Selection([("student", "Student"),
									 ("other_payer", "Other Payer")
									 ], default="student", store=True)
	check_number = fields.Char(string="Check Number", store=True)

	view_ctr = fields.Boolean()


	@api.constrains('amount_paid')
	def restrict_amount_paid(self):
		if self.amount_paid > self.cashier_id.total:
			raise UserError("Input amount should not be higher than total")

		

	def set_paid(self):
		for rec in self:
			if rec.amount_paid <= 0:
				raise UserError("Input amount should be higher than 0")

			if rec.cashier_id.transaction_mode == 'student':
				for recs in rec.cashier_id:
					total = recs.total
					if rec.amount_paid >= recs.total:
						for cashier_line in recs.cashier_line_ids:
							cashier_line.amount_paid = cashier_line.total
					else:
						amount_given = rec.amount_paid
						for cashier_line in recs.cashier_line_ids:
						# 	if cashier_line.total >= recs.total:
						# 		cashier_line.amount_paid = recs.total
							# else:
							# 	cashier_line.amount_paid = recs.total_amount_paid
							# 	total = total - cashier_line.total
							# percent_per_line = (cashier_line.total/recs.total)*100
							# cashier_line.amount_paid = rec.amount_paid*(percent_per_line/100)
							

							amount_given = amount_given - cashier_line.total
							if amount_given >= 0:
								cashier_line.amount_paid = cashier_line.total
							else:
								cashier_line.amount_paid = amount_given + cashier_line.total
								break

					recs.total_amount_paid = rec.amount_paid

					enrollment_id = self.env['esmis.enrollment'].search([('id','=', recs.enrollment_id.id)])
					if enrollment_id:
						for cashier_line in recs.cashier_line_ids:
							for enrollment_id_line in enrollment_id.fee_line_ids:
								if cashier_line.fee_id == enrollment_id_line.name:
									enrollment_id_line.amount_paid = enrollment_id_line.amount_paid + cashier_line.amount_paid

						# enrollment_id.paid_flag = True


					student_ledger_id = self.env['esmis.student.ledger'].search([('student_id', '=', recs.student_id.id)], limit=1)
					if student_ledger_id:
						# if recs.total == student_ledger_id.balance:
						student_ledger_line_id = self.env['esmis.student.ledger.line'].search([('student_ledger_id', '=', student_ledger_id.id),('school_year_id','=',recs.school_year_id.id)])
						if student_ledger_line_id:
							pass
						# 	total_credit_per_sem = 0
						# 	total_debit_per_sem = 0
						# 	for creds in student_ledger_line_id:
						# 		total_credit_per_sem = total_credit_per_sem + creds.credit
						# 		total_debit_per_sem = total_debit_per_sem + creds.debit
						# 	if float(format(recs.total, ".2f")) > float(format(total_debit_per_sem - total_credit_per_sem, ".2f")):
						# 		# raise UserError(str(recs.total) + " - " + str(total_debit_per_sem)+" - " + str(total_credit_per_sem))
								
								
						# 		student_ledger_id.write({
						# 		'student_ledger_lines': [(0,0,{
						# 								'school_year_id':recs.school_year_id.id,
						# 								'trans_date':datetime.today(),
						# 								'debit':recs.total
													
						# 								}
						# 							)],
						# 						})
							

						# 	student_ledger_id.write({
						# 	'student_ledger_lines': [(0,0,{
						# 							'school_year_id':recs.school_year_id.id,
						# 							'trans_date':datetime.today(),	
						# 							'credit':recs.total_amount_paid
							
						# 							}
						# 						)],
						# 					})
						# else:
						# 	student_ledger_id.write({
						# 		'student_ledger_lines': [(0,0,{
						# 								'school_year_id':recs.school_year_id.id,
						# 								'trans_date':datetime.today(),
						# 								'debit':recs.total
													
						# 								}
						# 							)],
						# 						})
							

						# 	student_ledger_id.write({
						# 	'student_ledger_lines': [(0,0,{
						# 							'school_year_id':recs.school_year_id.id,
						# 							'trans_date':datetime.today(),	
						# 							'credit':recs.total_amount_paid
							
						# 							}
						# 						)],
						# 					})
						

					else:
						vals = {
							'student_id': recs.student_id.id,
							'school_year_id': recs.school_year_id.id,
							# 'cashier_id': recs.id,
							# 'student_ledger_lines':[(0,0,{

							# 						'school_year_id':recs.school_year_id.id,
							# 						'trans_date':datetime.today(),
							# 						'debit': recs.total
													

							# 						}
							# 					)],
								}
						self.env['esmis.student.ledger'].sudo().create(vals)

						student_ledger_id = self.env['esmis.student.ledger'].search([('student_id', '=', recs.student_id.id)])
						student_ledger_id.write({
							'student_ledger_lines': [(0,0,{
													'school_year_id':recs.school_year_id.id,
													'trans_date':datetime.today(),
													'credit':recs.total_amount_paid

													}
												)],
											})	
			else:
				for recs in rec.cashier_id:
					recs.total_amount_paid = rec.amount_paid

			for recs in rec.cashier_id:
				for recs_to_del in recs.cashier_line_ids:
					# raise UserError("Asd")
					if recs_to_del.amount_paid == 0:
						recs_to_del.unlink()
			rec.cashier_id.status = 'paid'
			# rec.cashier_id._default_or_no_1()
			# rec.cashier_id.or_no = self.env['ir.sequence'].next_by_code('esmis.cashier.or')

			# else:
			# 	raise UserError("Asd")
