from odoo.http import request, Controller, route

class NewWebsiteAdmissionController(Controller):
    
    # display applicant type selection form
    @route('/admission/select_applicant_type', type='http', auth="public", website=True, methods=['GET'])
    def select_applicant_type(self, **post):
        return request.render("esmis_website.applicant_type_selection")

    # record the session data from applicant type selection
    @route('/admission/select_applicant_type', type='http', auth="public", website=True, methods=['POST'])
    def select_applicant_type_post(self, **post):
        #we need this to set up t-if to display appropriate admission type selection for undergrad and graduate
        applicant_type = post.get('select_level')
        request.session['applicant_type'] = applicant_type
        #redirect to admission type selection
        return request.redirect('/admission/select_admission_type?applicant_type=%s' % applicant_type)

    #display admission type and preferred SY selection form
    @route('/admission/select_admission_type', type='http', auth="public", website=True, methods=['GET'])
    def select_admission_type(self, **post):
        applicant_type = request.params.get('applicant_type')  # Get the applicant_type and pass it
        applicant_type_check = request.session.get('applicant_type')
        
        if not applicant_type_check:
            # If applicant_type is not set, redirect to select_applicant_type
            return request.redirect('/admission/reset')

        return request.render("esmis_website.admission_type_selection", {'applicant_type': applicant_type})

    #record the admission type and preferred SY
    @route('/admission/select_admission_type', type='http', auth="public", website=True, methods=['POST'])
    def select_admission_type_post(self, **post):
        admission_type = post.get('select_admission')
        select_sy_year = post.get('select_sy_year')

        request.session['admission_type'] = admission_type
        request.session['select_sy_year'] = select_sy_year

        #redirect to the main form
        return request.redirect('/admission/register_new')

    #display the main form
    @route('/admission/register_new', type='http', auth="public", website=True)
    def admission_register_new(self, redirect=None, **kwargs):
        # pass all session data from application type, admission type, and preferred SY
        applicant_type = request.session.get('applicant_type')
        admission_type = request.session.get('admission_type')
        select_sy_year = request.session.get('select_sy_year')

        #prevent user from directly going in this route
        if not applicant_type or not admission_type:
            # If either applicant_type or admission_type is not set, redirect to select_applicant_type
            return request.redirect('/admission/reset')

        context = {
            'applicant_type': applicant_type,
            'admission_type': admission_type,
            'select_sy_year': select_sy_year,
        }

        response = request.render("esmis_website.admission_registration_new", context)
        return response

    # reset for(applicant type, admission type + preferred SY)
    @route('/admission/reset', type='http', auth="public", website=True)
    def admission_reset(self, redirect=None, **kwargs):
        # Clear specific session data
        if 'applicant_type' in request.session:
            del request.session['applicant_type']
        if 'admission_type' in request.session:
            del request.session['admission_type']
        if 'select_sy_year' in request.session:
            del request.session['select_sy_year']

        # Redirect back to the applicant type selection page
        return request.redirect('/admission/select_applicant_type')