# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, RedirectWarning

class EsmisEnrollmentInherit(models.Model):
    _inherit = "esmis.enrollment"

    def _get_report_base_filename(self):
        return 'COR - %s' % (self.student_id.student_no_undg) if self.student_id.student_no_undg else 'COR - %s' % (self.student_id.student_no_grad)