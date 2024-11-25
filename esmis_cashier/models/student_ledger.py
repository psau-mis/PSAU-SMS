# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)



class eSMISStudentLedger(models.Model):
	_name = "esmis.student.ledger"
	_rec_name = "student_id"

	student_id = fields.Many2one('res.partner', string="Student", domain="[('is_student','=',True)]")
	school_year_id = fields.Many2one("esmis.school.year")
	student_ledger_lines = fields.One2many('esmis.student.ledger.line', 'student_ledger_id')
	cashier_id = fields.Many2one('esmis.cashier')

	balance = fields.Float(compute="_compute_balance")

	student_ledger_lines_copy = fields.Many2many('esmis.student.ledger.line.copy', compute="_get_debit_from_cashier", string="Student Ledger Lines")
	

	@api.depends("student_ledger_lines.debit", "student_ledger_lines.credit")
	def _compute_balance(self):
		for rec in self:
			balance = 0
			if rec.student_ledger_lines:
				for line in rec.student_ledger_lines_copy:
					balance += line.debit - line.credit

			rec.balance = balance

	def _get_debit_from_cashier(self):

		for rec in self:
			
			cashier_lines = []
			student_cashier = rec.env['esmis.cashier'].search([('student_id', '=', rec.student_id.id),('status','=', 'paid'),'|',('active','=', False),('active','=', True)], order="id asc")
			# rec.assessment_fee = [(4, enrollment.id) for enrollment in student_enrollment.fee_line_ids]
			

			sy = 0
			ctr = 0
			for recs in student_cashier:
				if ctr == 0:
					enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', recs.student_id.id),('status', 'in', ('validate', 'enrolled')),('school_year_id','=',recs.school_year_id.id),('full_paid_flag','=',False),('partial_paid_flag','=',True),('scholar1','=',False)], limit=1)
					total_amount = 0
					for fees in enrollment_id.fee_line_ids:
						total_amount = total_amount + fees.amount
					ctr += 1
					cashier_lines.append((0,0, {
							'student_ledger_id': rec.id,
							'school_year_id': recs.school_year_id.id,
							'ref_no': recs.id,
							'debit': total_amount
						
						}))
					cashier_lines.append((0,0, {
							'student_ledger_id': rec.id,
							'school_year_id': recs.school_year_id.id,
							'ref_no': recs.id,
							'credit': recs.total_amount_paid
						
						}))
					sy = recs.school_year_id

				else:
					if sy == recs.school_year_id:
						cashier_lines.append((0,0, {
								'student_ledger_id': rec.id,
								'school_year_id': recs.school_year_id.id,
								'ref_no': recs.id,
								'credit': recs.total_amount_paid
							
							}))
						sy = recs.school_year_id
					else:
						cashier_lines.append((0,0, {
							'student_ledger_id': rec.id,
							'school_year_id': recs.school_year_id.id,
							'ref_no': recs.id,
							'debit': recs.total
						
							}))
						cashier_lines.append((0,0, {
								'student_ledger_id': rec.id,
								'school_year_id': recs.school_year_id.id,
								'ref_no': recs.id,
								'credit': recs.total_amount_paid
							
							}))
						sy = recs.school_year_id
			
			

			rec.student_ledger_lines_copy = cashier_lines
			# rec.student_ledger_lines_copy = [(6, 0, admission) for admission in cashier_lines]

class eSMISStudentLedgerLine(models.Model):
	_name = "esmis.student.ledger.line"
	# _rec_name = "name"

	student_ledger_id = fields.Many2one('esmis.student.ledger')
	school_year_id = fields.Many2one("esmis.school.year")
	trans_date = fields.Date(string="Transaction Date", default=datetime.today())
	code = fields.Char(string="Code")
	ref_no = fields.Char(string="Ref #")
	debit = fields.Float(string="Debit")
	credit = fields.Float(string="Credit")
	balance = fields.Float(string="Balance", compute="_compute_balance")
	remarks = fields.Text(string="Remarks")
	posted = fields.Boolean(string="Posted")
	date_posted = fields.Date(string="Date Posted")

	# @api.depends("debit", "credit")
	def _compute_balance(self):
		remaining_balance = 0
		ctr = 0
		for rec in self:
			if ctr == 0:
				remaining_balance = rec.debit - rec.credit
				rec.balance = remaining_balance
				ctr+=1
			else:
				# remaining_balance = rec.debit - rec.credit - (-remaining_balance)
				remaining_balance = float(format(rec.debit, ".2f")) - float(format(rec.credit, ".2f")) - (-float(format(remaining_balance, ".2f")))
				rec.balance = remaining_balance

class eSMISStudentLedgerLineCopy(models.Model):
	_name = "esmis.student.ledger.line.copy"
	# _rec_name = "name"

	student_ledger_id = fields.Many2one('esmis.student.ledger')
	school_year_id = fields.Many2one("esmis.school.year")
	trans_date = fields.Date(string="Transaction Date", default=datetime.today())
	code = fields.Char(string="Code")
	ref_no = fields.Char(string="Ref #")
	debit = fields.Float(string="Debit")
	credit = fields.Float(string="Credit")
	balance = fields.Float(string="Balance", compute="_compute_balance")
	remarks = fields.Text(string="Remarks")
	posted = fields.Boolean(string="Posted")
	date_posted = fields.Date(string="Date Posted")

	student_id = fields.Many2one('res.partner', string="Student", related='student_ledger_id.student_id', store=True)


	# @api.depends("debit", "credit")
	def _compute_balance(self):
		remaining_balance = 0
		ctr = 0
		sy = 0
		for rec in self:
			if ctr == 0:
				remaining_balance = rec.debit - rec.credit
				rec.balance = remaining_balance
				ctr+=1
				sy = rec.school_year_id.id
			else:
				if sy == rec.school_year_id.id:
					remaining_balance = float(format(rec.debit, ".2f")) - float(format(rec.credit, ".2f")) - (-float(format(remaining_balance, ".2f")))
					remaining_balance = remaining_balance - float(format(rec.debit, ".2f"))
					rec.balance = remaining_balance
					sy = rec.school_year_id.id
				else:
					# remaining_balance = rec.debit - rec.credit - (-remaining_balance)
					remaining_balance = float(format(rec.debit, ".2f")) - float(format(rec.credit, ".2f")) - (-float(format(remaining_balance, ".2f")))
					rec.balance = remaining_balance
					sy = rec.school_year_id.id
