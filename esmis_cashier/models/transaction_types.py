# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISTransactionTypes(models.Model):
    _name = "esmis.transaction.types"
    _description = "Transaction Types"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Type')

    def unlink(self):
        for rec in self:
            external_identifier = self.env["ir.model.data"].search(
                [("res_id", "=", rec.id), ("model", "=", "esmis.transaction.types")]
            )
            if external_identifier and external_identifier.name:
                raise ValidationError(_("Can't delete default Fees"))
            return super(eSMISTransactionTypes, self).unlink()
