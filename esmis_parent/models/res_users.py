# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResUsers(models.Model):
    _inherit = 'res.users'

    parent_record_id = fields.Many2one('parent.record', string='Parent Record', compute='_compute_parent_record_id')

    @api.depends('login')
    def _compute_parent_record_id(self):
        for user in self:
            if user.login:
                parent_record = self.env['parent.record'].search([('email', '=', user.login)], limit=1)
                if parent_record:
                    user.parent_record_id = parent_record.id
                else:
                    user.parent_record_id = False
            else:
                user.parent_record_id = False