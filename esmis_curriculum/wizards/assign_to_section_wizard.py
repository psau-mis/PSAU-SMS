# Part of eSMIS App. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class eSMISAssignToSection(models.TransientModel):
    _name = "esmis.sections.assign.wizard"
    _description = "Add Students to Sections Wizard"

    @api.model
    def default_get(self, fields):
        res = super(eSMISAssignToSection, self).default_get(fields)
        if self.env.context.get("active_ids"):
            enrollment_ids = self.env["esmis.enrollment"].search(
                [
                    ("id", "in", self.env.context.get("active_ids")),
                    ("status", "in", ['new', 'validated']),
                ]
            )
            if enrollment_ids:
                res["enrollment_ids"] = enrollment_ids
            return res
        else:
            raise UserError(_("There are no selected Enrollments!"))

    enrollment_ids = fields.Many2many("esmis.enrollment", string="Enrollments")

    def assign_enrollments(self):
        for rec in self:
            success_ctr = 0
            error_ctr = 0

            for enrollment in rec.enrollment_ids:
                sections = self.env["esmis.sections"].search([("course_id", "=", enrollment.course_id.id)])
                success_assign = False
                for section in sections:
                    section._compute_reach_max()
                    if not section.reach_max:
                        enrollment.section_id = section.id
                        enrollment._onchange_section_id()
                        enrollment.fetch_from_section()
                        success_ctr += 1
                        success_assign = True
                        break
                if not success_assign:
                    error_ctr += 1

            message = _("%s enrollment/s assigned. %s enrollment/s not assigned" % (success_ctr, error_ctr))
            kind = "info"
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Assign to Section"),
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
            "name": "Auto-Assign Section",
            "view_mode": "form",
            "res_model": "esmis.sections.assign.wizard",
            "view_id": self.env.ref(
                "esmis_curriculum.esmis_section_assign_wizard_form_view"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": self.env.context,
        }
