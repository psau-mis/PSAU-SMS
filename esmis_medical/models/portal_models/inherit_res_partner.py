from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class InheritPartner(models.Model):
    _inherit = "res.partner"

    is_medical_sent = fields.Boolean('Is Medical Sent', compute='_compute_is_medical_sent', store=True)

    medical_cert_upload = fields.Binary(string='Medical Certificate')
    medical_cert_upload_name = fields.Char(string='Medical Certificate File Name')

    health_clearance_upload = fields.Binary(string='Health Clearance')
    health_clearance_upload_name = fields.Char(string='Health Clearance File Name')

    @api.depends('medical_cert_upload', 'health_clearance_upload')
    def _compute_is_medical_sent(self):
        for record in self:
            # Set is_medical_sent to True if both binary field has a value
            record.is_medical_sent = bool(record.medical_cert_upload and record.health_clearance_upload)