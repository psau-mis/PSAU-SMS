# Copyright 2018 Modoolar <info@modoolar.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    password_expiration = fields.Integer(
        related="company_id.password_expiration", readonly=False
    )
    password_minimum = fields.Integer(
        related="company_id.password_minimum", readonly=False
    )
    password_history = fields.Integer(
        related="company_id.password_history", readonly=False
    )
    password_lower = fields.Integer(related="company_id.password_lower", readonly=False)
    password_upper = fields.Integer(related="company_id.password_upper", readonly=False)
    password_numeric = fields.Integer(
        related="company_id.password_numeric", readonly=False
    )
    password_special = fields.Integer(
        related="company_id.password_special", readonly=False
    )

    # blame ~ psau-jonas
    password_default = fields.Char(
        related='company_id.password_default',
        string="Default Password",
        readonly=False
    )

    @api.constrains('password_default')
    def _check_default_password(self):
        for settings in self:
            min_length = settings.minlength
            default_password = settings.password_default or ''
            min_lowercase = settings.password_lower
            min_uppercase = settings.password_upper
            min_numeric = settings.password_numeric
            min_special = settings.password_special

            if len(default_password) < min_length:
                raise ValidationError(_('Default password must have at least %s characters.') % min_length)

            if not any(char.islower() for char in default_password):
                raise ValidationError(_('Default password must contain at least %s lowercase letter(s).' % min_lowercase))

            if not any(char.isupper() for char in default_password):
                raise ValidationError(_('Default password must contain at least %s uppercase letter(s).' % min_uppercase))

            if not any(char.isdigit() for char in default_password):
                raise ValidationError(_('Default password must contain at least %s numeric digit(s).' % min_numeric))

            special_chars = set('!@#$%^&*()_+={}[]:";\'<>?/.,|\\`~')
            if not any(char in special_chars for char in default_password):
                raise ValidationError(_('Default password must contain at least %s special character(s).' % min_special))
    
    @api.constrains('minlength', 'password_lower', 'password_upper', 'password_numeric', 'password_special')
    def _check_minlength(self):
        for settings in self:
            total_minlength = settings.password_lower + settings.password_upper + settings.password_numeric + settings.password_special
            if settings.minlength < total_minlength:
                # raise ValidationError(_('The minimum password length cannot be less than the sum of Password Lowercase, Uppercase, Numeric, and Special characters.'))
                raise ValidationError(_('The minimum length configured in Password Policy cannot be less than %s characters. Please adjust the Password Lowercase, Uppercase, Numeric, and Special characters accordingly.') % total_minlength)