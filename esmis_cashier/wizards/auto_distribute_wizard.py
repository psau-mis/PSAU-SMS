# Part of eSMIS App. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class eSMISAutoDistributeWizard(models.TransientModel):
    _name = "esmis.auto.distribute.wizard"
    _description = "Auto Distribute Wizard"

    cashier_id = fields.Many2one("esmis.cashier")
    amount = fields.Float("Amount to Distribute")
    total_amount = fields.Float("Total Amount")
    fees_affected = fields.One2many("esmis.auto.distribute.lines.wizard", "distribute_id")

    def auto_distribute(self):
        for rec in self:
            rec.cashier_id.or_no = rec.name
            rec.cashier_id.or_date_mode = rec.or_date_mode
            rec.cashier_id.or_date = rec.or_date

            message = _("%s was successfully distributed.", rec.amount)
            kind = "success"
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Auto-Distribute"),
                    "message": message,
                    "sticky": False,
                    "type": kind,
                    "next": {
                        "type": "ir.actions.act_window_close",
                    },
                },
            }
    def reopen_wizard(self):

        return {
            "name": "Auto-Distribute",
            "view_mode": "form",
            "res_model": "esmis.admission.exam.sched.wizard",
            "view_id": self.env.ref(
                "esmis_admission.esmis_admission_exam_sched_wizard_form_view"
            ).id,
            "type": "ir.actions.act_window",
            "target": "new",
            "context": self.env.context,
        }

class eSMISAutoDistributeLinesWizard(models.TransientModel):
    _name = "esmis.auto.distribute.lines.wizard"
    _description = "Auto Distribute Lines Wizard"

    distribute_id = fields.Many2one("esmis.auto.distribute.wizard")
    fee_id = fields.Many2one("esmis.fees.types", string="Item")
    fee_amount = fields.Float()
