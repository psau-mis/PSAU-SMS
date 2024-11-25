import base64
import json

from odoo.http import request, route, Controller
from odoo.addons.esmis_website_portal.controllers.student_portal import EsmisStudentPortalController

class InheritStudentWebPortal(EsmisStudentPortalController):
    @route(['/portal/<string:route>'], type='http', auth="user", website=True, methods=['POST', 'GET'])
    def student_portal(self, route="dashboard", **kw):
        res = super(InheritStudentWebPortal, self).student_portal(route, **kw)

        student = request.env['res.partner'].sudo().browse(request.env.user.partner_id.id)
        if request.httprequest.method == 'POST':

            med_cert = kw.get('medical_cert_upload')
            health_clearance = kw.get('health_clearance_upload')

            med_cert = self.prepare_file_attachment(med_cert)
            health_clearance = self.prepare_file_attachment(health_clearance)

            student.write({
                'medical_cert_upload':med_cert[1],
                'medical_cert_upload_name':med_cert[0],
                'health_clearance_upload':health_clearance[1],
                'health_clearance_upload_name':health_clearance[0],
                # 'is_medical_sent': True,
            })
        
        files = []
        for file in student:
            medical_cert_download_url = '/web/content/%s/%s/file/%s' % (file._name, file.id, file.medical_cert_upload_name) + '?download=true'
            health_clearance_download_url = '/web/content/%s/%s/file/%s' % (file._name, file.id, file.health_clearance_upload) + '?download=true'
            medical_cert_image = '/web/content/%s/%s/file/%s' % (file._name, file.id, file.medical_cert_upload_name)
            health_clearance_image = '/web/content/%s/%s/file/%s' % (file._name, file.id, file.medical_cert_upload_name)
            files.append({
                'medical_cert_download_url': medical_cert_download_url,
                'health_clearance_download_url': health_clearance_download_url,
                'medical_cert_image': medical_cert_image,
                'health_clearance_image': health_clearance_image,
                'medical_cert_file_binary': file.medical_cert_upload,
                'health_clearance_file_binary': file.health_clearance_upload,
                'medical_cert_file_name': file.medical_cert_upload_name,
                'health_clearance_file_name': file.health_clearance_upload_name,
            })

        if student.is_medical_sent:
            res.qcontext.update({
                'is_medical_sent': True,
                'med_cert': student.medical_cert_upload,
                'health_clearance': student.health_clearance_upload,
                'files': files,
            })

        return request.render("esmis_website_portal.portal_main_layout", res.qcontext)
    
    def prepare_file_attachment(self, attachment):
        file_name = attachment.filename
        file = attachment.read()
        return [file_name, base64.b64encode(file)]