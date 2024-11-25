# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning,UserError

_logger = logging.getLogger(__name__)


class eSMISEmpResPartner(models.Model):
    _inherit = "res.partner"

    is_employee = fields.Boolean()
    is_teacher = fields.Boolean()
    date_employed = fields.Date()
    employee_position = fields.Many2one("esmis.employment.positions", string="Position")
    name_title = fields.Char()
    name_2 = fields.Char(compute="_compute_name_2")

    signature_img = fields.Binary("Signature")
    signature_img_filename = fields.Char("Signature Filename")

    def _compute_name_2(self):
        for rec in self:
            # name_2 = "{} {} {}, {}".format(rec.first_name.upper() or False, rec.middle_name.upper() or False, rec.last_name.upper() or False, rec.name_title or False)
            # rec.name_2 = name_2

            name_2 = str("" if rec.last_name == False else rec.last_name.upper() + ", " + 
                ("" if rec.first_name == False else " " + rec.first_name.upper()) +
                ("" if rec.middle_name == False else " " + rec.middle_name.upper()) +
                ("" if rec.suffix_name == False else " " + rec.suffix_name.upper()))

            rec.name_2 = name_2

    def lock_teacher(self):
        for rec in self:
            if rec.state == 'unlock':
                rec.state = 'lock'
            else:
                raise UserError(_("The teacher record is already locked."))

    def unlock_teacher(self):
        for rec in self:
            if rec.state == 'lock':
                rec.state = 'unlock'
            else:
                raise UserError(_("The teacher record is already un-locked."))

    def lock_employee(self):
        for rec in self:
            if rec.state == 'unlock':
                rec.state = 'lock'
            else:
                raise UserError(_("The employee record is already locked."))

    def unlock_employee(self):
        for rec in self:
            if rec.state == 'lock':
                rec.state = 'unlock'
            else:
                raise UserError(_("The employee record is already un-locked."))

    @api.onchange('student_no_undg', 'student_no_grad', 'last_name', 'first_name', 'middle_name', 'suffix_name')
    def partner_name_change(self):
        if self.is_student:
            vals = {}
            name = ''
            stud_no = ''
            if self.student_no_grad:
                stud_no = '[' + self.student_no_grad + '] '
            elif self.student_no_undg:
                stud_no = '[' + self.student_no_undg + '] '
            if self.last_name:
                name += self.last_name + ', '
                vals.update({'last_name': self.last_name.title()})
            if self.first_name:
                name += self.first_name + ' '
                vals.update({'first_name': self.first_name.title()})
            if self.middle_name:
                name += self.middle_name + ' '
                vals.update({'middle_name': self.middle_name.title()})
            suffix_name = self.suffix_name or ''
            full_name = name.title() + suffix_name

            vals.update({
                'full_name': full_name,
                'name': stud_no + full_name,
            })
            self.update(vals)
        elif self.is_employee:
            vals = {}
            name = ''
            if self.last_name:
                name += self.last_name + ', '
                vals.update({'last_name': self.last_name.title()})
            if self.first_name:
                name += self.first_name + ' '
                vals.update({'first_name': self.first_name.title()})
            if self.middle_name:
                name += self.middle_name + ' '
                vals.update({'middle_name': self.middle_name.title()})

            suffix_name = self.suffix_name or ''
            full_name = name.title() + suffix_name

            vals.update({
                'full_name': full_name,
                'name': full_name,
            })
            self.update(vals)

    @api.model
    def create(self, vals):
        partner = super(eSMISEmpResPartner, self).create(vals)
        if partner:
            if partner.is_teacher:
                if not partner.employee_position:
                    partner.employee_position = self.env.ref("esmis_employee.emp_pos_teacher").id
        return partner
