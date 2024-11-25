from odoo.http import request, route, Controller, content_disposition
from odoo import _
from odoo.exceptions import ValidationError, UserError, AccessError
from odoo.tools import html_escape
import base64
import json


class WebsiteAdmissionRegister(Controller):
	CREDENTIALS_FIELDS = [
		#'form_138',
		'tor',
		'tor_bachelor',
		'tor_master',
		'tor_current_master',
		'tor_current_doctor',
		'birth_cert',
		'employ_cert',
		'honorable_dismissal',
		'shs_report_card',
		'gmc_cert',
		'stud_personal_statement',
		'passport_bio',
		'birth_cert_foreign',
		'english_cert',
		'police_clearance',
	]

	def _get_country_related_render_values(self):
		'''
		This method provides fields related to the country to render the website admission Form
		'''

		country = request.env.company.country_id
		cities = country.get_esmis_cities()
		barangays = request.env['res.barangay'].search([('city_id', 'in', cities.ids)])
		res = {
			'country': country,
			'country_states': country.get_esmis_states(),
			'countries': country.get_esmis_countries(),
			'country_cities': cities,
			'country_barangays': barangays,
		}
		return res

	def prepare_file_attachment(self, attachment):
		file_name = attachment.filename
		file = attachment.read()
		return [file_name, base64.b64encode(file)]

	@route(['/esmis/student_info'], type='json', auth="public", methods=['POST'], website=True)
	def student_info(self, student_id, **kw):
		student = request.env['res.partner'].sudo().search_read([('id', '=', student_id)], [
			'street','street2','zip','city_id','barangay_id','state_id','email',
			'mobile_number','phone_number','gender','birthdate','civil_status',
			'birthplace','nationality','religion','father_full_name',
			'father_birthdate','father_educ_attain','father_occupation',
			'father_company','father_monthly_income','father_contact_no',
			'mother_full_name','mother_birthdate','mother_educ_attain',
			'mother_occupation','mother_company','mother_monthly_income',
			'mother_contact_no','guardian_full_name','guardian_birthdate',
			'guardian_educ_attain','guardian_occupation','guardian_company',
			'guardian_monthly_income','guardian_contact_no',
			])
		return student

	@route(['/esmis/check/email'], type="json", auth="public", methods=["POST"])
	def email_unique_check(self, email_address, **kw):
		user_with_email = request.env['res.users'].sudo().search_read([('login', '=', email_address)])
		if len(user_with_email):
			return 'exists'
		return False

	@route(['/esmis/states_info/<model("res.country.state"):state_id>'], type='json', auth="public", methods=['POST'], website=True)
	def states_info(self, state_id, **kw):
		return dict(
			cities=[(ct.id, ct.name) for ct in state_id.get_esmis_cities_on_states()],
		)

	@route(['/esmis/cities_info/<model("res.city"):city_id>'], type='json', auth="public", methods=['POST'], website=True)
	def cities_info(self, city_id, **kw):
		return dict(
			barangay=[(ct.id, ct.name) for ct in city_id.get_esmis_barangay_on_city()],
		)

	@route('/admission_check_exist', type="json", auth="user", methods=['POST', 'GET'], website=False)
	def admission_check_exist(self, **kw):
		last_name = kw.get('last_name', False)
		first_name = kw.get('first_name', False)
		middle_name = kw.get('middle_name', False)
		suffix = kw.get('suffix', False)
		birthdate = kw.get('birthdate', False)
		admission_type_1 = kw.get('admission_type_1', False)
		# raise ValidationError(birthdate)
		return request.env['esmis.admission'].check_exist(last_name=last_name, first_name=first_name, middle_name=middle_name, suffix=suffix, birthdate=birthdate, admission_type_1=admission_type_1)

	def _admission_submitted_create(self, values):
		admission_model = request.env['esmis.admission'].sudo()
		require_first_choice = request.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_first_choice')
		require_second_choice = request.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_second_choice')
		require_third_choice = request.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_third_choice')
		create_values = {
			'name': '/', 'applicant_signature': request.session.get('applicant_signature', False),
			'require_first_choice': require_first_choice, 'require_second_choice': require_second_choice, 'require_third_choice': require_third_choice
		}
		for key in admission_model._fields:
			val = values.get(key, False)
			if val:
				if key in self.CREDENTIALS_FIELDS:
					attachments = self.prepare_file_attachment(val)
					create_values[key] = attachments[1]
					create_values[key+'_file'] = attachments[0]
				else:
					create_values[key] = val
					if key == 'student_image':
						encoded_string = base64.b64encode(val.read())
						create_values[key] = encoded_string
					if key == 'applicant_signature':
						encoded_string = base64.b64encode(val.read())
						create_values[key] = encoded_string

					if key in ['mobile', 'father_contact', 'mother_contact', 'guardian_contact', 'spouse_contact']:
						create_values[key] = '+63 %s' %val

		if values['admission_type_1'] == 'undergrad':
			create_values['admission_type_2'] = values.get('select_admission', False)
			create_values['whole_level'] = 'Undergraduate'
		else:
			create_values['admission_type_3'] = values.get('select_admission', False)
			if values.get('select_admission', False) in ['graduate', 'transferee2']:
				create_values['whole_level'] = 'Masteral'
			elif values.get('select_admission', False) in ['graduate2', 'transferee3']:
				create_values['whole_level'] = 'Doctorate'

		student_id = values.get('student_id', False)
		if student_id:
			student = request.env['res.partner'].sudo().search([('id', '=', int(student_id))], limit=1)
			for st in student:
				create_values.update({
					'first_name': st.first_name,
					'last_name': st.last_name,
					'middle_name': st.middle_name,
					'suffix': st.suffix_name,
					'email_address': st.email,
					})

		company_counter = values.get('company_counter', False)
		if company_counter:
			company_counter = int(company_counter) + 1
			work_experience = []
			for ctr in range(company_counter):
				if ctr == 0:
					company_name = values.get('company_name', False)
					company_role = values.get('company_role', False)
					company_address = values.get('company_address', False)
					company_start = values.get('company_start', False)
					company_end = values.get('company_end', False)
					if company_name:
						work_experience.append((0,0,{
							'name': company_name,
							'role': company_role,
							'address': company_address,
							'start': company_start,
							'end': company_end,
							}))
				else:
					company_name = values.get('company_name_'+str(ctr), False)
					company_role = values.get('company_role_'+str(ctr), False)
					company_address = values.get('company_address_'+str(ctr), False)
					company_start = values.get('company_start_'+str(ctr), False)
					company_end = values.get('company_end_'+str(ctr), False)
					if company_name:
						work_experience.append((0,0,{
							'name': company_name,
							'role': company_role,
							'address': company_address,
							'start': company_start,
							'end': company_end,
							}))
			if len(work_experience):
				create_values.update({
					'work_experience_ids':work_experience,
					})
		created_admission = admission_model.create(create_values)

		request.session['admission_id'] = created_admission.id
		return request.redirect('/admission_landing', 303)

	@route('/admission/admitted/accept/<model("esmis.admission"):admission_id>', type="http", auth="public", website=True, methods=['GET', 'POST'])
	def admission_admitted_accept(self, admission_id, **kw):
		admission_id = admission_id.sudo()
		if admission_id.state not in ['for_admission', 'not_qualified']:
			raise AccessError(_('Action not allowed.'))
		message = "Thank you for responding, your application is now Updated."
		if admission_id.admitted_applicant_response == False:
			admission_id.write({'admitted_applicant_response': 'accepted'})
		else:
			message = "Sorry, you cannot change your response."
		return request.render("esmis_website_admission.admission_landing", {
			'message': message,
			'admission_id': False,
			})

	@route('/admission/admitted/decline/<model("esmis.admission"):admission_id>', type="http", auth="public", website=True, methods=['GET', 'POST'])
	def admission_admitted_decline(self, admission_id, **kw):
		admission_id = admission_id.sudo()
		if admission_id.state not in ['for_admission', 'not_qualified']:
			raise AccessError(_('Action not allowed.'))
		message = "Thank you for responding, your application is now Updated."
		if admission_id.admitted_applicant_response == False:
			admission_id.write({'admitted_applicant_response': 'declined'})
		else:
			message = "Sorry, you cannot change your response."
		return request.render("esmis_website_admission.admission_landing", {
			'message': message,
			'admission_id': False,
			})

	@route('/admission_landing', type="http", auth="public", website=True, methods=["GET"])
	def admission_landing_redirect(self, **kw):
		admission_id = request.session.get('admission_id', False)
		if admission_id:
			request.session['admission_id'] = False
		return request.render("esmis_website_admission.admission_landing", {
			'message': "Admission Successfully saved..",
			'admission_id': ('/report/pdf/esmis_admission.report_admission_student_application_form/%s' %admission_id) if admission_id else False,
			})

	def _admission_submitted_student_id(self, student_number, admission_type_1, school_year_id, select_admission):
		student_no_str = 'student_no_undg' if admission_type_1 == 'undergrad' else 'student_no_grad'
		student_id = request.env['res.partner'].sudo().search([(student_no_str, '=', student_number)], limit=1)
		return student_id

	def _get_admission_rendering_values(self, admission_type_1, select_admission, select_year_post):
		admission_model = request.env['esmis.admission'].sudo()
		school_year_ids = request.env['esmis.school.year'].sudo().search([('state', '=', 'Active')])
		level = ('level', '=', "Undergraduate")
		if admission_type_1 == 'grad':
			if select_admission in ['graduate', 'transferee2']:
				level = ('level', '=', "Masteral")
			elif select_admission in ['graduate2', 'transferee3']:
				level = ('level', '=', "Doctorate")
			else:
				level = ('level', '!=', "Undergraduate")
		course = request.env['esmis.course'].sudo().search([level])
		admission_num = 'admission_type_2'
		if admission_type_1 == 'grad':
			admission_num = 'admission_type_3'
		admission_values = {
			'school_years': school_year_ids,
			'admission_type_1': admission_type_1,
			'admission_type_1_str': False if not admission_type_1 else dict(admission_model._fields['admission_type_1'].selection).get(admission_type_1),
			'select_admission_str': dict(admission_model._fields[admission_num].selection).get(select_admission),
			'select_admission': select_admission,
			'course_id':course,
		}

		if select_year_post:
			select_year = request.env['esmis.school.year'].sudo().search([('id', '=', select_year_post)])
			admission_values.update({'select_year': select_year})
		admission_values.update(self._get_country_related_render_values())
		return admission_values

	@route('/my/admission', type='http', auth="public", website=True, methods=['GET', 'POST'])
	def admission_registration(self, **kw):
		if bool(request.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_admission')):
			raise AccessError("Admission is currently not available...")

		require_first_choice = request.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_first_choice')
		require_second_choice = request.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_second_choice')
		require_third_choice = request.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_third_choice')

		admission_type = kw.get('admission_type', False)
		input_student_number = kw.get('input_student_number', False)
		admission_type_1 = kw.get('admission_type_1', False)
		select_admission = kw.get('select_admission', False)
		select_year_post = kw.get('select_sy_year', False)
		admission_values = {
		'enabled': ['tor', 'tor_bachelor', 'tor_master', 'tor_current_master', 'tor_current_doctor',
			'birth_cert', 'employ_cert', 'honorable_dismissal', 'shs_report_card', 'gmc_cert', 'stud_personal_statement',
			'passport_bio', 'birth_cert_foreign', 'english_cert', 'police_clearance',
			],
		'require_first_choice': require_first_choice,
		'require_second_choice': require_second_choice,
		'require_third_choice': require_third_choice,
		}
		admission_required_id = False
		try:
			admission_required_id = request.env.ref('esmis_admission.default_requiring_form').sudo()
		except Exception as e:
			pass
		if admission_type:
			return self._admission_submitted_create(kw)
		if input_student_number:
			admission_values.update({'student_id': self._admission_submitted_student_id(input_student_number, admission_type_1, select_year_post, select_admission)})
		if admission_required_id and select_admission:
			admission_values.update({'required_attachment': admission_required_id.get_required(select_admission)})
		admission_values.update(self._get_admission_rendering_values(admission_type_1, select_admission, select_year_post))
		response = request.render("esmis_website_admission.applicant_type_selection", admission_values)
		response.headers['Cache-Control'] = 'no-store,no-cache, must-revalidate, post-check=0, pre-check=0'
		return response

	@route('/admission/register/update/document/<uuid:admission_uuid>', type="http", auth="public", website=True)
	def admission_register_update_document(self, admission_uuid, **kw):
		admission = request.env['esmis.admission'].sudo().search([('admission_uuid', '=', admission_uuid)], limit=1)
		if not admission:
			admission_line = request.env['esmis.admission.redirection.line'].sudo().search([('name', '=', admission_uuid)])
			for al in admission_line:
				if al.admission_id.admission_uuid:
					raise ValidationError(_("A new email has been sent to your address. Please check your inbox and spam folder for the resend request."))
			raise ValidationError(_("Sorry, the link you're using has expired. "))
		admission_required_id = False
		try:
			admission_required_id = request.env.ref('esmis_admission.default_requiring_form').sudo()
		except Exception as e:
			pass
		enabled = []
		required_attachment = []
		for rec in admission:
			for key in self.CREDENTIALS_FIELDS:
				if rec['resend_%s' % key]:
					enabled.append(key)
			if admission_required_id:
				required_attachment = admission_required_id.get_required(rec.admission_type)
		
		response = request.render("esmis_website_admission.admission_update_document", {
			'admission': admission,
			'enabled': enabled,
			'required_attachment': required_attachment,
			})
		response.headers['Cache-Control'] = 'no-store,no-cache, must-revalidate, post-check=0, pre-check=0'
		return response

	@route('/admission/register/upload/medcert/<uuid:medcert_url_uuid>', type="http", auth="public", website=True)
	def admission_register_upload_medcert_document(self, medcert_url_uuid, **kw):
		admission = request.env['esmis.admission'].sudo().search([('medical_cert_url_uuid', '=', medcert_url_uuid)], limit=1)
		to_upload = kw.get('to_upload', False)
		if to_upload:
			med_cert = kw.get('medical_attachment')
			med_cert = self.prepare_file_attachment(med_cert)
			admission.write({
				'medical_attachment': med_cert[1],
				'medical_attachment_file': med_cert[0],
				'medical_cert_url_uuid': False,
				})
			response = request.render("esmis_website_admission.admission_landing", {
				'message': "Successfully Uploaded..."
			})
		else:
			response = request.render("esmis_website_admission.admission_upload_medcert_document", {
				'admission': admission,
				})
			response.headers['Cache-Control'] = 'no-store,no-cache, must-revalidate, post-check=0, pre-check=0'
		return response

	@route('/admission/register/update/document/submit', type='http', auth="public", website=True)
	def admission_register_update_document_save(self, admission_uuid, **kw):
		admission = request.env['esmis.admission'].sudo().search([('admission_uuid', '=', admission_uuid)], limit=1)
		to_update = {
			'admission_uuid': False,
			'state': 'resubmitted',
		}
		for rec in admission:
			to_update.update({'admission_redirection_ids': [(0, 0, {'name': rec.admission_uuid, 'admission_id': rec.id})]})
			
		for file in kw:
			attachment = self.prepare_file_attachment(kw[file])
			to_update[file] = attachment[1]
			to_update[file+"_file"] = attachment[0]

		for key in self.CREDENTIALS_FIELDS:
			to_update['resend_%s' % key] = False
		admission.write(to_update)
		return request.render("esmis_website_admission.admission_landing", {
			'message': "Successfully Reuploaded..."
		})

	@route('/admission_notice_data', type="json", auth="public")
	def admission_notice_data(self):
		if bool(request.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_admission')):
			return False

		active_sy = request.env['esmis.school.year'].sudo().search([('state', '=', 'Active')], limit=1)
		if active_sy:
			for sy in active_sy:
				return sy.name
		return False

	@route('/test_accept_signature', type="json", auth="public")
	def test_accept_signature(self, signature=None):
		if not signature:
			return {'error': _('Signature is missing.')}

		request.session['applicant_signature'] = signature
		return {'force_refresh': False, 'is_admission': True}


	@route(['/admission/test/portal', '/admission/test/portal/<string:menu>'], type='http', auth="user", website=True)
	def admission_test_portal(self, menu='home', **kw):
		return request.render("esmis_website_admission.test_student_portal", {'menu':menu, 'call': 'esmis_website_admission.test_announcement_portal'})
