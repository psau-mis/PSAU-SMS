from odoo.http import request, route, Controller
from odoo.addons.portal.controllers.portal import CustomerPortal

class EsmisParentPortalController(CustomerPortal):
    
    @route(['/parent/<string:route>'], type='http', auth="user", website=True)
    def parent_portal(self, route="child",**kw):
        user = request.env.user
        is_parent = user.is_parent
        page_name = route
        # children = request.env['res.partner'].sudo().search([('is_student', '=', True)])

        parent_id = user.parent_record_id
        children = parent_id.child_ids

        if not is_parent:
            return request.redirect('/')

        context = {
            'route': route,
            'call': 'esmis_website_portal.portal_main_layout',
            'user': user,
            'is_parent': is_parent,
            'parent': parent_id,
            'children': children,
            'page_name': page_name,
        }

        return request.render("esmis_website_portal.portal_main_layout", context)

    @route(['/parent/child/<model("res.partner"):child_id>'], type='http', auth="user", website=True)
    def child_records(self, child_id, route="child_records",**kw):
        route = "child_records"
        user = request.env.user
        is_parent = user.is_parent
        page_name = route

        if not is_parent:
            return request.redirect('/')

        context = {
            'route': route,
            'call': 'esmis_website_portal.portal_main_layout',
            'child_id': child_id,
            'user': user,
            'is_parent': is_parent,
            'page_name': page_name,
        }

        return request.render("esmis_website_portal.portal_main_layout", context)
    
    @route(['/parent/child/<model("res.partner"):child_id>/<string:route>'], type='http', auth="user", website=True, methods=['POST', 'GET'])
    def child_inner_records(self, child_id, route="child_info",**kw):
        user = request.env.user
        is_parent = user.is_parent
        page_name = route

        if child_id.age:
            age_parts = child_id.age.split(' ')
            if len(age_parts) == 3:
                years = age_parts[0].replace('y', '')
                months = age_parts[1].replace('m', '')
                formatted_age = f"{years}.{months}"
            else:
                formatted_age = ''

        if not is_parent:
            return request.redirect('/')

        subject_school_years = request.env['esmis.subject.enrolled'].sudo().search([
            ('enrollment_id.student_id', '=', child_id.id),
        ]).mapped('enrollment_id.school_year_id')

        subject_school_year_id = int(kw.get('subject_school_year_id', subject_school_years and subject_school_years[0].id or 0))

        enrollments = request.env['esmis.subject.enrolled'].sudo().search([
            ('student_name', '=', child_id.name),
            ('enrollment_id.school_year_id', '=', subject_school_year_id),
        ])
        enrolled_subjects = enrollments.mapped('subject_id')

        total_units = sum(subject.units for subject in enrollments.mapped('subject_id'))
        total_lab_units = sum(subject.lab_hrs_week for subject in enrollments.mapped('subject_id'))
        total_lec_units = sum(subject.lec_hrs_week for subject in enrollments.mapped('subject_id'))

        grade_school_years = request.env['esmis.grade.management.line'].sudo().search([
            ('student_id', '=', child_id.id),
            ('grade_id.status', '=', 'posted'),
        ]).mapped('grade_id.school_year_id')

        grade_school_year_id = int(kw.get('grade_school_year_id', grade_school_years and grade_school_years[0].id or 0))

        grades = request.env['esmis.grade.management.line'].sudo().search([
            ('student_id', '=', child_id.id),
            ('grade_id.status', '=', 'posted'),
            ('grade_id.school_year_id', '=', grade_school_year_id),
        ])

        enrollment_ids = request.env['esmis.enrollment'].sudo().search([
            ('student_id', '=', child_id.id),
            ('status', '=', 'enrolled')
        ])
        # enrollment_section = ', '.join(enrollment_ids.mapped('section_id.name'))

        request.session['child_id'] = child_id.id

        current_parent = request.env['parent.record'].sudo().search([('email', '=', user.email)], limit=1)
        grievances_created_by_user = request.env['esmis.grievance'].sudo().search([
            ('grievance_by', '=', 'parent'),
            ('parent_id', '=', current_parent.id),
        ])
        is_child_in_parent = child_id.id in current_parent.child_ids.ids

        context = {
            'route': route,
            'call': 'esmis_website_portal.portal_main_layout',
            'child_id': child_id,
            'user': user,
            'is_parent': is_parent,
            'formatted_age': formatted_age,
            'page_name': page_name,
            'enrollment_ids': enrollment_ids,
            # 'enrollment_section': enrollment_section,
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
                if is_child_in_parent:
                    grievance_values = {
                        'grievance_by': 'parent',
                        'parent_id': current_parent.id,
                        'student_id': child_id.id,
                        'grievance_subject': grievance_subject,
                        'grievance_category': grievance_category,
                        'grievance_description': grievance_description,
                        'state': 'submitted',
                    }

                    request.env['esmis.grievance'].sudo().create(grievance_values)
                    success = "Successfully submitted Grievance Form"
                    context['success_msg'] = success
                else:
                    return request.redirect('/')
            else:
                context['error_list'] = error_list
        else:
            print("The Method Called Is GET")

        return request.render("esmis_website_portal.portal_main_layout", context)

    @route('/parent/filter_child_grades', type="json", auth="user")
    def filter_child_grades(self, **kw):
        student_id = request.env.user.partner_id.id
        child_id = request.session.get('child_id')
        grade_school_year_id = int(kw.get('grade_school_year_id', 0) or 0)
        child_grades_data = self.get_child_grades_data(child_id, grade_school_year_id)

        return child_grades_data

    def get_child_grades_data(self, student_id, grade_school_year_id):
        user = request.env.user
        child_id = request.session.get('child_id')
        child = request.env['res.partner'].sudo().browse(child_id)
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
                'final_eq': grade.final_eq,
                'remarks': grade.remarks,
            }
            formatted_grades.append(formatted_grade)

        return {
            'grades': formatted_grades,
            'child_id': child_id,
        }

    @route('/parent/filter_child_subjects', type="json", auth="user")
    def filter_child_subjects(self, **kw):
        user = request.env.user
        child_id = request.session.get('child_id')
        subject_school_year_id = int(kw.get('subject_school_year_id', 0) or 0)
        child_subjects_data = self.get_child_subjects_data(child_id, subject_school_year_id)
        
        return child_subjects_data

    def get_child_subjects_data(self, student_id, subject_school_year_id):
        user = request.env.user
        child_id = request.session.get('child_id')

        enrollment_record = request.env['esmis.subject.enrolled'].sudo().search([
            ('enrollment_id.student_id', '=', student_id),
            ('enrollment_id.school_year_id', '=', subject_school_year_id),
        ])
        
        enrolled_subjects = enrollment_record.mapped('subject_id')

        # total_units = sum(subject.units for subject in enrolled_subjects)
        # total_lec_units = sum(subject.lec_hrs_week_1 for subject in enrolled_subjects)
        # total_lab_units = sum(subject.lab_hrs_week_1 for subject in enrolled_subjects)
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
            'child_id': child_id,
        }
    
    @route('/parent/download_cor/<int:subject_school_year_id>/<string:filename>', type='http', auth="user", website=True)
    def download_cor(self, filename, subject_school_year_id, **kw):
        user = request.env.user
        child_id = request.session.get('child_id')
        child = request.env['res.partner'].sudo().browse(child_id)

        if user.is_parent:
            # enrollment_id = user.enrollment_ids and user.enrollment_ids[0]
            enrollment_ids = child.enrollment_ids
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

        return request.redirect('/parent/child')
    
    @route('/parent/download_cog/<int:subject_school_year_id>/<string:filename>', type='http', auth="user", website=True)
    def download_cog(self, filename, subject_school_year_id, **kw):
        user = request.env.user
        child_id = request.session.get('child_id')
        child = request.env['res.partner'].sudo().browse(child_id)

        if user.is_parent:
            # enrollment_id = user.enrollment_ids and user.enrollment_ids[0]
            grades_ids = child.grades_ids
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

        return request.redirect('/parent/child')

    @route(['/parent/child/<model("res.partner"):child_id>/<model("esmis.grievance"):grievance_id>/<string:route>'], type='http', auth="user", website=True)
    def grievance_details(self, child_id, grievance_id, route="grievance_details", **kw):
        user = request.env.user
        is_parent = user.is_parent
        page_name = route

        context = {
            'route': route,
            'page_name': page_name,
            'is_parent': is_parent,
            'child_id': child_id,
            'grievance_id': grievance_id,
        }
        return request.render("esmis_website_portal.portal_main_layout", context)
