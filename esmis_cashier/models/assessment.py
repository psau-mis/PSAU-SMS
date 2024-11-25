# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)



class eSMISStudentAssessment(models.Model):
	_name = "esmis.student.assessment"
	# _rec_name = "name"

	student_id = fields.Many2one('res.partner', string="Student", domain="[('is_student','=',True)]")
	school_year_id = fields.Many2one("esmis.school.year")
	assessment_fee_line = fields.One2many('esmis.student.assessment.line', 'assessment_id', string="Assessment")
	student_image = fields.Binary("Student Image")
	
	assessment_fee = fields.Many2many('esmis.enrollment.fees', string="Assessment")

	net_amount = fields.Float(compute="_compute_total")
	total_payment = fields.Float(compute="_compute_total_payment")
	sy_balance = fields.Float(compute="_compute_sy_balance")
	outstanding_balance = fields.Float(compute="_compute_outstanding_balance")



	new_scholarship = fields.Many2one('esmis.scholarship.maintenance',string="Scholarship")
	new_scholar_code = fields.Char(string="Code", related="new_scholarship.code")
	new_scholar_provider = fields.Char(string="Provider", related="new_scholarship.provider")
	# financial_aid = fields.Float(string="Financial Aid")
	new_scholar_type = fields.Selection([('fixed', 'Fixed'),
										('percentage', 'Percentage')], string="Type")
	fix_amount = fields.Float(string="Amount")
	percent_amount = fields.Float(string="Percent")

	# @api.model
	def apply_scholar(self):

		# feeline_sudo = self.env['esmis.enrollment.fees'].search([])
		# fee_lines = feeline_sudo.browse(selected_list)
		# raise ValidationError("Ads")
		enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', self.student_id.id),('school_year_id', '=', self.school_year_id.id), ('status', 'in', ('enrolled', 'validate'))], limit=1)
		amount_to_deduct = 0

		enrollment_id.new_scholarship = self.new_scholarship
		enrollment_id.new_scholar_code = self.new_scholar_code
		enrollment_id.new_scholar_provider = self.new_scholar_provider
		enrollment_id.new_scholar_type = self.new_scholar_type
		enrollment_id.fix_amount = self.fix_amount
		enrollment_id.percent_amount = self.percent_amount


		for line in self.assessment_fee_line:
			# line.enrollment_id.write()
			# line.computed_aid = 1
			if line.checkbox_select == True:
				if self.new_scholar_type == 'fixed':
					if self.fix_amount - amount_to_deduct >= line.amount:
						line.financial_aid = line.amount
						amount_to_deduct += line.amount

					else:
						line.financial_aid = self.fix_amount - amount_to_deduct
						amount_to_deduct += line.financial_aid

					for rec in enrollment_id.fee_line_ids:
						if line.fee_id == rec.name:
							rec.aid = line.financial_aid

				else:
					line.financial_aid = line.amount*self.percent_amount
					for rec in enrollment_id.fee_line_ids:
						if line.fee_id == rec.name:
							rec.aid = line.financial_aid

		for line in self.assessment_fee_line:
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
			for recs in rec.assessment_fee_line:
				recs.financial_aid = 0
				recs.checkbox_select = False
			enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', self.student_id.id),('school_year_id', '=', self.school_year_id.id), ('status', 'in', ('enrolled', 'validate'))], limit=1)
			for line in rec.assessment_fee_line:
				for recs in enrollment_id.fee_line_ids:
					if line.fee_id == recs.name:
						recs.aid = 0
	def select_all(self):
		for rec in self:
			vals=[]
			for recs in rec.assessment_fee_line:
				recs.checkbox_select = True

	def unselect_all(self):
		for rec in self:
			for recs in rec.assessment_fee_line:
				recs.checkbox_select = False

	@api.depends('student_id', 'school_year_id')
	def _compute_total(self):
		for rec in self:
			total = 0
			if rec.assessment_fee_line:
				for line in rec.assessment_fee_line:
					total += line.net_assess

			rec.net_amount = total

	@api.depends('student_id', 'school_year_id')
	def _compute_total_payment(self):
		for rec in self:
			total = 0
			if rec.assessment_fee_line:
				for line in rec.assessment_fee_line:
					total += line.actual_payment

			rec.total_payment = total

	@api.depends('student_id', 'school_year_id')
	def _compute_sy_balance(self):
		for rec in self:
			total = 0
			if rec.assessment_fee_line:
				for line in rec.assessment_fee_line:
					total += line.balance

			rec.sy_balance = total

	@api.depends('student_id')
	def _compute_outstanding_balance(self):
		for rec in self:
			student_enrollment = rec.env['esmis.enrollment'].search([('student_id', '=', rec.student_id.id),('status', 'in', ('enrolled', 'validate'))])
			total = 0
			if student_enrollment:
				for recs in student_enrollment:
					total += recs.total_fee
		

			rec.outstanding_balance = total

	@api.onchange("student_id", "school_year_id")
	def _compute_assessment_fee(self):
		for rec in self:
			rec.assessment_fee_line = None
			if rec.school_year_id:
				enrollment_id = self.env['esmis.enrollment'].search([('student_id', '=', rec.student_id.id),('school_year_id', '=', rec.school_year_id.id), ('status', 'in', ('enrolled', 'validate'))], limit=1)
				# enrollment = rec.school_year_id
				# if enrollment.must_pay:
				vals = []
				total_amount = 0
				for fees in enrollment_id.fee_line_ids:
					total_amount = total_amount + fees.amount

				

				for recs in enrollment_id.fee_line_ids:
					if enrollment_id.scholar1:
						fee_val = {
							'fee_id': recs.name.id,
							'fee_code': recs.name.code,
							'amount': recs.amount,
							'financial_aid': recs.amount,
							'net_assess': 0,
							'actual_payment':recs.amount,
							'credit_memo':0,
							'debit_refund':0,
							'balance':recs.amount - recs.amount,
							'remarks':"",

						}
					else:
						fee_val = {
							'fee_id': recs.name.id,
							'fee_code': recs.name.code,
							'amount': recs.amount,
							'financial_aid': recs.aid,
							'net_assess': recs.amount - recs.aid,
							'actual_payment':recs.amount_paid_copy,
							'credit_memo':0,
							'debit_refund':0,
							'balance':(recs.amount - recs.aid) - recs.amount_paid_copy,
							'remarks':"",

						}
					vals.append((Command.create(fee_val)))

				# rec.enrollment_id = enrollment_id
				rec.update({"assessment_fee_line": vals})


	@api.model
	def create(self, vals):
		
		res = super(eSMISStudentAssessment, self).create(vals)
		

		return res


class eSMISStudentAssessmentLine(models.Model):
	_name = "esmis.student.assessment.line"

	assessment_id = fields.Many2one('esmis.student.assessment')
	fee_id = fields.Many2one('esmis.coa')
	fee_code = fields.Char(string="Code")
	amount = fields.Float()
	financial_aid = fields.Float()
	net_assess = fields.Float()
	actual_payment = fields.Float()
	credit_memo = fields.Float()
	debit_refund = fields.Float()
	balance = fields.Float()
	remarks = fields.Text()

	checkbox_select = fields.Boolean()
	