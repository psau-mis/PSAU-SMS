from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SendEmailWiz(models.TransientModel):
	_name = 'esmis.send.email.wiz'

	@api.model
	def default_get(self, fields):
		res = super(SendEmailWiz, self).default_get(fields)
		cancelled_auto_send_email = self.env['ir.config_parameter'].get_param('esmis_admission.disable_sending_of_email')
		if not cancelled_auto_send_email:
			raise UserError(_("You cannot send bulk email if auto sending of email is active."))
		if self.env.context.get("active_ids"):
			admission_ids = self.env["esmis.admission"].search(
				[
					("id", "in", self.env.context.get("active_ids")),
				]
			)
			if admission_ids:
				res["admission_ids"] = admission_ids
			else:
				raise UserError(_("There are no selected Admissions!"))
			return res
		else:
			raise UserError(_("There are no selected Admissions!"))

	admission_ids = fields.Many2many("esmis.admission", string="Admissions")
	admission_on_save_mail = fields.Boolean(string="Admission Notice")
	test_sched_notification = fields.Boolean(string="Entrance Test Notice")
	admission_test_result_mail = fields.Boolean(string="Admission Test Results")

	def send_email(self):
		for rec in self.admission_ids:
			if self.admission_on_save_mail:
				try:
					rec.send_mail_with_template('esmis_admission.admission_on_save_mail', bulk=True)
				except Exception as e:
					pass
			if self.test_sched_notification:
				try:
					rec.send_mail_with_template('esmis_admission.test_sched_notification', bulk=True)
				except Exception as e:
					pass
			if self.admission_test_result_mail:
				try:
					rec.send_mail_with_template('esmis_admission.admission_test_result_mail', bulk=True)
				except Exception as e:
					pass
		return False

	def open_wizard(self):

		return {
			"name": "Email Sending",
			"view_mode": "form",
			"res_model": "esmis.send.email.wiz",
			"view_id": self.env.ref(
				"esmis_admission.esmis_send_email_wiz_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			"context": self.env.context,
		}
