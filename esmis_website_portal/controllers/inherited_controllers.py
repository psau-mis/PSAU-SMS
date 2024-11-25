from odoo.http import request, route, Controller

# inherited controller from odoo default addons
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_slides.controllers.main import WebsiteSlides
from odoo.addons.website_profile.controllers.main import WebsiteProfile

# inherited controller from psau custom addons
from odoo.addons.esmis_website_admission.controllers.admission_main import WebsiteAdmissionRegister

class EsmisWebsiteCustomController(Website):

    @route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        user = request.env.user
        is_portal_user = user.has_group('base.group_portal')

        portal = '/my/home'

        if is_portal_user:
            return request.redirect(portal)
        else:
            return super(EsmisWebsiteCustomController, self).index(**kw)
   
    @route('/contactus', type='http', auth="public", website=True, sitemap=True)
    def contact_us(self, **kw):
        user = request.env.user
        is_student = user.is_student
        is_parent = user.is_parent

        if is_student:
            return request.redirect('/portal/dashboard')
        elif is_parent:
            return request.redirect('/parent/child')
        else:
            # return request.redirect('/contactus')
            return request.render("website.contactus")

class EsmisInheritCustomerPortal(CustomerPortal):

    @route(['/my', '/my/home'], type='http', auth="user", website=True)
    def home(self, **kw):
        user = request.env.user
        is_student = user.is_student
        is_parent = user.is_parent
        
        values = self._prepare_portal_layout_values()
        values.update({
            'name': user.first_name,
            'is_student': is_student,
            'is_parent' : is_parent,
        })

        if is_student:
            return request.redirect('/portal/dashboard')
        elif is_parent:
            return request.redirect('/parent/child')
        else:
            return super(EsmisInheritCustomerPortal, self).home(**kw)
    
    @route('/my/security', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def security(self, **post):
        user = request.env.user
        route = 'security'
        page_name = route
        # values['get_error'] = get_error
        # values['allow_api_keys'] = bool(request.env['ir.config_parameter'].sudo().get_param('portal.allow_api_keys'))
        # values['open_deactivate_modal'] = False

        # if request.httprequest.method == 'POST':
        #     values.update(self._update_password(
        #         post['old'].strip(),
        #         post['new1'].strip(),
        #         post['new2'].strip()
        #     ))
        
        values = self._prepare_portal_layout_values()
        values.update({
            'route': route,
            'user': user,
            'page_name': page_name,
            'is_student': user.is_student,
            'is_parent' : user.is_parent,
            'route': route,
            'page_name': page_name,
        })
        
        return super(EsmisInheritCustomerPortal, self).security(**post)
class EsmisInheritAdmissionController(WebsiteAdmissionRegister):

    @route('/my/admission', type='http', auth="public", website=True, methods=['GET', 'POST'])
    def admission_registration(self, **kw):
        user = request.env.user
        is_student = user.is_student
        is_parent = user.is_parent

        if is_student:
            return request.redirect('/portal/dashboard')
        elif is_parent:
            return request.redirect('/parent/child')
        else:
            return super(EsmisInheritAdmissionController, self).admission_registration(**kw)

        return super(EsmisInheritAdmissionController, self).admission_registration(**kw)
    
class CommonValuesMixin:
    @staticmethod
    def get_common_values():
        user = request.env.user
        return {
            'is_student': user.is_student,
            'is_parent': user.is_parent,
            'route': "elearning",
        }
    
class EsmisInheritWebSlideController(CommonValuesMixin, WebsiteSlides):

    def _slide_render_context_base(self):
        context = super(EsmisInheritWebSlideController, self)._slide_render_context_base()
        context.update(self.get_common_values())

        return context
    
class EsmisInheritWebsiteProfile(CommonValuesMixin, WebsiteProfile):

    def _prepare_user_values(self, **kwargs):
        values = super(EsmisInheritWebsiteProfile, self)._prepare_user_values(**kwargs)
        values.update(self.get_common_values())

        return values
    
    @route(['/profile/users', '/profile/users/page/<int:page>'], type='http', auth="public", website=True, sitemap=True)
    def view_all_users_page(self, page=1, **kwargs):
        response = super(EsmisInheritWebsiteProfile, self).view_all_users_page(page=page, **kwargs)
        response.qcontext.update(self.get_common_values())

        return response