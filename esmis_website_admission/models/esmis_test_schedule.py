from odoo import models, fields, api, _
import uuid


class eSMISTestSchedule(models.Model):
	_inherit = 'esmis.admission.test.schedule'

	def set_as_complete(self):
		super(eSMISTestSchedule, self).set_as_complete()
		for rec in self.esmis_admission_ids:
			rec.write({
				'medical_cert_url_uuid': uuid.uuid4(),
				})
			rec.send_mail_with_template('esmis_website_admission.esmis_admission_application_med_cert_upload_email_template')
