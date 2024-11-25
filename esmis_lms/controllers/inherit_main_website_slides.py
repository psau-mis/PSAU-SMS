from odoo.http import request, route, Controller
from odoo.addons.website_slides.controllers.main import WebsiteSlides


class InheritSlidesController(WebsiteSlides):
    
    @route('/slides', type='http', auth="public", website=True, sitemap=True)
    def slides_channel_home(self, **post):
        res = super(InheritSlidesController, self).slides_channel_home(**post)

        return res
    
    @route('/slides/examination_result', type='http', auth="user", website=True, sitemap=True)
    def examination_result(self, **kwargs):

        exam = request.env['survey.user_input'].search([
            ('partner_id.id', '=', request.env.user.partner_id.id),
            ('state', "=", 'done'),
            ('survey_id.certification', '=', True),
        ])

        vals = {
            'examinations': exam,
        }
        return request.render('esmis_lms.examination_result', vals)