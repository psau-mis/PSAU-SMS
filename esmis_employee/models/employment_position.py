# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISEmploymentPosition(models.Model):
    _name = "esmis.employment.positions"
    _description = "Employment Positions"
    _order = "id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Position')

    def unlink(self):
        for rec in self:
            external_identifier = self.env["ir.model.data"].search(
                [("res_id", "=", rec.id), ("model", "=", "esmis.employment.positions")]
            )
            if external_identifier and external_identifier.name:
                raise ValidationError(_("Can't delete default Employment Positions"))
            return super(eSMISEmploymentPosition, self).unlink()

    def write(self, vals):
        for rec in self:
            external_identifier = self.env["ir.model.data"].search(
                [("res_id", "=", rec.id), ("model", "=", "esmis.employment.positions")]
            )
            if external_identifier and external_identifier.name:
                raise ValidationError(_("Can't edit default Employment Positions"))
            else:
                return super(eSMISEmploymentPosition, self).write(vals)
