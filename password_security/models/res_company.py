# Copyright 2016 LasLabs Inc.
# Copyright 2017 Kaushal Prajapati <kbprajapati@live.com>.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models
import random, string


class ResCompany(models.Model):
    _inherit = "res.company"

    password_expiration = fields.Integer(
        "Days",
        default=60,
        help="How many days until passwords expire",
    )
    password_lower = fields.Integer(
        "Lowercase",
        default=1,
        help="Require number of lowercase letters",
    )
    password_upper = fields.Integer(
        "Uppercase",
        default=1,
        help="Require number of uppercase letters",
    )
    password_numeric = fields.Integer(
        "Numeric",
        default=1,
        help="Require number of numeric digits",
    )
    password_special = fields.Integer(
        "Special",
        default=1,
        help="Require number of unique special characters",
    )
    password_history = fields.Integer(
        "History",
        default=30,
        help="Disallow reuse of this many previous passwords - use negative "
        "number for infinite, or 0 to disable",
    )
    password_minimum = fields.Integer(
        "Minimum Hours",
        default=24,
        help="Amount of hours until a user may change password again",
    )

    # blame ~ psau-jonas
    password_default = fields.Char(
        string="Default Password",
        default="Psau!2024",
        help="Default password for new users in this company",
    )

    def generate_password(self):
        # Fetch the password policy settings
        params = self.env["ir.config_parameter"].sudo()
        minlength = int(params.get_param("auth_password_policy.minlength", default=8))

        # Get the password policy from the company settings
        lowercase_count = self.password_lower
        uppercase_count = self.password_upper
        numeric_count = self.password_numeric
        special_count = self.password_special

        # Create character pools
        lowercase_chars = string.ascii_lowercase
        uppercase_chars = string.ascii_uppercase
        numeric_chars = string.digits
        special_chars = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

        # Store random characters in password array
        password = []
        password.extend(random.choices(lowercase_chars, k=lowercase_count))
        password.extend(random.choices(uppercase_chars, k=uppercase_count))
        password.extend(random.choices(numeric_chars, k=numeric_count))

        # Ensure exactly special_count special characters
        password.extend(random.choices(special_chars, k=special_count))

        # Calculate the current length and the remaining length to meet the minimum length
        current_length = len(password)
        remaining_length = max(0, minlength - current_length)

        # Add random characters to meet the remaining length
        all_chars = lowercase_chars + uppercase_chars + numeric_chars + special_chars
        password.extend(random.choices(all_chars, k=remaining_length))

        # Shuffle the password list to ensure randomness
        random.shuffle(password)

        # Convert list to string and return the password
        return ''.join(password)