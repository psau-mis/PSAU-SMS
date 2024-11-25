from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError


class AdmissionExamSchedulingWizard(models.TransientModel):
	_name = 'esmis.admission.exam.scheduling.wiz'

	@api.model
	def default_get(self, fields):
		res = super(AdmissionExamSchedulingWizard, self).default_get(fields)
		if self.env.context.get("active_ids"):
			admission_ids = self.env["esmis.admission"].search(
				[
					("id", "in", self.env.context.get("active_ids")),
					("state", "=", 'received'),
				]
			)
			if admission_ids:
				res["admission_ids"] = admission_ids
			else:
				raise UserError(_("There are no admissions selected that are 'for examination state'!"))
			return res
		else:
			raise UserError(_("There are no selected Admissions!"))

	admission_ids = fields.Many2many("esmis.admission", string="Admissions")
	test_date = fields.Datetime(default=fields.Datetime.now())
	test_type_id = fields.Many2one('esmis.admission.test.type', string="Test Type", domain="[('active', '=', True)]", required=True)
	exam_responsible_ids = fields.Many2many('res.users', string="Exam Personnels", required=True)

	def set_exam_admission(self):
		for rec in self:
			message = _("Successfully scheduled an exam.")
			for admission in rec.admission_ids:
				admission.write({
					'test_date': rec.test_date,
					'test_scheduled_by_user_id': self.env.user.id,
					'active_course_id': admission.course1_id.id,
					'test_type_id': self.test_type_id.id,
					'exam_responsible_ids': [(6, 0, self.exam_responsible_ids.ids)],
					})
				if rec.test_date:
					admission.notify_test_sched()
					# message = _("Successfully notified students and scheduled an exam.")
			kind = "success"
			return {
				"type": "ir.actions.client",
				"tag": "display_notification",
				"params": {
					"title": _("Test Scheduling"),
					"message": message,
					"sticky": False,
					"type": kind,
					"next": {
						"type": "ir.actions.act_window_close",
					},
				},
			}

	def open_wizard(self):

		return {
			"name": "Schedule Tests",
			"view_mode": "form",
			"res_model": "esmis.admission.exam.scheduling.wiz",
			"view_id": self.env.ref(
				"esmis_admission.esmis_admission_exam_scheduling_wizard_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			"context": self.env.context,
		}
