from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
import time


class AdmissionNotQualifiedWizard(models.TransientModel):
	_name = 'esmis.admission.not.qualified.wiz'

	admission_id = fields.Many2one("esmis.admission", string="Admissions")
	course_id = fields.Many2one("esmis.course", string="Course")
	active_course_id = fields.Many2one("esmis.course", string="Active Course")
	evaluation_selection = fields.Selection([('admitted', 'Admitted'), ('not_admitted', 'Not Admitted')], string="Evaluation", required=True)
	reason = fields.Selection([('gwa', 'SUBJECT GRADE/GWA'), ('test_results', 'TEST RESULTS'), ('no_more_slots', 'NO MORE SLOTS')], string="Not Admitted Because of", required=True)

	def save_admission(self):
		kind = 'info'
		update = {}
		message = _(
			"Admission was transferred to the next program admission officer")
		if self.course_id.id == self.admission_id.course1_id.id:
			update['evaluation1'] = dict(self._fields['evaluation_selection'].selection).get(self.evaluation_selection) or 'Not Specified'
			update['reason1'] = dict(self._fields['reason'].selection).get(self.reason) or 'Not Specified'
			update['active_course_id'] = self.active_course_id
		elif self.course_id.id == self.admission_id.course2_id.id:
			update['evaluation2'] = dict(self._fields['evaluation_selection'].selection).get(self.evaluation_selection) or 'Not Specified'
			update['reason2'] = dict(self._fields['reason'].selection).get(self.reason) or 'Not Specified'
			update['active_course_id'] = self.active_course_id
		elif self.course_id.id == self.admission_id.course3_id.id:
			update['evaluation3'] = dict(self._fields['evaluation_selection'].selection).get(self.evaluation_selection) or 'Not Specified'
			update['reason3'] = dict(self._fields['reason'].selection).get(self.reason) or 'Not Specified'

		if not self.active_course_id:
			update['not_qualified_by_id'] = self.env.user.id
			update['not_qualified_datetime'] = fields.Datetime.now()
			update['state'] = 'not_qualified'
			message = _(
				"Student was not qualified in all chosen program")
			kind = 'danger'
		self.admission_id.update(update)
		redirect = self.env.ref('esmis_admission.action_esmis_admission_form_for_evaluation').run()
		return redirect
