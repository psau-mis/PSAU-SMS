# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import pytz

from odoo import http
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.http import request
from odoo.modules.module import get_module_resource
from odoo.tools import ustr
from odoo.tools.translate import _


class ManifestTrack(http.Controller):

    @http.route(['/portal/manifest.webmanifest', '/parent/manifest.webmanifest'], type='http', auth='public', methods=['GET'], website=True, sitemap=False)
    def pwa_webmanifest(self):
        """ Returns a WebManifest describing the metadata associated with a web application.
        Using this metadata, user agents can provide developers with means to create user 
        experiences that are more comparable to that of a native application.
        """
        website = request.website
        manifest = {
            'name': website.company_id.name,
            'short_name': website.company_id.name,
            'description': _('%s Portal') % website.company_id.name,
            'scope': url_for('/'),
            'start_url': url_for('/'),
            'display': 'standalone',
            'background_color': '#ffffff',
            'theme_color': '#875A7B',
        }
        icon_sizes = ['192x192', '512x512']
        manifest['icons'] = [{
            'src': website.image_url(website.company_id, 'logo', size=size),
            'sizes': size,
            'type': 'image/png',
        } for size in icon_sizes]
        body = json.dumps(manifest, default=ustr)
        response = request.make_response(body, [
            ('Content-Type', 'application/manifest+json'),
        ])
        return response

    @http.route(['/portal/service-worker.js', '/parent/service-worker.js'], type='http', auth='public', methods=['GET'], website=True, sitemap=False)
    def service_worker(self):
        """ Returns a ServiceWorker javascript file scoped for website_event
        """
        sw_file = get_module_resource('esmis_website_portal', 'static/js/pwa_servicewoker.js')
        with open(sw_file, 'r') as fp:
            body = fp.read()
        js_cdn_url = 'undefined'
        if request.website.cdn_activated:
            cdn_url = request.website.cdn_url.replace('"','%22').replace('\x5c','%5C')
            js_cdn_url = '"%s"' % cdn_url
        body = body.replace('__ODOO_CDN_URL__', js_cdn_url)
        response = request.make_response(body, [
            ('Content-Type', 'text/javascript'),
            ('Service-Worker-Allowed', url_for('/portal', '/parent')),
        ])
        return response

    # @http.route('/event/offline', type='http', auth='public', methods=['GET'], website=True, sitemap=False)
    # def offline(self):
    #     """ Returns the offline page used by the 'website_event' PWA
    #     """
    #     return request.render('website_event_track.pwa_offline')
