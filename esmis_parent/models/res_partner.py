# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    parent_record_id = fields.Many2one('parent.record', string='Guardian Record', compute='_compute_partner_record_id')
    is_parent = fields.Boolean()

    @api.depends('is_student', 'parent_record_id')
    def _compute_partner_record_id(self):
        for partner in self:
            if partner.is_student:
                parent_record = self.env['parent.record'].search([('child_ids', 'in', partner.id)], limit=1)
                if parent_record:
                    partner.parent_record_id = parent_record.id
                else:
                    partner.parent_record_id = False
            else:
                partner.parent_record_id = False

    def action_open_parent_record(self):
        self.ensure_one()
        if self.parent_record_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'parent.record',
                'view_mode': 'form',
                'view_id': self.env.ref('esmis_parent.parent_form_view').id,
                'res_id': self.parent_record_id.id,
                'target': 'current',
            }
        else:
            return {
                'warning': {
                    'title': 'No Parent Record',
                    'message': 'No related parent record found.',
                },
            }
