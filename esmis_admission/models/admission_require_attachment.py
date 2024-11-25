from odoo import api, fields, models, tools, _
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError, UserError


class AdmissionRequirePDFAttachment(models.Model):
	_name = 'admission.require.attachment'

	name = fields.Char(string="Name", default="Default Form for Requiring Attachment")
	tor_transferee = fields.Boolean(string='Transferee TOR (Transcript of Records)', default=True)
	tor_foreign = fields.Boolean(string='Transferee TOR (Transcript of Records)', default=True)
	tor_bachelor = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records)", default=True)
	tor_bachelor_continuing = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records)", default=True)
	tor_bachelor_graduate = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records)", default=True)
	tor_master = fields.Boolean(string="TOR Masters' Degree (Transcript of Records)", default=True)
	tor_current_master = fields.Boolean(string="TOR Current Masters' Program (Transcript of Records)", default=True)
	tor_current_doctor = fields.Boolean(string="TOR Current Doctors' Program (Transcript of Records)", default=True)
	birth_cert_transferee = fields.Boolean(string='PSA-issued Birth Certificate', default=True)
	birth_cert_freshmen = fields.Boolean(string='PSA-issued Birth Certificate', default=True)
	birth_cert_continuing = fields.Boolean(string='PSA-issued Birth Certificate', default=True)
	employ_cert_graduate = fields.Boolean(string='Certificate of Employment', default=True)
	employ_cert_transferee2 = fields.Boolean(string='Certificate of Employment', default=True)
	employ_cert_graduate2 = fields.Boolean(string='Certificate of Employment', default=True)
	employ_cert_transferee3 = fields.Boolean(string='Certificate of Employment', default=True)
	honorable_dismissal_transferee = fields.Boolean(string='Honorable Dismissal', default=True)
	honorable_dismissal_transferee2 = fields.Boolean(string='Honorable Dismissal', default=True)
	honorable_dismissal_transferee3 = fields.Boolean(string='Honorable Dismissal', default=True)
	shs_report_card = fields.Boolean(string='Senior Highschool Report Card', default=True)
	gmc_cert = fields.Boolean(string='Certificate of Good Moral Character', default=True)
	stud_personal_statement = fields.Boolean(string='Student Personal History Statement', default=True)
	passport_bio = fields.Boolean(string='Passport Bio Page', default=True)
	birth_cert_foreign = fields.Boolean(string='Birth Certificate', default=True)
	english_cert = fields.Boolean(string='Certificate of English Proficiency', default=True)
	police_clearance = fields.Boolean(string='Police Clearance (Philippines NBI)', default=True)

	def unlink(self):
		raise ValidationError('You cannot delete this default form...')
		return super().unlink()

	@api.model
	def action_configuration_view(self):
		default_form = self.env.ref('esmis_admission.default_requiring_form').sudo().id or False
		return {
			"name": "Requiring Attachment",
			"view_mode": "form",
			"res_model": "admission.require.attachment",
			"type": "ir.actions.act_window",
			"target": 'current',
			"res_id": default_form,
		}

	@api.model
	def get_required(self, admission_type):
		list_of_required = []
		if admission_type == 'freshmen':
			if self.birth_cert_freshmen:
				list_of_required.append('birth_cert')
			if self.shs_report_card:
				list_of_required.append('shs_report_card')
			if self.gmc_cert:
				list_of_required.append('gmc_cert')

		if admission_type == 'transferee':
			if self.birth_cert_transferee:
				list_of_required.append('birth_cert')
			if self.tor_transferee:
				list_of_required.append('tor')
			if self.honorable_dismissal_transferee:
				list_of_required.append('honorable_dismissal')

		if admission_type == 'continuing':
			if self.birth_cert_continuing:
				list_of_required.append('birth_cert')
			if self.tor_bachelor_continuing:
				list_of_required.append('tor_bachelor')
				
		if admission_type == 'foreign':
			if self.stud_personal_statement:
				list_of_required.append('stud_personal_statement')
			if self.passport_bio:
				list_of_required.append('passport_bio')
			if self.birth_cert_foreign:
				list_of_required.append('birth_cert_foreign')
			if self.english_cert:
				list_of_required.append('english_cert')
			if self.police_clearance:
				list_of_required.append('police_clearance')
			if self.tor_foreign:
				list_of_required.append('tor')
				
		if admission_type == 'graduate':
			if self.tor_bachelor_graduate:
				list_of_required.append('tor_bachelor')
			if self.employ_cert_graduate:
				list_of_required.append('employ_cert')
				
		if admission_type == 'transferee2':
			if self.honorable_dismissal_transferee2:
				list_of_required.append('honorable_dismissal')
			if self.employ_cert_transferee2:
				list_of_required.append('employ_cert')
			if self.tor_current_master:
				list_of_required.append('tor_current_master')
				
		if admission_type == 'graduate2':
			if self.tor_master:
				list_of_required.append('tor_master')
			if self.employ_cert_graduate2:
				list_of_required.append('employ_cert')
				
		if admission_type == 'transferee3':
			if self.tor_current_doctor:
				list_of_required.append('tor_current_doctor')
			if self.employ_cert_transferee3:
				list_of_required.append('employ_cert')
			if self.honorable_dismissal_transferee3:
				list_of_required.append('honorable_dismissal')
			
		return list_of_required
