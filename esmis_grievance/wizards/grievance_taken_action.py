from odoo import api, fields, models

class GrievanceActionWizard(models.TransientModel):
    _name = 'grievance.action.wizard'
    _description = 'Grievance Action Wizard'

    action_taken = fields.Text(required=True)

    def button_apply_action(self):
        active_grievance = self.env['esmis.grievance'].browse(self.env.context.get('active_id'))

        active_grievance.write({'action_taken': self.action_taken})

        active_grievance.write({'state': 'in_action'})

        return {'type': 'ir.actions.act_window_close'}