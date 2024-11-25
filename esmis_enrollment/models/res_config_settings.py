# -*- coding:utf-8 -*-
from odoo import fields, models


class InheritResConfigSettings(models.TransientModel):
	_inherit = "res.config.settings"

	enrollment_disable_sending_of_email = fields.Boolean(string="Disable auto sending of email", config_parameter="esmis_enrollment.enrollment_disable_sending_of_email")

