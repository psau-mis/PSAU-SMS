# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISCashierLine(models.Model):
    _name = "esmis.cashier.line"
    _description = "Cashier Line"
    _order = "sequence asc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(compute="_compute_name", store=True)
    cashier_id = fields.Many2one("esmis.cashier", string="Cashier")
    fee_id = fields.Many2one("esmis.coa", string="Item")
    fee_amount = fields.Float()
    discount = fields.Float()
    qty = fields.Integer(default=1)
    total = fields.Float(compute="_compute_total", store=True)
    remarks = fields.Text()
    is_non_ledger = fields.Boolean(default=False, string="Non Ledger")
    group = fields.Char()
    type = fields.Char()
    reference = fields.Char()
    amount_paid = fields.Float(string="Amount Paid")
    sequence = fields.Integer()
  


    # def filter_fee(self):
    #     coa_id = self.env['esmis.coa'].search()

    @api.depends("fee_id")
    def _compute_name(self):
        for rec in self:
            rec.name = "{}".format(rec.fee_id.name)

    # @api.onchange("fee_id")
    # def _onchange_fee_id(self):
    #     fee_amount = 0
    #     for rec in self:
    #         if rec.fee_id:
    #             for record in rec.fee_id:
    #                 fee_amount = fee_amount + record.amount
    #     self.fee_amount = fee_amount

    @api.depends("fee_amount", "qty", "discount")
    def _compute_total(self):
        for rec in self:
            total = 0
            if rec.fee_amount and rec.qty:
                total = (rec.fee_amount * rec.qty)
                if rec.discount:
                    total = total - rec.discount
            rec.total = total
