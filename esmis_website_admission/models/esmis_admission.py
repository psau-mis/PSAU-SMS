from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import uuid


class eSMISAdmission(models.Model):
	_inherit = 'esmis.admission'

	admitted_applicant_response = fields.Selection([('accepted', 'Accepted'), ('declined', 'Declined')], string="Admitted Applicat Response")
	barangay_id = fields.Many2one('res.barangay', string="Barangay")

	resend_tor = fields.Boolean(string='TOR (Transcript of Records)')
	resend_tor_bachelor = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records)")
	resend_tor_master = fields.Boolean(string="TOR Masters' Degree (Transcript of Records)")
	resend_tor_current_master = fields.Boolean(string="TOR Current Masters' Program (Transcript of Records)")
	resend_tor_current_doctor = fields.Boolean(string="TOR Current Doctors' Program (Transcript of Records)")
	resend_birth_cert = fields.Boolean(string='PSA-issued Birth Certificate')
	resend_employ_cert = fields.Boolean(string='Certificate of Employment')
	resend_honorable_dismissal = fields.Boolean(string='Honorable Dismissal')
	resend_shs_report_card = fields.Boolean(string='Senior Highschool Report Card')
	resend_gmc_cert = fields.Boolean(string='Certificate of Good Moral Character')
	resend_stud_personal_statement = fields.Boolean(string='Student Personal History Statement')
	resend_passport_bio = fields.Boolean(string='Passport Bio Page')
	resend_birth_cert_foreign = fields.Boolean(string='Birth Certificate')
	resend_english_cert = fields.Boolean(string='Certificate of English Proficiency')
	resend_police_clearance = fields.Boolean(string='Police Clearance (Philippines NBI)')
	admission_redirection_ids = fields.One2many('esmis.admission.redirection.line', 'admission_id', string="Redirections")
	url_validity = fields.Date()
	medical_cert_url_uuid = fields.Char(string="Medical Certificate URL UUID")


	@api.model
	def check_exist(self, last_name ,first_name, middle_name, suffix, birthdate, admission_type_1):
		search = [('last_name','=', last_name), ('first_name','=', first_name), ('birthdate', '=', birthdate), ('admission_type_1','=', admission_type_1)]
		if middle_name:
			search.append(('middle_name', '=', middle_name))
		if suffix:
			search.append(('suffix', '=', suffix))
		admission = self.search(search)
		if len(admission):
			return True
		return False

	def _get_admission_create_student_values(self):
		rec = super(eSMISAdmission, self.sudo())._get_admission_create_student_values()
		rec['barangay_id'] = self.barangay_id.id
		return rec

	def send_application_documents_to_resend_mail(self):
		""" confirm documents to reupload email sender """

		return {
			"name": "Select Document to Resubmit",
			"view_mode": "form",
			"res_model": "esmis.admission.document.to.resend.wiz",
			"view_id": self.env.ref(
				"esmis_website_admission.esmis_admission_document_to_resend_wizard_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			'context': {
				'default_admission_id': self.id,
				'default_admission_type': self.admission_type,
			},
		}

	def evaluate_qualified_test(self):
		self.send_mail_with_template('esmis_website_admission.admission_admitted_second_or_third_choice_mail')

	def evaluate_qualified(self):
		super(eSMISAdmission, self.sudo()).evaluate_qualified()
		for rec in self:
			if rec.active_course_id.id == rec.course1_id.id:
				rec.send_mail_with_template('esmis_website_admission.admission_admitted_first_choice_mail')
			else:
				rec.send_mail_with_template('esmis_website_admission.admission_admitted_second_or_third_choice_mail')

	def evaluate_qualified_email_only(self):
		for rec in self:
			if rec.active_course_id.id == rec.course1_id.id:
				resp = rec.send_mail_with_template('esmis_website_admission.admission_admitted_first_choice_mail', bulk=True)
			else:
				resp = rec.send_mail_with_template('esmis_website_admission.admission_admitted_second_or_third_choice_mail', bulk=True)

	def admission_admit(self):
		super(eSMISAdmission, self.sudo()).admission_admit()
		for rec in self:
			rec.write({
				'medical_cert_url_uuid': uuid.uuid4(),
				})
			rec.send_mail_with_template('esmis_website_admission.esmis_admission_application_med_cert_upload_email_template')

	@api.onchange('state_id')
	def _state_id_on_change(self):
		if self.state_id:
			self.update({'city_id': False, 'barangay_id': False, 'zip': False, })
			return {'domain':{'city_id': [('state_id', '=', self.state_id.id)]}}

	@api.onchange('city_id')
	def _city_id_on_change(self):
		if self.city_id:
			self.zip = self.city_id.zipcode
			return {'domain':{'barangay_id': [('city_id', '=', self.city_id.id)]}}

	@api.model
	def _expire_resubmission_url(self):
		admission_ids = self.search([('url_validity', '=', datetime.today().date())])
		for rec in admission_ids:
			rec.update({'admission_uuid': False})


class eSMISAdmissionNotQualifiedWiz(models.TransientModel):
	_inherit = 'esmis.admission.not.qualified.wiz'

	def save_admission(self):
		res = super(eSMISAdmissionNotQualifiedWiz, self.sudo()).save_admission()
		if not self.active_course_id:
			self.admission_id.send_mail_with_template('esmis_website_admission.admission_not_admitted_mail')
		return res

class SendEmailWiz(models.TransientModel):
	_inherit = 'esmis.send.email.wiz'

	evaluation = fields.Selection([('evaluate_qualified', 'Qualified Notification'),
		('evaluate_not_qualified', 'Not Qualified Notification')], string="Qualification Notification")
	reupload_document = fields.Boolean(string="Reupload Document Notification")
	medcert_upload = fields.Boolean(string="Medical Certificate Upload")

	def send_email(self):
		res = super(SendEmailWiz, self.sudo()).send_email()
		max_due_days = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.requirements_submission_due')
		if not max_due_days:
			max_due_days = 1
		for rec in self.admission_ids:
			if self.evaluation:
				if self.evaluation == 'evaluate_qualified':
					rec.evaluate_qualified_email_only()
				else:
					if rec.state == 'not_qualified':
						rec.send_mail_with_template('esmis_website_admission.admission_not_admitted_mail', bulk=True)
			if self.reupload_document and rec.state == 'need_to_resubmit':
				rec.write({'url_validity': datetime.today() + timedelta(days=int(max_due_days))})
				rec.send_mail_with_template('esmis_website_admission.esmis_admission_application_documents_to_resend_email_template', bulk=True)
			if self.medcert_upload:
				rec.write({
					'medical_cert_url_uuid': uuid.uuid4(),
					})
				rec.send_mail_with_template('esmis_website_admission.esmis_admission_application_med_cert_upload_email_template', bulk=True)
		return res

class eSMISAdmissionUUIDRedirectionRecord(models.Model):
	_name = 'esmis.admission.redirection.line'

	name = fields.Char(string="Redirection")
	admission_id = fields.Many2one('esmis.admission', string="Admission")
