from odoo import api, fields, models, tools, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError, UserError


class GradeEquivalent(models.Model):
	_name = 'esmis.grade.eq'
	_description = "Grade Equivalent"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	name = fields.Char(string="Name", required=True)
	is_active = fields.Boolean(default=False)
	grade_eq_line_ids = fields.One2many('esmis.grade.eq.line', 'grade_eq_id')

	def get_eq_from_grade(self, grade):
		test_type_line_id = self.grade_eq_line_ids.filtered(lambda line: line.grade_from <= grade
				and line.grade_to >= grade)
		if test_type_line_id:
			for test in test_type_line_id:
				return test.grade_equivalent
		return 0

	def check_grade_range(self):
		grade_list = []
		for rec in self.grade_eq_line_ids:
			for sc in range(rec.grade_from, rec.grade_to + 1):
				grade_list.append(sc)

			test_type_with_stanine = self.grade_eq_line_ids.filtered(lambda line: line.grade_equivalent == rec.grade_equivalent)
			if len(test_type_with_stanine) > 1:
				raise ValidationError(_('Repeating grade equivalent is not allowed.'))

		if len(grade_list) != len(set(grade_list)):
			raise ValidationError(_('Repeating grade is not allowed.'))

	# @api.constrains('is_active')
	# def _make_false_other_rule_state(self):
	# 	if self.is_active:
	# 		rules=self.env['esmis.grade.eq'].search([('id', '!=', self.id),('is_active','=',True)])
	# 		# raise ValidationError(rules.id)
	# 		for rule in rules:
	# 			rule.is_active=False
	# 			# raise ValidationError("as")
	# 			return {
	# 				'type': 'ir.actions.client',
	# 				'tag': 'reload',
	# 			}

	@api.constrains('is_active')
	def _make_false_other_rule_state(self):
		# if self.is_active:
		for rec in self:
			rules=self.env['esmis.grade.eq'].search([('is_active','=',True)])
			if len(rules)>=2:
				raise ValidationError("Only one active grade equivalent is allowed.")
		

	

class GradeEquivalentLine(models.Model):
	_name = 'esmis.grade.eq.line'

	name = fields.Char(string="Name")
	grade_from = fields.Integer(string="From", required=True)
	grade_to = fields.Integer(string="To", required=True)
	# stanine = fields.Integer(string="Stanine", required=True)
	grade_equivalent = fields.Selection([('1.00', '1.00'), 
									('1.25', '1.25'), 
									('1.50', '1.50'),
									('1.75', '1.75'),
									('2.00', '2.00'),
									('2.25', '2.25'),
									('2.50', '2.50'),
									('2.75', '2.75'),
									('3.00', '3.00'),
									('5.00', '5.00')], string="Grade Equivalent", required=True)
	grade_eq_id = fields.Many2one('esmis.grade.eq', string="Grade Equivalent")

	@api.model
	def create(self, vals):
		"""
			extends default create function
			set field name value
			return dict
		"""
		name = vals.get('name', False)
		if name == False:
			vals['name'] = "Grade Equivalent %s from grade %s - %s" %( vals.get('stanine'), vals.get('grade_from'), vals.get('grade_to') )
		res = super(GradeEquivalentLine, self.sudo()).create(vals)
		return res

	@api.constrains('grade_to', 'grade_from', 'grade_equivalent')
	def constrainst_grade_and_grade_equivalent(self):
		self.grade_eq_id.check_grade_range()
		if self.grade_from > self.grade_to:
			raise ValidationError(_('Grade From must not be greater than Grade To'))
