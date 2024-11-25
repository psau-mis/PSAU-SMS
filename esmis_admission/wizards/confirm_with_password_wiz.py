from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class ConfirmWithPasswordWiz(models.TransientModel):
	_name = 'esmis.confirm.with.password.wiz'

	"""
		pass context
		with_action = callable function on string format
		admission_id = id of the admission where the action will be executed
	"""

	admission_id = fields.Many2one("esmis.admission", string="Admissions")
	password = fields.Char(string="Password", required=True)

	def confirm_admission(self):
		self.env.user._check_credentials(self.password, {'interactive': True})
		action = self._context.get('with_action', False)
		if action:
			return self.admission_id.confirmation_action(action)
