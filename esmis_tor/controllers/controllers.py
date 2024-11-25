# -*- coding: utf-8 -*-
# from odoo import http


# class EsmisTor(http.Controller):
#     @http.route('/esmis_tor/esmis_tor', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/esmis_tor/esmis_tor/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('esmis_tor.listing', {
#             'root': '/esmis_tor/esmis_tor',
#             'objects': http.request.env['esmis_tor.esmis_tor'].search([]),
#         })

#     @http.route('/esmis_tor/esmis_tor/objects/<model("esmis_tor.esmis_tor"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('esmis_tor.object', {
#             'object': obj
#         })
