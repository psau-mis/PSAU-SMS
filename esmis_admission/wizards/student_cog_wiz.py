from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
from odoo.http import request


class StudentCertificateOfGradesWiz(models.TransientModel):
	_name = 'student.cog.wiz'

	@api.model
	def default_get(self, fields):
		res = super(StudentCertificateOfGradesWiz, self).default_get(fields)
		if self.env.context.get("active_ids"):
			student_ids = self.env["res.partner"].search(
				[
					("id", "in", self.env.context.get("active_ids")),
				]
			)
			if student_ids:
				res["student_ids"] = student_ids
			else:
				raise UserError(_("There are no selected Admissions!"))
			return res
		else:
			raise UserError(_("There are no selected Admissions!"))

	school_year_id = fields.Many2one('esmis.school.year', string='School Year/Semester', required=True)
	student_ids = fields.Many2many('res.partner', string='Students')

	def confirm_student_cog(self):
		report_action = self.env.ref('esmis_admission.action_report_student_cog_form')
		request.session['school_year_id'] = self.school_year_id.id
		request.session['school_year_name'] = self.school_year_id.name
		report = report_action.with_context(school_year_id=self.school_year_id).report_action(self.student_ids.ids)
		return report

class StudentCertificateOfGradesReport(models.AbstractModel):
	_name = 'report.esmis_admission.report_student_cog_form'
	_description = 'Student CoG report from School Year'

	@api.model
	def _get_report_values(self, docids, data=None):
		docs = self.env['res.partner'].browse(docids)
		return {
			'doc_ids': docids,
			'doc_model': 'res.partner',
			'docs': docs,
			'school_year_name': request.session.get('school_year_name', False),
			'school_year_id': request.session.get('school_year_id', False),
		}
