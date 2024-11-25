# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)


class eSMISPrograms(models.Model):
    _inherit = "esmis.course"

    fee_id = fields.Many2many("esmis.fees", domain="[('state', '=', 'active')]")