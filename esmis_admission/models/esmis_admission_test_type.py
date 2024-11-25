from odoo import api, fields, models, tools, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError, UserError


class StudenAdmissionTestType(models.Model):
	_name = 'esmis.admission.test.type'
	_description = "Admission Test Interpretation"

	name = fields.Char(string="Name", required=True)
	active = fields.Boolean(default=True)
	admission_test_type_line_ids = fields.One2many('esmis.admission.test.type.line', 'admission_test_type_id')

	def get_stanine_from_score(self, score):
		test_type_line_id = self.admission_test_type_line_ids.filtered(lambda line: line.score_from <= score
				and line.score_to >= score)
		if test_type_line_id:
			for test in test_type_line_id:
				return test.stanine, dict(self.env['esmis.admission.test.type.line']._fields['interpretation'].selection).get(test.interpretation)
		return 0, 'invalid'

	def check_test_type_score_range(self):
		score_list = []
		for rec in self.admission_test_type_line_ids:
			for sc in range(rec.score_from, rec.score_to + 1):
				score_list.append(sc)

			test_type_with_stanine = self.admission_test_type_line_ids.filtered(lambda line: line.stanine == rec.stanine)
			if len(test_type_with_stanine) > 1:
				raise ValidationError(_('Repeating stanine is not allowed.'))

		if len(score_list) != len(set(score_list)):
			raise ValidationError(_('Repeating score is not allowed.'))


class StudenAdmissionTestTypeLine(models.Model):
	_name = 'esmis.admission.test.type.line'

	name = fields.Char(string="Name")
	score_from = fields.Integer(string="From", required=True)
	score_to = fields.Integer(string="To", required=True)
	stanine = fields.Integer(string="Stanine", required=True)
	interpretation = fields.Selection([('below_average', 'Below Average'), ('average', 'Average'), ('above_average', 'Above Average')], string="Interpretation", required=True)
	admission_test_type_id = fields.Many2one('esmis.admission.test.type', string="Admission Test Type")

	@api.model
	def create(self, vals):
		"""
			extends default create function
			set field name value
			return dict
		"""
		name = vals.get('name', False)
		if name == False:
			vals['name'] = "Stanine %s from score %s - %s" %( vals.get('stanine'), vals.get('score_from'), vals.get('score_to') )
		res = super(StudenAdmissionTestTypeLine, self.sudo()).create(vals)
		return res

	@api.constrains('score_to', 'score_from', 'stanine')
	def constrainst_score_and_stanine(self):
		self.admission_test_type_id.check_test_type_score_range()
		if self.score_from > self.score_to:
			raise ValidationError(_('Score From must not be greater than Score To'))
