# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)


class eSMISCashierResPartner(models.Model):
    _inherit = "res.partner"

    is_cashier = fields.Boolean(default=False)
    cashier_invoice_ids = fields.One2many("esmis.cashier", "student_id")

    # Todo: Add invoices tabs in students form

    @api.onchange("is_cashier")
    def _onchange_is_cashier(self):
        for rec in self:
            if rec.is_cashier:
                rec.employee_position = self.env.ref("esmis_cashier.emp_pos_cashier").id

    # Todo: If the employee_position was changed the is_cashier should be change also

    def lock_cashier(self):
        for rec in self:
            if rec.state == 'unlock':
                rec.state = 'lock'
            else:
                raise UserError(_("The cashier record is already locked."))

    def unlock_cashier(self):
        for rec in self:
            if rec.state == 'lock':
                rec.state = 'unlock'
            else:
                raise UserError(_("The cashier record is already un-locked."))