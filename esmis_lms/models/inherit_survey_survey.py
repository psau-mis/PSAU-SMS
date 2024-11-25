from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError

class InheritSurvey(models.Model):
    _inherit = "survey.survey"

    # inherited default fields
    user_input_ids = fields.One2many('survey.user_input', 'survey_id', string='User responses', readonly=True, groups='survey.group_survey_user,esmis_base.group_esmis_teacher')
    access_mode = fields.Selection([
        ('public', 'Anyone with the link'),
        ('token', 'Invited people only')
    ], string='Access Mode', default='token', required=True)
    users_login_required = fields.Boolean('Require Login', default=True, help="If checked, users have to login before answering even with a valid token.")

    # custom fields
    is_teacher = fields.Boolean(compute='_compute_is_teacher_group', store=False)
    school_year_id = fields.Many2one('esmis.school.year', String='School Year', required=True)
    subject_id = fields.Many2one('esmis.subjects', string='Subject')
    section_ids = fields.Many2many('esmis.sections', string='Sections')

    # Computed fields for dynamic domains domain=[(...)] is decalared on xml form view inherit_survey_views.xml
    available_subject_ids = fields.Many2many('esmis.subjects', compute='_compute_available_subjects', string='Available Subjects')
    available_section_ids = fields.Many2many('esmis.sections', compute='_compute_available_sections', string='Available Sections')

    students_to_enroll = fields.Many2many('res.partner', string='Students to Enroll', compute='_get_students_to_enroll')

    @api.depends('user_id')
    def _compute_is_teacher_group(self):
        """ This function is used to make the user_id field in the inherited form view of
            survey.survey model(inherit_survey_views) to be readonly=True if the user_id group is 
            in Teacher user group('esmis_base.group_esmis_teacher')"""
        teacher_group = self.env.ref('esmis_base.group_esmis_teacher')
        for survey in self:
            user = survey.user_id
            if user:
                survey.is_teacher = teacher_group in user.groups_id
            else:
                survey.is_teacher = False

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
                # Find the employee record for the current user (Examination Responsible User)
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

    # def action_send_exam_to_students(self):
    #   """ test button action para ma invite students sa exam """
    #    for record in self:
    #        if not record.students_to_enroll:
    #            continue
    #
    #        target_students = self.env['res.partner'].browse(record.students_to_enroll.ids)
    #
    #        return record.with_context(
    #            default_partner_ids=target_students.ids
    #        ).action_send_survey()

    # this behaves like the def action_send_survey(self) it will open a wizard with recipients already filled up
    # ready for sending invitations to the students(based on students_to_enroll)
    def action_send_exam_to_students(self):
        """ Add students to the Exam if they are not already added. """
        """ For this function we used def action_send_survey() to send/invite student for the exam """
        for record in self:
            if not record.students_to_enroll:
                continue

            # Get existing students that are already invited in the exam
            existing_user_inputs = self.env['survey.user_input'].search([
                ('survey_id', '=', record.id),
                ('partner_id', 'in', record.students_to_enroll.ids)
            ])
            
            # If students are already invited(True), raise a validation error ***Note: UserError === ValidationError
            if existing_user_inputs:
                existing_partner_names = existing_user_inputs.mapped('partner_id.name')
                raise UserError(_('The following students are already invited to the exam: %s') % ', '.join(existing_partner_names))

            # Prepare the list of emails and students to invite
            partners = self.env['res.partner']
            emails = []
            for student in record.students_to_enroll:
                if student.id:
                    partners |= student
                elif student.email:
                    emails.append(student.email)

            # Use the action_send_survey method with the correct values taht will be used on the email template('survey.mail_template_user_input_invite')
            return record.with_context(
                default_partner_ids=partners.ids,
                default_emails=','.join(emails)
            ).action_send_survey()

        # irrelevant because the invite function uses wizard window   
        # return {
        #     "type": "ir.actions.client",
        #     "tag": "display_notification",
        #     "params": {
        #         "title": _("eSMIS LMS: Examination"),
        #         "message": _("Success! All Students have been invited to the Exam."),
        #         "sticky": True,
        #         "type": "success",
        #         "next": {
        #             "type": "ir.actions.act_window_close",
        #         },
        #     },
        # }


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
    #         return {
    #             'domain': {'subject_id': [('id', 'in', subject_ids)]}
    #         }
    #     else:
    #         # If no teacher is found, return an empty domain
    #         return {
    #             'domain': {'subject_id': [('id', '=', False)]}
    #         }
        
    # @api.onchange('subject_id')
    # def _onchange_subject_id(self):
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
    #         return {
    #             'domain': {'section_ids': [('id', '=', False)]}
    #         }