from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class InheritEmployee(models.Model):
    _inherit = "hr.employee"

    def send_mail_with_template(self, template, context={}):
        mail_template = self.env.ref(template)
        self.with_context(context).message_post_with_template(template_id=mail_template.id)