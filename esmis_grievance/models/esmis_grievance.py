# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class eSMISGrievance(models.Model):
    _name = 'esmis.grievance'
    _description = 'eSMIS Grievance'
    _rec_name = "grievance_no"
    _order = "id asc"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('in_review', 'In Review'),
        ('in_action', 'In Action'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Grievance State', default='draft')

    grievance_no = fields.Char('Grievance No.')

    grievance_by = fields.Selection([
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('faculty', 'Faculty'),
    ], string='Grievance By', required=True)

    grievance_subject = fields.Char('Grievance Subject', required=True)

    student_id = fields.Many2one('res.partner', string='Student', domain="[('is_student', '=', True)]", readonly=True)
    parent_id = fields.Many2one('parent.record', string='Parent', domain="[('is_parent', '=', True)]")
    faculty_id = fields.Many2one('hr.employee', string='Faculty', domain="[('job_id.name', '=', 'Teacher')]")

    grievance_date_creation = fields.Date('Date Created', readonly=True)
    grievance_category = fields.Selection([
        ('academic', 'Academic'),
        ('non_academic', 'Non Academic'),
    ], string='Grievance Category', required=True)

    course_id = fields.Many2one('esmis.course', string='Program', readonly=True, compute='_compute_enrollment_info', store=True)
    section_id = fields.Many2many('esmis.sections', string='Section', readonly=True, compute='_compute_enrollment_info', store=True)
    # academic_year_id = fields.Many2one('esmis.school.year', string='Academic Year', readonly=True)
    academic_year = fields.Char(string='Academic Year', readonly=True, compute='_compute_enrollment_info', store=True)
    academic_semester_id = fields.Many2one('esmis.school.year', string='Academic Semester', readonly=True, compute='_compute_enrollment_info', store=True)

    grievance_description = fields.Text()
    action_taken = fields.Text()

    @api.model
    def create(self, vals):
        """
            extends default create function
            set field grievance_no sequence value and grievance_date_creation
        """
        grievance_no = vals.get('grievance_no', False)
        if not grievance_no:
            admission_no_seq = self.env['ir.sequence'].sudo().next_by_code('esmis.grievance.no') or '/'
            vals['grievance_no'] = admission_no_seq
        
        vals['grievance_date_creation'] = fields.Date.today()

        res = super(eSMISGrievance, self.sudo()).create(vals)
        return res
    
    @api.onchange('grievance_by', 'parent_id')
    def onchange_grievance_by(self):
        """
        Set the domain for student_id based on the selected parent_id
        and set the default domain for student_id if the grievance_by selected is student
        """
        if self.grievance_by == 'parent' and self.parent_id:
            self.student_id = False
            self.faculty_id = False
            parents_child = [('id', 'in', self.parent_id.child_ids.ids)]

            return {'domain': {'student_id': parents_child}}
        elif self.grievance_by == 'student':
            self.parent_id = False
            self.student_id = False
            self.faculty_id = False
            student_id = [('is_student', '=', True)]

            return {'domain': {'student_id': student_id}}
        elif self.grievance_by == 'faculty':
            self.parent_id = False
            self.student_id = False
            return {'domain': {'faculty_id': [('job_id.name', '=', 'Teacher')]}}

    @api.depends('student_id')
    def _compute_enrollment_info(self):
        for record in self:
            if record.student_id:
                enrollment = self.env['esmis.enrollment'].sudo().search([
                    ('student_id', '=', record.student_id.id),
                    ('status', '=', 'enrolled')
                ], order='id desc', limit=1)

                if enrollment:
                    record.course_id = enrollment.curriculum_id.course_id.id
                    record.section_id = enrollment.section_id.ids
                    record.academic_year = enrollment.year_level
                    record.academic_semester_id = enrollment.curriculum_id.year_id.id
                else:
                    record.course_id = False
                    record.section_id = False
                    record.academic_year = False
                    record.academic_semester_id = False

    # state actions and function
    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_review(self):
        self.write({'state': 'in_review'})

    def action_take_action(self):
        view_id = self.env.ref('esmis_grievance.view_grievance_action_wizard_form').id
        return {
            'name': 'Take Action',
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'grievance.action.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def action_reject(self):
        self.write({'state': 'rejected'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_close(self):
        self.write({'state': 'closed'})