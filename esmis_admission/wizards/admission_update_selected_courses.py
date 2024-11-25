from odoo import _, api, fields, models
from odoo.exceptions import UserError


class UpdateSelectedCourses(models.TransientModel):
	_name = 'admission.update.selected.courses'

	admission_id = fields.Many2one("esmis.admission", string="Admissions", required=True)
	current_course_ids = fields.Many2many('esmis.course', string="Current", required=True)
	whole_level = fields.Char(string="Whole Level")
	course1_id = fields.Many2one('esmis.course', string="Select Program", domain="[('level', '=', whole_level)]", required=True)
	course2_id = fields.Many2one('esmis.course', string="Second Choice")
	course3_id = fields.Many2one('esmis.course', string="Third Choice")

	def update_course(self):
		if self.admission_id:
			self.admission_id.write({
				'course1_id': self.course1_id.id,
				'course2_id': False,
				'course3_id': False,
				'for_evaluation_by_id': self.env.user.id,
				'for_evaluation_datetime': fields.Datetime.now(),
				'state': 'for_evaluation',
				'active_course_id': self.course1_id.id,
				})
		return {
			"type": "ir.actions.client",
			"tag": "display_notification",
			"params": {
				"title": _("Course Updating"),
				"message": "Successfully saved..",
				"sticky": False,
				"type": 'success',
				"next": {
					"type": "ir.actions.act_window_close",
				},
			},
		}
