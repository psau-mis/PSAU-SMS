from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.http import request


class StudentCAVWiz(models.TransientModel):
	_name = 'cav.wiz'

	@api.model
	def default_get(self, fields):
		res = super(StudentCAVWiz, self).default_get(fields)
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
	board_resolution_no = fields.Char(string="Board Resolution No.", required=True)
	processed_by = fields.Char(string="Processed By", default=lambda self: self.env.user.name, required=True)
	reviewed_by = fields.Char(string="Reviewed By", default=lambda self: self.env.user.name, required=True)
	or_no = fields.Char(string="O.R. No.")
	cav_suc_no = fields.Char(string="CAV SUC No.", required=True)
	purpose = fields.Text(string="Purpose", required=True)

	def confirm_cav(self):
		report_action = self.env.ref('esmis_admission.action_cav_report_form')
		request.session['requestor_name'] = self.requestor_name
		request.session['purpose'] = self.purpose
		request.session['board_resolution_no'] = self.board_resolution_no
		request.session['processed_by'] = self.processed_by
		request.session['reviewed_by'] = self.reviewed_by
		request.session['or_no'] = self.or_no
		request.session['cav_suc_no'] = self.cav_suc_no
		report = report_action.report_action(self.student_ids.ids)
		return report



class StudentCAVReport(models.AbstractModel):
	_name = 'report.esmis_admission.report_cav'
	_description = 'CAV'

	@api.model
	def _get_report_values(self, docids, data=None):
		docs = self.env['res.partner'].browse(docids)
		return {
			'doc_ids': docids,
			'doc_model': 'res.partner',
			'docs': docs,
			'requestor_name': request.session.get('requestor_name', ''),
			'processed_by': request.session.get('processed_by', ''),
			'reviewed_by': request.session.get('reviewed_by', ''),
			'or_no': request.session.get('or_no', ''),
			'board_resolution_no': request.session.get('board_resolution_no', ''),
			'purpose': request.session.get('purpose', ''),
			'cav_suc_no': request.session.get('cav_suc_no', '')
		}
