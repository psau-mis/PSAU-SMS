from odoo.http import request, Controller, route

class WebsiteAdmissionController(Controller):

    @route('/admission/register', type='http', auth="public", website=True)
    def admission_register(self, redirect=None, **kwargs):
        response = request.render("esmis_website.admission_registration")
        return response


    # test for one flow Undergraduate(applicant type) + New Student(admission type)
    @route('/admission', type='http', auth="public", website=True)
    def admission_setup(self, **kwargs):
        return request.render('esmis_website.admission_setup_template')

    @route('/setup_admission', type='http', auth="public", website=True, methods=['POST'])
    def setup_admission(self, **post):
        
        applicant_type = post.get('select_level')
        admission_type = post.get('select_admission')
        admission_type_grad = post.get('select_admission_grad')

        
        request.session['applicant_type'] = applicant_type
        request.session['admission_type'] = admission_type
        request.session['admission_type_grad'] = admission_type_grad

        
        if applicant_type == 'Undergraduate':
            if admission_type == 'New Student':
                return request.redirect('/admission/undergraduate/new_student')
            elif admission_type == 'Transferee':
                return request.redirect('/admission/undergraduate/transferee')
            elif admission_type == 'Second Courser':
                return request.redirect('/admission/undergraduate/second_courser')
            elif admission_type == 'Foreign Applicant':
                return request.redirect('/admission/undergraduate/foreign_applicant')
        elif applicant_type == 'Graduate':
            if admission_type_grad == 'Graduate Level: Masteral (New Student)':
                return request.redirect('/admission/graduate/masteral_new_student')
            elif admission_type_grad == 'Graduate Level: Masteral (Transferee)':
                return request.redirect('/admission/graduate/masteral_transferee')
            elif admission_type_grad == 'Graduate Level: Doctoral (New Student)':
                return request.redirect('/admission/graduate/doctoral_new_student')
            elif admission_type_grad == 'Graduate Level: Doctoral (Transferee)':
                return request.redirect('/admission/graduate/doctoral_transferee')
        else:
            return request.redirect('/admission')

    # Undergraduate Form Routes
    @route('/admission/undergraduate/new_student', type='http', auth="public", website=True)
    def undergraduate_new_student(self, **kwargs):
        if not request.session.get('applicant_type') or not request.session.get('admission_type'):
            return request.redirect('/admission')

        # return request.redirect('/')
        return request.render('esmis_website.undergraduate_new_student')


# For testing ~ Jonas
# from odoo import http
# from odoo.http import request, Controller, route

# class AdmissionController(Controller):

#     @route('/admission', type='http', auth="public", website=True)
#     def admission_setup(self, **kwargs):
#         return request.render('esmis_website.admission_setup_template')

#     @route('/setup_admission', type='http', auth="public", website=True, methods=['POST'])
#     def setup_admission(self, **post):
        
#         applicant_type = post.get('select_level')
#         admission_type = post.get('select_admission')
#         admission_type_grad = post.get('select_admission_grad')

        
#         request.session['applicant_type'] = applicant_type
#         request.session['admission_type'] = admission_type
#         request.session['admission_type_grad'] = admission_type_grad

        
#         if applicant_type == 'Undergraduate':
#             if admission_type == 'New Student':
#                 return request.redirect('/admission/undergraduate/new_student')
#             elif admission_type == 'Transferee':
#                 return request.redirect('/admission/undergraduate/transferee')
#             elif admission_type == 'Second Courser':
#                 return request.redirect('/admission/undergraduate/second_courser')
#             elif admission_type == 'Foreign Applicant':
#                 return request.redirect('/admission/undergraduate/foreign_applicant')
#         elif applicant_type == 'Graduate':
#             if admission_type_grad == 'Graduate Level: Masteral (New Student)':
#                 return request.redirect('/admission/graduate/masteral_new_student')
#             elif admission_type_grad == 'Graduate Level: Masteral (Transferee)':
#                 return request.redirect('/admission/graduate/masteral_transferee')
#             elif admission_type_grad == 'Graduate Level: Doctoral (New Student)':
#                 return request.redirect('/admission/graduate/doctoral_new_student')
#             elif admission_type_grad == 'Graduate Level: Doctoral (Transferee)':
#                 return request.redirect('/admission/graduate/doctoral_transferee')
#         else:
#             return request.redirect('/admission')

#     # Undergraduate Form Routes
#     @route('/admission/undergraduate/new_student', type='http', auth="public", website=True)
#     def undergraduate_new_student(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.undergraduate_new_student')
        
#     @route('/admission/undergraduate/transferee', type='http', auth="public", website=True)
#     def undergraduate_transferee(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.undergraduate_transferee')
    
#     @route('/admission/undergraduate/second_courser', type='http', auth="public", website=True)
#     def undergraduate_second_courser(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.undergraduate_second_courser')
    
#     @route('/admission/undergraduate/foreign_applicant', type='http', auth="public", website=True)
#     def undergraduate_foreign_applicant(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.undergraduate_foreign_applicant')

#     # Graduate Form Routes
#     @route('/admission/graduate/masteral_new_student', type='http', auth="public", website=True)
#     def graduate_masteral_new_student(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type_grad'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.graduate_masteral_new_student')
    
#     @route('/admission/graduate/masteral_transferee', type='http', auth="public", website=True)
#     def graduate_masteral_transferee(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type_grad'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.graduate_masteral_transferee')
    
#     @route('/admission/graduate/doctoral_new_student', type='http', auth="public", website=True)
#     def graduate_doctoral_new_student(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type_grad'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.graduate_doctoral_new_student')
    
#     @route('/admission/graduate/doctoral_transferee', type='http', auth="public", website=True)
#     def graduate_doctoral_transferee(self, **kwargs):
#         if not request.session.get('applicant_type') or not request.session.get('admission_type_grad'):
#             return request.redirect('/admission')

#         return request.render('esmis_website.graduate_doctoral_transferee')
