from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.http import request


class CertificationLatinHonorWiz(models.TransientModel):
	_name = 'certification.latin.honor.wiz'

	@api.model
	def default_get(self, fields):
		res = super(CertificationLatinHonorWiz, self).default_get(fields)
		if self.env.context.get("active_ids"):
			student_ids = self.env["res.partner"].search(
				[
					("id", "in", self.env.context.get("active_ids")),
				]
			)
			if student_ids:
				res["student_ids"] = student_ids
			else:
				raise UserError(_("There are no selected Student/s!"))
			return res
		else:
			raise UserError(_("There are no selected Student/s!"))

	student_ids = fields.Many2many('res.partner', string='Students')
	requestor_name = fields.Char(string="Name of Requestor", default=lambda self: self.env.user.name, required=True)
	latin_honor = fields.Selection([('Magna Cum Laude', 'Magna Cum Laude'), ('Cum Laude','Cum Laude'), ('Summa Cum Laude','Summa Cum Laude')], default="Magna Cum Laude", string="Latin Honor", required=True)
	purpose = fields.Text(string="Purpose", required=True)

	def confirm_certification(self):
		report_action = self.env.ref('esmis_admission.action_certification_of_latin_honors_form')
		request.session['requestor_name'] = self.requestor_name
		request.session['latin_honor'] = self.latin_honor
		request.session['purpose'] = self.purpose
		report = report_action.report_action(self.student_ids.ids)
		return report



class StudentCertificationOfLatinHonorsReport(models.AbstractModel):
	_name = 'report.esmis_admission.report_certification_of_latin_honors'
	_description = 'Student Certification of Latin Honor added context'

	@api.model
	def _get_report_values(self, docids, data=None):
		docs = self.env['res.partner'].browse(docids)
		return {
			'doc_ids': docids,
			'doc_model': 'res.partner',
			'docs': docs,
			'requestor_name': request.session.get('requestor_name', False),
			'latin_honor': request.session.get('latin_honor', False),
			'purpose': request.session.get('purpose', False),
		}
