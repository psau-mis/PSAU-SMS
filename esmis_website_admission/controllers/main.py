from odoo.http import request, route, Controller
from odoo import _
from odoo.addons.esmis_website.controllers.admission_controller import NewWebsiteAdmissionController
from odoo.exceptions import ValidationError, UserError, AccessError
import base64


class WebsiteAdmissionControllerInherit(NewWebsiteAdmissionController):

	@route('/admission/undergraduate/new_student', type='http', auth="public", website=True)
	def undergraduate_new_student(self, **kwargs):
		res = super(WebsiteAdmissionControllerInherit, self).undergraduate_new_student(**kwargs)
		if not request.session.get('applicant_type') or not request.session.get('admission_type'):
			return res

		course = request.env['esmis.course'].sudo().search_read([],['name'])
		school_year_id = request.session.get('school_year', False)
		if school_year_id:
			school_year_id = request.env['esmis.school.year'].sudo().search([('id', '=', school_year_id)], limit=1)
		res.qcontext.update({'course':course, 'school_year': school_year_id})
		res.qcontext.update(self._get_country_related_render_values())
		return res

	@route('/admission/register_new', type='http', auth="public", website=True)
	def admission_register_new(self, **post):
		res = super(WebsiteAdmissionControllerInherit, self).admission_register_new(**post)
		admission_model = request.env['esmis.admission'].sudo()
		applicant_type = request.session.get('applicant_type', False)
		admission_type = request.session.get('admission_type', False)
		#prevent user from directly going in this route
		if not applicant_type or not admission_type:
			# If either applicant_type or admission_type is not set, redirect to select_applicant_type
			return res

		res.qcontext.update(self._get_admission_related_render_values())
		res.qcontext.update(self._get_country_related_render_values())
		return res

	@route('/admission/select_admission_type', type='http', auth="public", website=True, methods=['GET'])
	def select_admission_type(self, **post):
		res = super(WebsiteAdmissionControllerInherit, self).select_admission_type(**post)
		admission_model = request.env['esmis.admission'].sudo()
		school_year_ids = request.env['esmis.school.year'].sudo().search([])
		applicant_type = request.params.get('applicant_type', False)
		applicant_type_str = dict(admission_model._fields['admission_type_1'].selection).get(applicant_type)
		res.qcontext.update({'school_year': school_year_ids, 'applicant_type': applicant_type_str})
		return res

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

	def _get_admission_related_render_values(self):
		admission_model = request.env['esmis.admission'].sudo()
		applicant_type = request.session.get('applicant_type', False)
		admission_type = request.session.get('admission_type', False)
		school_year = request.env['esmis.school.year'].search([('id', '=', request.session.get('select_sy_year', False))], limit=1)
		course = request.env['esmis.course'].sudo().search_read([],['name'])
		admission_num = 'admission_type_2'
		if applicant_type == 'grad':
			admission_num = 'admission_type_3'
		return {
			'course': course, 'select_sy_year': school_year, 'admission_type_1': applicant_type,
			'admission_type_2': admission_type if applicant_type == 'undergrad' else False,
			'admission_type_3': admission_type if applicant_type == 'grad' else False,
			'applicant_type': dict(admission_model._fields['admission_type_1'].selection).get(applicant_type),
			'admission_type': dict(admission_model._fields[admission_num].selection).get(admission_type),
		}

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
		return [file_name, file]

	def string_datatype_check(self, value):
		if type(value) is str:
			if value == "":
				return False
			return value
		
		return value

	@route('/admission/register/action', type='http', auth="public", methods=['POST'], website=True)
	def admission_register_action(self, **kw):
		student_number = kw.get('input_student_number', False)
		admission_type_1 = kw.get('admission_type_1', False)
		if student_number:
			student_no_str = 'student_no_undg' if admission_type_1 == 'undergrad' else 'student_no_grad'
			student_id = request.env['res.partner'].sudo().search([(student_no_str, '=', student_number)], limit=1)
			admission_values = self._get_admission_related_render_values()
			admission_values.update(self._get_country_related_render_values())
			admission_values.update({'student_id': student_id, 'student_searched': True})
			return request.render("esmis_website.admission_registration_new", admission_values)

		upload_psa = self.prepare_file_attachment(kw.get('upload_psa', False))
		upload_hs_card = self.prepare_file_attachment(kw.get('upload_hs_card', False))
		upload_good_moral = self.prepare_file_attachment(kw.get('upload_good_moral', False))
		street = ""
		input_house_addr = kw.get('input_house_addr', False)
		input_street = kw.get('input_street', False)
		if input_house_addr:
			street = input_house_addr
			if input_street:
				street = street + " " + input_street
		barangay = kw.get('select_barangay', False)
		# if barangay:
		# 	barangay_id = request.env['res.barangay'].search([('id', '=', barangay)], limit=1)
		# 	if barangay_id:
		# 		barangay = barangay_id.name
		admission_type_2 = kw.get('admission_type_2', False)
		create_value = {
			'name': '/',
			'admission_type_1': admission_type_1,
			'admission_type_2': admission_type_2,
			'admission_type_3': kw.get('admission_type_3', False),
			'admission_type': admission_type_2 if admission_type_2 else kw.get('admission_type_3', False),
			'last_name': kw.get('input_Lname'),
			'first_name': kw.get('input_Fname'),
			'middle_name': kw.get('input_Mname', False),
			'suffix': kw.get('select_suffix', False),
			'course1_id': kw.get('select_first_choice', False),
			'course2_id': kw.get('select_second_choice', False),
			'course3_id': kw.get('select_third_choice', False),
			'email_address': kw.get('input_email'),
			'mobile': kw.get('input_mob_number', False),
			'phone': kw.get('input_landline', False),
			'street': input_house_addr,
			# 'street': kw.get('input_street'),#combine
			'state_id': kw.get('select_province', False),
			'city_id': kw.get('select_state', False),
			'street2': input_street,
			'barangay_id': barangay,
			'gender': kw.get('select_gender', False),
			'birthdate': self.string_datatype_check(kw.get('input_birthdate', False)),
			'civil_status': kw.get('select_civil_status', False),
			'place_of_birth': kw.get('input_birthplace', False),
			'citizenship': kw.get('input_citizenship', False),
			'religion': kw.get('input_religion', False),
			'father_name': kw.get('input_father_fname', False),
			'father_birthdate': self.string_datatype_check(kw.get('input_father_birthdate', False)),
			'father_educ_attain': kw.get('input_father_educ', False),
			'father_occupation': kw.get('input_father_job', False),
			'father_company': kw.get('input_father_company', False),
			'father_monthly_income': kw.get('input_father_income', False),
			'father_contact': kw.get('input_father_contact', False),
			'mother_name': kw.get('input_mother_fname', False),
			'mother_birthdate': self.string_datatype_check(kw.get('input_mother_birthdate', False)),
			'mother_educ_attain': kw.get('input_mother_educ', False),
			'mother_occupation': kw.get('input_mother_job', False),
			'mother_company': kw.get('input_mother_company', False),
			'mother_monthly_income': kw.get('input_mother_income', False),
			'mother_contact': kw.get('input_mother_contact', False),
			'guardian_name': kw.get('input_guardian_fname', False),
			'guardian_birthdate': self.string_datatype_check(kw.get('input_guardian_birthdate', False)),
			'guardian_educ_attain': kw.get('input_guardian_educ', False),
			'guardian_occupation': kw.get('input_guardian_job', False),
			'guardian_company': kw.get('input_guardian_company', False),
			'guardian_monthly_income': kw.get('input_guardian_income', False),
			'guardian_contact': kw.get('input_guardian_contact', False),
			'elementary_school_name': kw.get('input_elem_name', False),
			'elementary_school_start': kw.get('input_elem_start', False),
			'elementary_school_end': kw.get('input_elem_end', False),
			'elementary_school_address': kw.get('input_elem_address', False),
			'elementary_honors': kw.get('input_elem_honors', False),
			'senior_high_school_name': kw.get('input_shs_name', False),
			'senior_high_school_start': kw.get('input_shs_start', False),
			'senior_high_school_end': kw.get('input_shs_end', False),
			# '': 'input_shs_type',
			'senior_high_ave_grade': kw.get('input_shs_grade', False),
			'senior_high_school_address': kw.get('input_shs_address', False),
			'senior_high_honors': kw.get('input_shs_honors', False),
			'last_school_attended_name': kw.get('input_last_school_name', False),
			'last_school_attended_start': kw.get('input_last_school_start', False),
			'last_school_attended_end': kw.get('input_last_school_end', False),
			# '': 'input_last_school_type',
			# '': 'input_last_school_grade',
			'last_school_attended_address': kw.get('input_last_school_address', False),
			'birth_cert': upload_psa[1],
			'birth_cert_file': upload_psa[0],
			'shs_report_card': upload_hs_card[1],
			'shs_report_card_file': upload_hs_card[0],
			'gmc_cert': upload_good_moral[1],
			'gmc_cert_file': upload_good_moral[0],
			'school_year_id': kw.get('school_year_id', False),
		}
		admission = request.env['esmis.admission'].sudo().create(create_value)
		return request.redirect('/admission/landing', 303)

	@route('/admission/landing', type="http", auth="public", website=True, methods=["GET"])
	def admission_landing_redirect(self, **kw):

		return request.render("esmis_website_admission.admission_landing", {
			'message': "Admission Successfully saved.."
			})


	@route('/admission/register/update/document/<string:admission_uuid>', type="http", auth="public", website=True)
	def admission_register_update_document(self, admission_uuid, **kw):
		admission = request.env['esmis.admission'].sudo().search([('admission_uuid', '=', admission_uuid)], limit=1)
		if not admission:
			raise ValidationError("Admission not found...")
		return request.render("esmis_website_admission.admission_update_document", {
			'admission': admission
			})

	@route('/admission/admitted/accept/<model("esmis.admission"):admission_id>', type="http", auth="public", website=True)
	def admission_admitted_accept(self, admission_id, **kw):
		if admission_id.state not in ['for_admission', 'not_qualified']:
			raise AccessError(_('Action not allowed.'))
		return "Accept"

	@route('/admission/admitted/decline/<model("esmis.admission"):admission_id>', type="http", auth="public", website=True)
	def admission_admitted_decline(self, admission_id, **kw):
		if admission_id.state not in ['for_admission', 'not_qualified']:
			raise AccessError(_('Action not allowed.'))
		return "Declined"

	def prepare_attachment(self, attachment, field, admission):
		attachment_id = request.env['ir.attachment'].sudo()
		file_name = attachment.filename
		file = attachment.read()
		admission.update({
			field+"_file":file_name,
			field: file
		})
		saved_attach = attachment_id.create({
			'name': file_name,
			'res_field': field,
			'description': file_name,
			'store_fname': file_name,
			'type': 'binary',   
			'res_model': 'esmis.admission',
			'res_id': admission.id,
			'datas': base64.b64encode(file),
		})


	@route('/admission/register/update/document/submit', type='http', auth="public", website=True)
	def admission_register_update_document_save(self, admission_uuid, **kw):
		admission = request.env['esmis.admission'].sudo().search([('admission_uuid', '=', admission_uuid)], limit=1)
		admission.update({
			'admission_uuid': False,
		})
		for file in kw:
			self.prepare_attachment(kw[file], file, admission)
		return "Success " + str(admission.name)
