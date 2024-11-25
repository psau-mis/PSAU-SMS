# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, RedirectWarning

class Parent(models.Model):
    _name = 'parent.record'
    _description = 'Parent Record'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company.id)

    name = fields.Char(string='Parent Name', required=True)
    email = fields.Char(string='Email', required=True)
    mobile = fields.Char(string='Mobile Number', required=True)
    child_ids = fields.Many2many('res.partner', string='Children', domain="[('is_student', '=', True)]")
    is_parent = fields.Boolean()

    def send_mail_with_template(self, template, context={}):
        mail_template = self.env.ref(template)
        self.with_context(context).message_post_with_template(template_id=mail_template.id)

    @api.model
    def create(self, vals):
        email_exists = vals.get('email') and self.env['parent.record'].search_count([('email', '=', vals['email'])]) > 0

        default_password = self.env.user.company_id.generate_password() #random password generator
        email_template = 'password_security.mail_esmis_parent_portal_user_password' #email template for parent credentials
        parent_name = vals.get('name')
        parent_email = vals.get('email')
        parent_mobile = vals.get('mobile')
        
        if email_exists:
            raise UserError("Email address is already associated with another parent record.")

        parent = super(Parent, self).create(vals)

        if parent_email:
            user = self._create_portal_user(parent, parent_email, parent_mobile, default_password)
            if user:
                parent.write({'is_parent': True})
                parent.send_mail_with_template(email_template, context={'name': parent_name, 'email': parent_email, 'password': default_password,})
            else:
                raise ValidationError("Failed to create the Parent record. Please check the email address.")
        else:
                raise ValidationError("Failed to create the Parent record. Please check the email address.")
                
        return parent

    # This function is called in the def create function to automatically create parent user and 
    # make it a portal user and pass user_values ↓↓↓↓↓↓
    def _create_portal_user(self, parent, email, mobile, password):
        password_write_date = datetime.now() - timedelta(days=1)
        user_vals = {
            'name': parent.name,
            'login': email,
            'email': email,
            'password': password,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
            'mobile': mobile,
            'is_parent': True,
            'password_write_date': password_write_date,
        }

        return self.env['res.users'].sudo().create(user_vals)
        # OLD EMAIL SENDING CODE
        # template = self.env.ref('password_security.mail_esmis_parent_portal_user_password')
        # template.sudo().send_mail(user.id, force_send=True)
        # if template:
        #     ctx = {
        #         'email': email,
        #         'generated_password': password,
        #     }
            # template.sudo().with_context(ctx).send_mail(user.id, force_send=True)

    def write(self, vals):
        if 'email' in vals:
            email_exists = self.env['parent.record'].search_count([('email', '=', vals['email']), ('id', '!=', self.id)]) > 0
            if email_exists:
                raise UserError("Email address is already associated with another parent record.")

            for parent in self:
                user = self.env['res.users'].sudo().search([('email', '=', parent.email)], limit=1)
                if user:
                    user.write({'email': vals['email']})

        res = super(Parent, self).write(vals)
        if 'email' in vals or 'mobile' in vals or 'name' in vals:
            for parent in self:
                user = self.env['res.users'].sudo().search([('email', '=', parent.email)], limit=1)
                if user:
                    user.write({
                        'name': parent.name,
                        'login': parent.email,
                        'mobile': parent.mobile,
                        'mobile_number': parent.mobile,
                    })
        return res
    
    # Check if mobile is 11 digit starting from 09 ↓↓↓↓↓↓
    @api.constrains('mobile')
    def _check_mobile_format(self):
        for parent in self:
            if parent.mobile and (len(parent.mobile) != 11 or not parent.mobile.startswith('09') or not parent.mobile.isdigit()):
                raise ValidationError("Mobile number should be 11 digits and start with '09'.")
    
    # Check if children is already linked in a parent record ↓↓↓↓↓↓
    @api.constrains('child_ids')
    def _check_children_association(self):
        for parent in self:
            associated_children = self.env['parent.record'].search([('child_ids', 'in', parent.child_ids.ids), ('id', '!=', parent.id)])
            if associated_children:
                child_names = ' and '.join(associated_children.mapped('child_ids.full_name'))
                parent_name = ', '.join(associated_children.mapped('name'))
                
                error_msg = _('%(child_names)s records are already associated with other parent records: %(parent_name)s') % {
                    'child_names': child_names,
                    'parent_name': parent_name,
                }
                action_error = self.env.ref('esmis_parent.parent_menu_action').read()[0]
                action_error['domain'] = [('id', 'in', associated_children.ids)]

                raise RedirectWarning(error_msg, action_error, _('Go to parents'))
                # raise ValidationError(f"{child_names} record(s) already associated with other parent records: {parent_name}")

    # @api.model
    # def set_is_parent_for_existing_records(self):
    #     # Update is_parent to True for existing records
    #     existing_records = self.search([])
    #     for record in existing_records:
    #         user = self.env['res.users'].sudo().search([('email', '=', record.email)], limit=1)
    #         if user:
    #             user.write({'is_parent': True})
    #     return True

    def unlink(self):
        for parent in self:
            user = self.env['res.users'].sudo().search([('email', '=', parent.email)], limit=1)
            if user and user.active:    
                error_msg = _('You cannot delete contacts linked to an active user.\n'
                          'You should rather archive them after archiving their associated user.\n\n'
                          'Linked active users : %(names)s', names=", ".join([u.display_name for u in user]))
                action_error = user._action_show()
                raise RedirectWarning(error_msg, action_error, _('Go to users'))
                # raise UserError("Cannot delete parent records with active or not yet deleted user records. Deactivate or delete associated user records first.")
        
        return super(Parent, self).unlink()