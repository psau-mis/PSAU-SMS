from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EnrollmentSendEmailWiz(models.TransientModel):
	_name = 'esmis.enrollment.send.email.wiz'

	@api.model
	def default_get(self, fields):
		res = super(EnrollmentSendEmailWiz, self).default_get(fields)
		cancelled_auto_send_email = self.env['ir.config_parameter'].get_param('esmis_enrollment.enrollment_disable_sending_of_email')
		# raise UserError(cancelled_auto_send_email)
		if not cancelled_auto_send_email:
			raise UserError(_("You cannot send email if auto sending of email is active."))
		if self.env.context.get("active_ids"):
			enrollment_ids = self.env["esmis.enrollment"].search(
				[
					("id", "in", self.env.context.get("active_ids")),
				]
			)
			if enrollment_ids:
				res["enrollment_ids"] = enrollment_ids
			else:
				raise UserError(_("There are no selected Enrollment!"))
			return res
		else:
			raise UserError(_("There are no selected Enrollment!"))

	enrollment_ids = fields.Many2many("esmis.enrollment", string="Enrollment")


	def send_email(self):
		for rec in self.enrollment_ids:
			ctr = 0
			enrollment_ids = self.env['esmis.enrollment'].search([('student_id','=', rec.student_id.id)])
			for rec in enrollment_ids:
				ctr+=1

			if rec.status == 'enrolled':
				if ctr>1:
					try:
						rec.send_mail_with_template('esmis_enrollment.enrollment_notice_mail_old_student')
					except Exception as e:
						pass
				else:
					try:
						rec.send_mail_with_template('esmis_enrollment.enrollment_notice_mail')
					except Exception as e:
						pass
		return False

	def open_wizard(self):

		return {
			"name": "Email Sending",
			"view_mode": "form",
			"res_model": "esmis.enrollment.send.email.wiz",
			"view_id": self.env.ref(
				"esmis_enrollment.esmis_enrollment_send_email_wiz_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			"context": self.env.context,
		}
