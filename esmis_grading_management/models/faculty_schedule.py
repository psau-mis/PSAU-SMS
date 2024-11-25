import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)

   
class FacultySchedule(models.Model):
	_inherit = "esmis.subject.offerings"


	teacher_id_1 = fields.Many2one("hr.employee", compute="_compute_user")


	def _compute_user(self):
		for rec in self:
			current_user = self.env['hr.employee'].search([('user_id', '=', rec._uid)])
			rec.teacher_id_1 = current_user.id
			