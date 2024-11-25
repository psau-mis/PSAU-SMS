from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta
import uuid


class AdmissionDocumenttoResendWiz(models.TransientModel):
	_name = 'esmis.admission.document.to.resend.wiz'

	admission_id = fields.Many2one("esmis.admission", string="Admissions", required=True)
	tor = fields.Boolean(string='TOR (Transcript of Records)')
	tor_bachelor = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records)")
	tor_master = fields.Boolean(string="TOR Masters' Degree (Transcript of Records)")
	tor_current_master = fields.Boolean(string="TOR Current Masters' Program (Transcript of Records)")
	tor_current_doctor = fields.Boolean(string="TOR Current Doctors' Program (Transcript of Records)")
	birth_cert = fields.Boolean(string='PSA-issued Birth Certificate')
	employ_cert = fields.Boolean(string='Certificate of Employment')
	honorable_dismissal = fields.Boolean(string='Honorable Dismissal')
	shs_report_card = fields.Boolean(string='Senior Highschool Report Card')
	gmc_cert = fields.Boolean(string='Certificate of Good Moral Character')
	stud_personal_statement = fields.Boolean(string='Student Personal History Statement')
	passport_bio = fields.Boolean(string='Passport Bio Page')
	birth_cert_foreign = fields.Boolean(string='Birth Certificate')
	english_cert = fields.Boolean(string='Certificate of English Proficiency')
	police_clearance = fields.Boolean(string='Police Clearance (Philippines NBI)')
	admission_type = fields.Selection([('freshmen', 'New Student'), ('transferee', 'Transferee'), ('continuing', 'Second Courser'),
		('foreign', 'Foreign Applicant'), ('graduate', 'Graduate Level: Masteral (New Student)'), ('transferee2', 'Graduate Level: Masteral (Transferee)'),
		('graduate2', 'Graduate Level: Doctoral (New Student)'), ('transferee3', 'Graduate Level: Doctoral (Transferee)')], string="Admission Type", required=True)


	def set_admission_document_to_resend(self):
		max_due_days = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.requirements_submission_due')
		if not max_due_days:
			max_due_days = 1
		admission_update = {
			'admission_uuid': uuid.uuid4(),
			'state': 'need_to_resubmit',
			'url_validity': datetime.today() + timedelta(days=int(max_due_days)),
			}
		if self.admission_id.admission_uuid:
			admission_update.update({'admission_redirection_ids': [(0, 0, {'name': self.admission_id.admission_uuid, 'admission_id': self.admission_id.id})],})
		search = ""
		for key in [
			#'form_138',
			'tor',
			'tor_bachelor',
			'tor_master',
			'tor_current_master',
			'tor_current_doctor',
			'birth_cert',
			'employ_cert',
			'honorable_dismissal',
			'shs_report_card',
			'gmc_cert',
			'stud_personal_statement',
			'passport_bio',
			'birth_cert_foreign',
			'english_cert',
			'police_clearance',
		]:
			if eval('self.'+key):
				admission_update['resend_%s' % key] = True
			else:
				admission_update['resend_%s' % key] = False
		self.admission_id.write(admission_update)
		mail_ids = self.admission_id.send_mail_with_template('esmis_website_admission.esmis_admission_application_documents_to_resend_email_template', {'reupload':search})
		message = "Action Successfully executed..."
		
		if not mail_ids:
			message = "Unable to send email, please enable email sender or send the email manually."
			
		return {
			"type": "ir.actions.client",
			"tag": "display_notification",
			"params": {
				"title": _("Document to Resend"),
				"message": message,
				"sticky": False,
				"type": "info",
				"next": {
					"type": "ir.actions.act_window_close",
				},
			},
		}
