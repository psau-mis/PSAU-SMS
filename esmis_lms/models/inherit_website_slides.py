from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

class InheritCourses(models.Model):
    _inherit = "slide.channel"

    channel_partner_ids = fields.One2many('slide.channel.partner', 'channel_id', string='Members Information', groups='website_slides.group_website_slides_officer,esmis_base.group_esmis_teacher', depends=['partner_ids'])
    visibility = fields.Selection([
        ('public', 'Open To All'),
        ('members', 'Members Only')
    ], default='members', string='Visibility', required=True, help='Defines who can access your courses and their content.')
    
    school_year_id = fields.Many2one('esmis.school.year', String='School Year', required=True)
    subject_id = fields.Many2one('esmis.subjects', string='Subject')
    section_ids = fields.Many2many('esmis.sections', string='Sections')

    # Computed fields for dynamic domains domain=[(...)] is decalared on xml form view inherit_website_slides_views.xml
    available_subject_ids = fields.Many2many('esmis.subjects', compute='_compute_available_subjects', string='Available Subjects')
    available_section_ids = fields.Many2many('esmis.sections', compute='_compute_available_sections', string='Available Sections')

    students_to_enroll = fields.Many2many('res.partner', string='Students to Enroll', compute='_get_students_to_enroll')

    def action_publish_course(self):
        """ Toggle the is_published field. """
        if not self.id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'warning',
                    'message': _("Please save the course to publish it.")
                }
            }
        else:
            self.is_published = True
            # self.is_published = not self.is_published

    def action_unpublish_course(self):
        """ Set the is_published field to False. """
        if self:
            self.is_published = False

    @api.onchange('school_year_id')
    def _onchange_school_year(self):
        """ Reset the subject_id and section_ids field when the school_year_id changes. """
        self.subject_id = False
        self.section_ids = False

    @api.onchange('subject_id')
    def _onchange_subject(self):
        """ Reset the section_ids field when the subject_id changes. """
        self.section_ids = False

    @api.depends('school_year_id', 'user_id')
    def _compute_available_subjects(self):
        for record in self:
            subject_ids = []
            if record.school_year_id and record.user_id:
                employee_teacher_id = self.env['hr.employee'].search([('user_id', '=', record.user_id.id)], limit=1)
                if employee_teacher_id:
                    subject_offerings = self.env['esmis.subject.offerings'].search([
                        ('teacher_id', '=', employee_teacher_id.id),
                        ('section_id.year_id', '=', record.school_year_id.id)
                    ])
                    subject_ids = subject_offerings.mapped('subject_id.id')
            record.available_subject_ids = [(6, 0, subject_ids)]

    @api.depends('subject_id', 'user_id')
    def _compute_available_sections(self):
        for record in self:
            section_ids = []
            if record.subject_id and record.user_id:
                employee_teacher_id = self.env['hr.employee'].search([('user_id', '=', record.user_id.id)], limit=1)
                if employee_teacher_id:
                    subject_offerings = self.env['esmis.subject.offerings'].search([
                        ('teacher_id', '=', employee_teacher_id.id),
                        ('subject_id', '=', record.subject_id.id)
                    ])
                    section_ids = subject_offerings.mapped('section_id.id')
            record.available_section_ids = [(6, 0, section_ids)]

    @api.depends('section_ids', 'subject_id', 'user_id')
    def _get_students_to_enroll(self):
        """ Get all enrolled students based on the
            school year, subject, section, and teacher assigned """
        for record in self:
            student_ids = []
            if record.subject_id and record.user_id and record.section_ids:
                # Find the employee record for the current user (Course Responsible User)
                employee_teacher_id = self.env['hr.employee'].search([('user_id', '=', record.user_id.id)], limit=1)
                if employee_teacher_id:
                    # Search for subject offerings based on the teacher, subject, and sections
                    subject_offerings = self.env['esmis.subject.offerings'].search([
                        ('teacher_id', '=', employee_teacher_id.id),
                        ('subject_id', '=', record.subject_id.id),
                        ('section_id', 'in', record.section_ids.ids)
                    ])
                    # Get the enrollment records related to the subject offerings
                    enrollment_records = self.env['esmis.subject.enrolled'].search([
                        ('subject_id', 'in', subject_offerings.ids)
                    ])
                    # Extract student IDs from enrollment records
                    student_ids = enrollment_records.mapped('enrollment_id.student_id.id')
            record.students_to_enroll = [(6, 0, student_ids)]

    # def action_add_students_to_channel(self):
    # """ test button action para maenroll students sa course """
    #     if self.students_to_enroll:
    #         self._action_add_members(self.students_to_enroll)

    def action_add_students_to_channel(self):
        """ Add students to the channel if they are not already added. """
        for record in self:
            if not record.students_to_enroll:
                continue
            
            # Get existing students that are already enrolled to the channel
            existing_partners = self.env['slide.channel.partner'].search([
                ('channel_id', 'in', record.ids),
                ('partner_id', 'in', record.students_to_enroll.ids)
            ])
            
            # If students are already enrolled, raise a validation error
            if existing_partners:
                existing_partner_ids = existing_partners.mapped('partner_id.id')
                existing_partner_names = existing_partners.mapped('partner_id.name')
                raise UserError(_('The following students are already enrolled in the channel: %s') % ', '.join(existing_partner_names))

            # Continue with adding new students if no existing students were found
            target_partners = self.env['res.partner'].browse(record.students_to_enroll.ids)
            record._action_add_members(target_partners)
        
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("eSMIS LMS: Course"),
                "message": _("Success! All Students have been enrolled."),
                "sticky": True,
                "type": "success",
                "next": {
                    "type": "ir.actions.act_window_close",
                },
            },
        }

    # @api.onchange('school_year_id')
    # def _get_subject_assigned(self):
    #     """ This method will dynamically set the domain for the subject_id
    #         field based on the teacher's assignment on esmis.subject.offerings """
    #     self.subject_id = False

    #     # Find the employee record for the current user(Course Responsible User)
    #     employee_teacher_id = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)
        
    #     if employee_teacher_id:
    #         # Get the subjects that the teacher is assigned to
    #         subject_offerings = self.env['esmis.subject.offerings'].search([
    #             ('teacher_id', '=', employee_teacher_id.id),
    #             ('section_id.year_id', '=', self.school_year_id.id)
    #         ])
            
    #         # Extract the subject IDs
    #         subject_ids = subject_offerings.mapped('subject_id.id')

    #         # Set the domain for the subject_id field
    #         return {'domain': {'subject_id': [('id', 'in', subject_ids)]}}
    #     else:
    #         # If no teacher is found, return an empty domain
    #         return {'domain': {'subject_id': [('id', '=', False)]}}
        
    # @api.onchange('subject_id')
    # def _get_section_assigned(self):
    #     """ This method will dynamically set the domain for the section_ids
    #         field based on the subject and teacher's assignment on esmis.subject.offerings """
    #     self.section_ids = False

    #     employee_teacher_id = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)

    #     if employee_teacher_id:
    #         # Get the subject offering line record based on the subject_id
    #         # the employee_teacher_id is assigned to
    #         subject_offerings = self.env['esmis.subject.offerings'].search([
    #             ('teacher_id', '=', employee_teacher_id.id),
    #             ('subject_id', '=', self.subject_id.id),
    #         ])
            
    #         # Extract the sections IDs
    #         section_list_ids = subject_offerings.mapped('section_id.id')
    #         year_list_ids = subject_offerings.mapped('section_id.year_id.id')
    #         # Set the domain for the section_ids field
    #         return {
    #             'domain': {'section_ids': [('id', 'in', section_list_ids),('year_id', 'in', year_list_ids)]}
    #         }
    #     else:
    #         # If no teacher is found, return an empty domain
    #         return {'domain': {'section_ids': [('id', '=', False)]}}