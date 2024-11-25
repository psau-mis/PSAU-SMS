from odoo.http import request, route, Controller
from odoo.addons.portal.controllers.portal import CustomerPortal

class EsmisStudentPortalController(CustomerPortal):

    @route(['/portal/<string:route>'], type='http', auth="user", website=True, methods=['POST', 'GET'])
    def student_portal(self, route="dashboard", **kw):
        user = request.env.user
        is_student = user.is_student
        page_name = route
        student_id = user.id

        evaluation_records = request.env['faculty.evaluation'].sudo().search([
            ('state', '=', 'in_progress'), ('evaluation_lines.student_id', '=', user.partner_id.id)
        ])

        grievances_created_by_user = request.env['esmis.grievance'].sudo().search([
            ('grievance_by', '=', 'student'),
            ('student_id', '=', user.partner_id.id),
        ])

        grade_school_years = request.env['esmis.grade.management.line'].sudo().search([
            ('student_id', '=', user.partner_id.id),
            ('grade_id.status', '=', 'posted'),
        ]).mapped('grade_id.school_year_id')

        subject_school_years = request.env['esmis.subject.enrolled'].sudo().search([
            ('enrollment_id.student_id', '=', user.partner_id.id),
        ]).mapped('enrollment_id.school_year_id')

        grade_school_year_id = int(kw.get('grade_school_year_id', grade_school_years and grade_school_years[0].id or 0))
        subject_school_year_id = int(kw.get('subject_school_year_id', subject_school_years and subject_school_years[0].id or 0))

        grades = request.env['esmis.grade.management.line'].sudo().search([
            ('student_id', '=', user.partner_id.id),
            ('grade_id.status', '=', 'posted'),
            ('grade_id.school_year_id', '=', grade_school_year_id),
        ])
        enrollments = request.env['esmis.subject.enrolled'].sudo().search([
            ('student_name', '=', user.name),
            ('enrollment_id.school_year_id', '=', subject_school_year_id),
        ])
        enrolled_subjects = enrollments.mapped('subject_id')

        total_units = enrollments.enrollment_id.total_units
        total_lec_units = enrollments.enrollment_id.total_lec_units
        total_lab_units = enrollments.enrollment_id.total_lab_units

        # Format the age string to "23.6" format
        if user.age:
            age_parts = user.age.split(' ')
            if len(age_parts) == 3:
                years = age_parts[0].replace('y', '')
                months = age_parts[1].replace('m', '')
                formatted_age = f"{years}.{months}"
            else:
                formatted_age = ''
        
        if not is_student:
            return request.redirect('/')
        
        context = {
            'call': 'esmis_website_portal.portal_main_layout',
            'route': route,
            'user': user,
            'is_student': is_student,
            'page_name': page_name,
            'formatted_age': formatted_age,
            'enrolled_subjects': enrolled_subjects,
            'student_id': student_id,
            'teachers': evaluation_records,
            'grades': grades,
            'grade_school_years': grade_school_years,
            'subject_school_years': subject_school_years,
            'grade_school_year_id': grade_school_year_id,
            'subject_school_year_id': subject_school_year_id,
            'total_units': total_units,
            'total_lab_units': total_lab_units,
            'total_lec_units': total_lec_units,
            'grievance_list': grievances_created_by_user,
        }

        return request.render("esmis_website_portal.portal_main_layout", context)
    
    @route(['/portal/<string:route>/<string:grievance_route>/<model("esmis.grievance"):grievance_id>'], type='http', auth="user", website=True)
    def student_grievance_list(self, grievance_id, route="student_grievance", grievance_route="student_grievance_list", **kw):
        user = request.env.user
        is_student = user.is_student
        page_name = grievance_route

        enrollment_ids = request.env['esmis.enrollment'].sudo().search([
            ('student_id', '=', user.partner_id.id),
            ('status', '=', 'enrolled')
        ])

        context = {
            'user': user,
            'grievance_route': grievance_route,
            'page_name': page_name,
            'is_student': is_student,
            'enrollment_ids': enrollment_ids,
            'grievance_id': grievance_id,
        }
        return request.render("esmis_website_portal.portal_main_layout", context)
    
    @route(['/portal/<string:route>/<string:grievance_route>'], type='http', auth="user", website=True, methods=['POST', 'GET'])
    def student_grievance_form(self, route="student_grievance", grievance_route="student_grievance_form", **kw):
        user = request.env.user
        is_student = user.is_student
        page_name = grievance_route
        student_id = user.id

        enrollment_ids = request.env['esmis.enrollment'].sudo().search([
            ('student_id', '=', user.partner_id.id),
            ('status', '=', 'enrolled')
        ])

        context = {
            'call': 'esmis_website_portal.portal_main_layout',
            'grievance_route': grievance_route,
            'user': user,
            'is_student': is_student,
            'page_name': page_name,
            'student_id': student_id,
            'enrollment_ids': enrollment_ids,
        }
        if request.httprequest.method == 'POST':
            grievance_subject = kw.get('grievance_subject')
            grievance_category = kw.get('grievance_category')
            grievance_description = kw.get('grievance_description')

            error_list = []
            if not grievance_subject:
                error_list.append("Grievance Subject is required")
            if grievance_category == 'none':
                error_list.append("Grievance Category is required")
            elif grievance_category not in ['academic', 'non_academic']:
                error_list.append("Grievance Category is NOT VALID")
            if not grievance_description:
                error_list.append("Grievance Description is required")

            if not error_list:
                grievance_values = {
                    'grievance_by': 'student',
                    # 'parent_id': user.partner_id.parent_record_id.id,
                    'student_id': user.partner_id.id,
                    'grievance_subject': grievance_subject,
                    'grievance_category': grievance_category,
                    'grievance_description': grievance_description,
                    'state': 'submitted',
                }

                request.env['esmis.grievance'].sudo().create(grievance_values)
                success = "Successfully submitted Grievance Form"
                context['success_msg'] = success
            else:
                context.update({
                    'grievance_subject': grievance_subject,
                    'grievance_category': grievance_category,
                    'grievance_description': grievance_description,
                })
                context['error_list'] = error_list

        return request.render("esmis_website_portal.portal_main_layout", context)
    
    @route('/portal/filter_grade_lines', type="json", auth="user")
    def filter_grade_lines(self, **kw):
        student_id = request.env.user.partner_id.id
        grade_school_year_id = int(kw.get('grade_school_year_id', 0) or 0)
        grades_data = self.get_grades_data(student_id, grade_school_year_id)

        return grades_data

    def get_grades_data(self, student_id, grade_school_year_id):
        user = request.env.user

        grades = request.env['esmis.grade.management.line'].sudo().search([
            ('student_id', '=', student_id),
            ('grade_id.status', '=', 'posted'),
            ('grade_id.school_year_id', '=',int(grade_school_year_id)),
        ])

        formatted_grades = []
        for grade in grades:
            formatted_grade = {
                'subject_code': grade.grade_id.subject_id.subject,
                'subject_description': grade.grade_id.subject_id.descriptive_title,
                'section': grade.grade_id.section_id.name,
                'subject_units': grade.grade_id.subject_id.subject_unit,
                're_exam': grade.re_exam,
                'final_eq': grade.final_eq,
                'remarks': grade.remarks,
            }
            formatted_grades.append(formatted_grade)

        return {'grades': formatted_grades}
    
    @route('/portal/filter_enrolled_subjects', type="json", auth="user")
    def filter_enrolled_subjects(self, **kw):
        user = request.env.user
        subject_school_year_id = int(kw.get('subject_school_year_id', 0) or 0)
        enrolled_subjects_data = self.get_enrolled_subjects_data(user.name, subject_school_year_id)
        
        return enrolled_subjects_data

    def get_enrolled_subjects_data(self, student_name, subject_school_year_id):
        user = request.env.user

        enrollment_record = request.env['esmis.subject.enrolled'].sudo().search([
            ('student_name', '=', student_name),
            ('enrollment_id.school_year_id', '=', subject_school_year_id),
        ])
        
        enrolled_subjects = enrollment_record.mapped('subject_id')

        total_units = enrollment_record.enrollment_id.total_units
        total_lec_units = enrollment_record.enrollment_id.total_lec_units
        total_lab_units = enrollment_record.enrollment_id.total_lab_units
        
        total_units_array = [{
            'total_units': total_units,
            'total_lec_units': total_lec_units,
            'total_lab_units': total_lab_units,
        }]

        formatted_enrolled_subjects = []
        for enrolled_subject in enrolled_subjects:
            formatted_subject = {
                'subject_code': enrolled_subject.subject_id.subject,
                'subject_desc': enrolled_subject.subject_id.descriptive_title,
                'units': enrolled_subject.units,
                'lec_hrs_week': enrolled_subject.lec_hrs_week_1.unit,
                'lab_hrs_week': enrolled_subject.lab_hrs_week_1.unit,
                'section': enrolled_subject.section_id.name,
                'sched_display': enrolled_subject.sched_display,
                'teacher_name': enrolled_subject.teacher_id.name,
            }
            formatted_enrolled_subjects.append(formatted_subject)

        return {
            'enrolled_subjects': formatted_enrolled_subjects,
            'total_units_array': total_units_array,
            'student_no_undg': user.student_no_undg,
            'student_no_grad' : user.student_no_grad,
        }

    @route('/portal/student_cor_download/<int:subject_school_year_id>/<string:filename>', type='http', auth="user", website=True)
    def student_cor_download(self, filename, subject_school_year_id, **kw):
        user = request.env.user

        if user.is_student:
            # enrollment_id = user.enrollment_ids and user.enrollment_ids[0]
            enrollment_ids = user.enrollment_ids
            if enrollment_ids and len(enrollment_ids) >= subject_school_year_id:
                enrollment_id = enrollment_ids[subject_school_year_id - 1]

                if enrollment_id:
                    filename = 'COR - %s' % (user.student_no_undg) if user.student_no_undg else 'COR - %s' % (user.student_no_grad)

                    return self._show_report(
                        model=enrollment_id,
                        report_type='pdf',
                        report_ref='esmis_curriculum.action_certificate_of_registration',
                        download=kw.get('download'),
                    )

        return request.redirect('/portal/subjects')
    
    @route('/portal/student_cog_download/<int:subject_school_year_id>/<string:filename>', type='http', auth="user", website=True)
    def student_cog_download(self, filename, subject_school_year_id, **kw):
        user = request.env.user

        if user.is_student:
            # enrollment_id = user.enrollment_ids and user.enrollment_ids[0]
            grades_ids = user.grades_ids
            if grades_ids and len(grades_ids) >= subject_school_year_id:
                grade_id = grades_ids[subject_school_year_id - 1]

                if grade_id:
                    filename = 'COG - %s' % (user.student_no_undg) if user.student_no_undg else 'COR - %s' % (user.student_no_grad)

                    return self._show_report(
                        model=grade_id,
                        report_type='pdf',
                        report_ref='esmis_website_portal.action_portal_certificate_of_grades',
                        download=kw.get('download'),
                    )

        return request.redirect('/portal/grades')
    
    @route(['/portal/faculty_evaluation/<model("hr.employee"):teacher_id>'], type='http', auth="user", website=True, methods=['POST', 'GET'])
    def faculty_evaluation(self, teacher_id, route="faculty_form",**kw):
        route = "faculty_form"
        user = request.env.user
        is_student = user.is_student
        page_name = route

        ratings = request.env['question.ratings'].sudo().search([], order='id desc')

        evaluation_rating_line = request.env['evaluation.rating.line'].sudo().search([
            ('evaluation_id.teacher_id', '=', teacher_id.id),
            ('evaluation_id.state', 'not in', ['draft', 'cancel']),
            ('student_id', '=', user.partner_id.id)
        ], order='id desc')
        questions_to_answer = evaluation_rating_line.mapped('question_ratings')
        if evaluation_rating_line.is_submitted:
            return request.redirect('/portal/faculty_evaluation')

        if not is_student:
            return request.redirect('/')

        vals = {
            'call': 'esmis_website_portal.portal_main_layout',
            'teacher_id': teacher_id,
            'route' : route,
            'user': user,
            'is_student': is_student,
            'questions': questions_to_answer,
            'ratings': ratings,
            'page_name': page_name,
        }

        if request.httprequest.method == 'POST':
            form_data = {}  # To store the form input(type:radio) data
            all_questions_answered = True

            for question_to_answer in questions_to_answer:
                rating_value = kw.get(str(question_to_answer.question_id.id))
                form_data[str(question_to_answer.question_id.id)] = rating_value

                if not rating_value:  # Check if all questions are answered
                    all_questions_answered = False
                    break

            student_comment = kw.get('student_comment', '')

            if all_questions_answered:
                for question_to_answer in questions_to_answer:
                    rating_value = form_data.get(str(question_to_answer.question_id.id))
                    question_to_answer.write({'rating': rating_value})
                
                evaluation_rating_line.write({'is_submitted': True, 'comment': student_comment})

                success_message = "Your evaluation has been submitted successfully!"
                vals['success_message'] = success_message
                return request.redirect("/portal/faculty_evaluation")
            else:
                error_message = "Please select a rating for all questions before submitting."
                vals['error_message'] = error_message
                vals['form_data'] = form_data #pasa pabalik sa template filled up inputs

        return request.render("esmis_website_portal.portal_main_layout", vals)