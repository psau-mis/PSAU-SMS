from odoo import _, api, fields, models

class InheritResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def get_default_portal_user(self):
        return self.env.ref('base.group_portal').id