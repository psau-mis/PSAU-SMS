# -*- coding:utf-8 -*-

from odoo import api, fields, models, tools, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.osv import expression
from odoo.exceptions import ValidationError, UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools.safe_eval import safe_eval
import pytz
import mimetypes
import base64

ATTACHMENT_NAMES = [
	'tor', 'tor_bachelor', 'tor_master', 'tor_current_master', 'tor_current_doctor', 'birth_cert', 'employ_cert', 'honorable_dismissal', 'shs_report_card', 'gmc_cert', 'stud_personal_statement', 'passport_bio', 'birth_cert_foreign', 'english_cert', 'police_clearance',
	]

class StudenAdmission(models.Model):
	_name = 'esmis.admission'
	_description = "Student Admission"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	@api.model
	def default_get(self, fields):
		res = super(StudenAdmission, self).default_get(fields)
		res['require_first_choice'] = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_first_choice')
		res['require_second_choice'] = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_second_choice')
		res['require_third_choice'] = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.require_third_choice')

		return res

	#fields declaration
	name = fields.Char(string="Name", default="/")
	admission_uuid = fields.Char(string="UUID")
	company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company.id)

	#
	first_name = fields.Char(string="First Name", required=True)
	last_name = fields.Char(string="Last Name", required=True)
	middle_name = fields.Char(string="Middle Name")
	suffix = fields.Char(string="Suffix")
	admission_number = fields.Char(string="Admission No.")

	state = fields.Selection([('new', 'New'), ('submitted', 'Submitted'), ('need_to_resubmit', 'Need to Resubmit'),
								('resubmitted', 'Resubmitted'), ('received', 'For Entrance Exam'), ('for_evaluation', 'For Evaluation'),
								('for_admission', 'For Admission'), ('admitted', 'Admitted'),('cancelled', 'Cancelled'), ('not_qualified', 'Not Qualified')],
								string="State", default='new', track_visibility='onchange')
	lrn = fields.Char(string="LRN", size=12)
	admission_type_1 = fields.Selection([('undergrad', 'Undergraduate'), ('grad', 'Graduate')], string='Level', required=True)
	admission_type_2 = fields.Selection([('freshmen', 'New Student'), ('transferee', 'Transferee'), ('continuing', 'Second Courser'),
		('foreign', 'Foreign Applicant')], string = "Admission Type(Undegraduate Level)")

	admission_type_3 = fields.Selection([('graduate', 'Graduate Level: Masteral (New Student)'), ('transferee2', 'Graduate Level: Masteral (Transferee)'),
		('graduate2', 'Graduate Level: Doctoral (New Student)'), ('transferee3', 'Graduate Level: Doctoral (Transferee)'), ], string="Admission Type(Graduate Level)")

	admission_type = fields.Selection([('freshmen', 'New Student'), ('transferee', 'Transferee'), ('continuing', 'Second Courser'),
		('foreign', 'Foreign Applicant'), ('graduate', 'Graduate Level: Masteral (New Student)'), ('transferee2', 'Graduate Level: Masteral (Transferee)'),
		('graduate2', 'Graduate Level: Doctoral (New Student)'), ('transferee3', 'Graduate Level: Doctoral (Transferee)'), ], string="Admission Type", required=True)
	level_flag = fields.Boolean('Level')
	whole_level = fields.Char()
	course_domain_logical_operator = fields.Char('Logical Operator')
	#personal info
	gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default="male", required=True)
	birthdate = fields.Date(string="Date of Birth", required=True)
	citizenship = fields.Char(string="Citizenship")
	religion = fields.Char(string="Religion")
	civil_status = fields.Selection([('single', 'Single'), ('married', 'Married'), ('separated', 'Separated'), ('divorced', 'Divorced'),
									('widowed', 'Widowed')], string="Civil Status")
	place_of_birth = fields.Char(string="Place of Birth")
	street = fields.Char()
	street2 = fields.Char()
	zip = fields.Char(change_default=True)
	city_id = fields.Many2one('res.city', string="City")
	state_id = fields.Many2one("res.country.state", string='State/Province', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
	country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=lambda self: self.env.company.country_id.id)
	origin_address = fields.Text(string="Origin Address")
	origin_country_id = fields.Many2one('res.country', string='Origin Country', ondelete='restrict', default=lambda self: self.env.company.country_id.id)
	email_address = fields.Char(string="Email Address", required=True)
	mobile = fields.Char(string="Mobile No.", required=True)
	phone = fields.Char(string="Phone No.")
	student_image = fields.Image(string="Student Image")

	age = fields.Char(compute='_calc_age', string="Age", size=50, readonly=True)
	age2 = fields.Char(compute='_calc_age', string="Age", size=50, readonly=True)

	#academic record
	#elem
	elementary_school_name = fields.Char(string='Elementary')
	elementary_school_address = fields.Char(string='Elementary School Address')
	elementary_school_start = fields.Char(string='Elementary School Year(From)')
	elementary_school_end = fields.Char(string='Elementary School Year(To)')
	elementary_honors = fields.Char(string='Elementary School Honors Received')
	#senior high
	senior_high_school_name = fields.Char(string="Senior Highschool")
	senior_high_school_address = fields.Char(string='Senior Highschool Address')
	senior_high_school_start = fields.Char(string='Senior Highschool Year(From)')
	senior_high_school_end = fields.Char(string='Senior Highschool(To)')
	senior_high_ave_grade = fields.Char(string='Avarage Grade')
	senior_high_type = fields.Selection([('Public', 'Public'), ('Private', 'Private')], string='Type')
	senior_high_graduation_date = fields.Date(string='Graduation Date')
	senior_high_honors = fields.Char(string='Honors Received')
	first_time_college = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="First time in College", default="No")
	#college
	college_school_name = fields.Char(string="College School")
	college_address = fields.Char(string='College School Address')
	college_year_start = fields.Char(string='College School Year(From)')
	college_year_end = fields.Char(string='College School Year(To)')
	college_degree = fields.Char(string="College School Degree Earned")
	#Masters
	master_school_name = fields.Char(string="Masteral School Name")
	master_address = fields.Char(string='Masteral School Address')
	master_year_start = fields.Char(string='Masteral School Year(From)')
	master_year_end = fields.Char(string='Masteral School(To)')
	master_degree = fields.Char(string="Masteral School Degree Earned")
	#last school
	last_school_attended_name = fields.Char(string='Last School Attended')
	last_school_attended_address = fields.Char(string='Last School Attended Address')
	last_school_attended_start = fields.Char(string='Last School Attended Year(From)')
	last_school_attended_end = fields.Char(string='Last School Attended Year(To)')
	last_school_attended_honors = fields.Char(string='Last School Attended Honors Received')
	last_school_attended_academic_level = fields.Selection([('undergrad', 'Undergraduate'), ('graduate', 'Graduate'),
				('techvoc', 'Vocational'), ('basiced', 'Basic Education'), ('n/a', 'Not Applicable')], string='Last School Attended Academic Level')

	scholar_sponsor = fields.Char(string="Scholarship Enjoyed/ Sponsor")
	gpa_rating = fields.Char(string="GPA Rating")

	#Family BG
	#Father
	father_name = fields.Char(string='Father Name')
	father_birthdate = fields.Date(string='Father Birthday')
	father_educ_attain = fields.Char(string='Father Highest Educational Attainment')
	father_occupation = fields.Char(string='Father Occupation/Employment')
	father_company = fields.Char(string='Father Company Name/Address')
	father_monthly_income = fields.Char(string='Father Monthly Income')
	father_contact = fields.Char(string='Father Contact No.')
	#Mother
	mother_name = fields.Char(string='Mother Name')
	mother_birthdate = fields.Date(string='Mother Birthday')
	mother_educ_attain = fields.Char(string='Mother Highest Educational Attainment')
	mother_occupation = fields.Char(string='Mother Occupation/Employment')
	mother_company = fields.Char(string='Mother Company Name/Address')
	mother_monthly_income = fields.Char(string='Mother Monthly Income')
	mother_contact = fields.Char(string='Mother Contact No.')
	#Guardian
	guardian_name = fields.Char(string='Guardian Name')
	guardian_birthdate = fields.Date(string='Guardian Birthday')
	guardian_educ_attain = fields.Char(string='Guardian Highest Educational Attainment')
	guardian_occupation = fields.Char(string='Guardian Occupation/Employment')
	guardian_company = fields.Char(string='Guardian Company Name/Address')
	guardian_monthly_income = fields.Char(string='Guardian Monthly Income')
	guardian_contact = fields.Char(string='Guardian Contact No.')
	#Spouse
	spouse_name = fields.Char(string='Spouse Name')
	spouse_birthdate = fields.Date(string='Spouse Birthday')
	spouse_educ_attain = fields.Char(string='Spouse Highest Educational Attainment')
	spouse_occupation = fields.Char(string='Spouse Occupation/Employment')
	spouse_company = fields.Char(string='Spouse Company Name/Address')
	spouse_monthly_income = fields.Char(string='Spouse Monthly Income')
	spouse_contact = fields.Char(string='Spouse Contact No.')

	#Admission Qualification
	raw_score = fields.Integer(string="Raw Score")
	is_no_show = fields.Boolean(string="No Show")
	stanine = fields.Integer(string="Stanine", compute="_compute_entrance_test_score_calc")
	interpretation = fields.Char(string="Interpretation", compute="_compute_entrance_test_score_calc")
	psychometrician_id = fields.Many2one('hr.employee', "Psychometrician")
	psychological_remarks = fields.Text("Remarks")
	qualified_course_id = fields.Many2one('esmis.course', "Qualified Program")
	qualified_department_id = fields.Many2one(
		'esmis.department',
		"School/College",
		related="qualified_course_id.department_id",
		readonly=True
	)
	test_type_id = fields.Many2one('esmis.admission.test.type', string="Interpretation", domain="[('active', '=', True)]", track_visibility='onchange')

	evaluated_by_id = fields.Many2one("res.users", "Evaluated By", readonly=True)
	evaluated_datetime = fields.Datetime("Date Evaluated", readonly=True)

	not_qualified_by_id = fields.Many2one("res.users", "Not Qualified By", readonly=True)
	not_qualified_datetime = fields.Datetime("Date Not Qualified", readonly=True)

	#preferred program
	preferred_date_enrollment = fields.Char(string='Preferred Date of Enrollment')
	preferred_year = fields.Char(string='Preferred Year', related="school_year_id.year_to")
	preferred_semester = fields.Selection([('1st Semester', '1st Semester'),('2nd Semester', '2nd Semester'),('Mid-Term', 'Mid-Term')], related="school_year_id.sem", string='Preferred Year')

	grad_previously_enrolled = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Previously Enrolled in other College", default="no")
	grad_previously_enrolled_school_name = fields.Char(string="School Name")
	#online submission
	date_submitted = fields.Date(string="Date Submitted")
	application_datetime_completion = fields.Datetime(string="Date Application was Completed")

	#admitting Office action
	received_by_user_id = fields.Many2one('res.users', string='Received By')
	cancelled_by_user_id = fields.Many2one('res.users', string='Cancelled By')
	admitted_by_user_id = fields.Many2one('res.users', string='Admitted By')
	received_date = fields.Date(string='Received Date')
	cancelled_date = fields.Date(string='Cancelled Date')
	admitted_date = fields.Date(string='Admitted Date')
	exam_responsible_id = fields.Many2one('res.users', string='Exam Responsible')

	#guidance office action
	test_scheduled_by_user_id = fields.Many2one('res.users', string="Entrance Test Schechuled By")
	test_date = fields.Datetime("Test Date")
	test_venue = fields.Char(string='Test Venue')
	set_admission_by_user_id = fields.Many2one('res.users', string="Set for Admission By")
	date_set_for_admission = fields.Date(string="Date set for Admission")
	student_with_user = fields.Boolean(string="Student with User")

	student_id = fields.Many2one("res.partner", "Student Record")
	student_no_undg = fields.Char('Student Number (Undegraduate)')
	student_no_grad = fields.Char('Student Number (Graduate)')

	for_evaluation_by_id = fields.Many2one("res.users", "Set for Evaluation By", readonly=True)
	for_evaluation_datetime = fields.Datetime("Date Set for Evaluation", readonly=True)
	for_admission_by_id = fields.Many2one("res.users","Set for Admission By", readonly=True)
	for_admission_datetime = fields.Datetime("Date Set for Admission", readonly=True)
	#selected program
	school_year_id = fields.Many2one('esmis.school.year', string='School Year/Semester')
	course1_id = fields.Many2one('esmis.course', string="First Choice", domain="[('level', '=', whole_level)]")
	course2_id = fields.Many2one('esmis.course', string="Second Choice", domain="[('level', '=', whole_level), ('id', '!=', course1_id)]")
	course3_id = fields.Many2one('esmis.course', string="Third Choice", domain="[('level', '=', whole_level), '&', ('id', '!=', course1_id), ('id', '!=', course2_id)]")
	active_course_id = fields.Many2one('esmis.course', "Active Program For Evaluation")
	require_first_choice = fields.Boolean(string="Require 1st Choice", required=True)
	require_second_choice = fields.Boolean(string="Require 2nd Choice", required=True)
	require_third_choice = fields.Boolean(string="Require 3rd Choice")

	#documents
	form_138 = fields.Binary(string='Form 138')
	form_138_file = fields.Char(string='Form 138 File Name')
	tor = fields.Binary(string='TOR (Transcript of Records)')
	tor_file = fields.Char(string='TOR (Transcript of Records) File Name')
	tor_pdf = fields.Boolean(string='TOR (Transcript of Records) PDF', default=True)
	tor_required = fields.Boolean(string='TOR (Transcript of Records)', compute="_compute_required_attachment")
	tor_bachelor = fields.Binary(string="TOR Bachelors' Degree (Transcript of Records)")
	tor_bachelor_file = fields.Char(string="TOR Bachelors' Degree (Transcript of Records) File Name")
	tor_bachelor_required = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records)", compute="_compute_required_attachment")
	tor_bachelor_pdf = fields.Boolean(string="TOR Bachelors' Degree (Transcript of Records) PDF", default=True)
	tor_master = fields.Binary(string="TOR Masters' Degree (Transcript of Records)")
	tor_master_file = fields.Char(string="TOR Masters' Degree (Transcript of Records) File Name")
	tor_master_required = fields.Boolean(string="TOR Masters' Degree (Transcript of Records)", compute="_compute_required_attachment")
	tor_master_pdf = fields.Boolean(string="TOR Masters' Degree (Transcript of Records) PDF", default=True)
	tor_current_master = fields.Binary(string="TOR Current Masters' Program (Transcript of Records)")
	tor_current_master_file = fields.Char(string="TOR Current Masters' Program (Transcript of Records) File Name")
	tor_current_master_required = fields.Boolean(string="TOR Current Masters' Program (Transcript of Records)", compute="_compute_required_attachment")
	tor_current_master_pdf = fields.Boolean(string="TOR Current Masters' Program (Transcript of Records) PDF", default=True)
	tor_current_doctor = fields.Binary(string="TOR Current Doctors' Program (Transcript of Records)")
	tor_current_doctor_file = fields.Char(string="TOR Current Doctors' Program (Transcript of Records) File Name")
	tor_current_doctor_required = fields.Boolean(string="TOR Current Doctors' Program (Transcript of Records)", compute="_compute_required_attachment")
	tor_current_doctor_pdf = fields.Boolean(string="TOR Current Doctors' Program (Transcript of Records) PDF", default=True)
	birth_cert = fields.Binary(string='PSA-issued Birth Certificate')
	birth_cert_file = fields.Char(string='PSA-issued Birth Certificate File Name')
	birth_cert_required = fields.Boolean(string='PSA-issued Birth Certificate', compute="_compute_required_attachment")
	birth_cert_pdf = fields.Boolean(string='PSA-issued Birth Certificate PDF', default=True)
	employ_cert = fields.Binary(string='Certificate of Employment')
	employ_cert_file = fields.Char(string='Certificate of Employment File Name')
	employ_cert_required = fields.Boolean(string='Certificate of Employment', compute="_compute_required_attachment")
	employ_cert_pdf = fields.Boolean(string='Certificate of Employment PDF', default=True)
	honorable_dismissal = fields.Binary(string='Honorable Dismissal')
	honorable_dismissal_file = fields.Char(string='Honorable Dismissal File Name')
	honorable_dismissal_required = fields.Boolean(string='Honorable Dismissal', compute="_compute_required_attachment")
	honorable_dismissal_pdf = fields.Boolean(string='Honorable Dismissal PDF', default=True)
	shs_report_card = fields.Binary(string='Senior Highschool Report Card')
	shs_report_card_file = fields.Char(string='SHS Report Card File Name')
	shs_report_card_required = fields.Boolean(string='Senior Highschool Report Card', compute="_compute_required_attachment")
	shs_report_card_pdf = fields.Boolean(string='Senior Highschool Report Card PDF', default=True)
	gmc_cert = fields.Binary(string='Certificate of Good Moral Character')
	gmc_cert_file = fields.Char(string='Certificate of Good Moral character File Name')
	gmc_cert_pdf = fields.Boolean(string='Certificate of Good Moral Character PDF', default=True)
	gmc_cert_required = fields.Boolean(string='Certificate of Good Moral Character', compute="_compute_required_attachment")
	stud_personal_statement = fields.Binary(string='Student Personal History Statement')
	stud_personal_statement_file = fields.Char(string='Student Personal History Statement File Name')
	stud_personal_statement_required = fields.Boolean(string='Student Personal History Statement', compute="_compute_required_attachment")
	stud_personal_statement_pdf = fields.Boolean(string='Student Personal History Statement PDF', default=True)
	passport_bio = fields.Binary(string='Passport Bio Page')
	passport_bio_file = fields.Char(string='Passport Bio Page File Name')
	passport_bio_required = fields.Boolean(string='Passport Bio Page', compute="_compute_required_attachment")
	passport_bio_pdf = fields.Boolean(string='Passport Bio Page PDF', default=True)
	birth_cert_foreign = fields.Binary(string='Birth Certificate')
	birth_cert_foreign_file = fields.Char(string='Birth Certificate File Name')
	birth_cert_foreign_required = fields.Boolean(string='Birth Certificate', compute="_compute_required_attachment")
	birth_cert_foreign_pdf = fields.Boolean(string='Birth Certificate PDF', default=True)
	english_cert = fields.Binary(string='Certificate of English Proficiency')
	english_cert_file = fields.Char(string='Certificate of English proficiency File Name')
	english_cert_required = fields.Boolean(string='Certificate of English Proficiency', compute="_compute_required_attachment")
	english_cert_pdf = fields.Boolean(string='Certificate of English Proficiency PDF', default=True)
	police_clearance = fields.Binary(string='Police Clearance (Philippines NBI)')
	police_clearance_file = fields.Char(string='Police Clearance (Philippines NBI) File Name')
	police_clearance_required = fields.Boolean(string='Police Clearance (Philippines NBI)', compute="_compute_required_attachment")
	police_clearance_pdf = fields.Boolean(string='Police Clearance (Philippines NBI) PDF', default=True)

	medical_cleared = fields.Boolean(string="Medical Cleared")

	medical_attachment = fields.Binary(string='Medical Certificate')
	medical_attachment_file = fields.Char(string='Medical Certificate File Name')

	tor_image = fields.Boolean( compute="_compute_attachment_image")
	tor_bachelor_image = fields.Boolean(compute="_compute_attachment_image")
	tor_master_image = fields.Boolean(compute="_compute_attachment_image")
	tor_current_master_image = fields.Boolean(compute="_compute_attachment_image")
	tor_current_doctor_image = fields.Boolean(compute="_compute_attachment_image")
	birth_cert_image = fields.Boolean(compute="_compute_attachment_image")
	employ_cert_image = fields.Boolean(compute="_compute_attachment_image")
	honorable_dismissal_image = fields.Boolean(compute="_compute_attachment_image")
	shs_report_card_image = fields.Boolean(compute="_compute_attachment_image")
	gmc_cert_image = fields.Boolean(compute="_compute_attachment_image")
	stud_personal_statement_image = fields.Boolean(compute="_compute_attachment_image")
	passport_bio_image = fields.Boolean(compute="_compute_attachment_image")
	birth_cert_foreign_image = fields.Boolean(compute="_compute_attachment_image")
	english_cert_image = fields.Boolean(compute="_compute_attachment_image")
	police_clearance_image = fields.Boolean(compute="_compute_attachment_image")

	#not admitted
	evaluation1 = fields.Char(string="Evaluation")
	reason1 = fields.Text(string="Not Admitted Because of")
	evaluation2 = fields.Char(string="Evaluation")
	reason2 = fields.Text(string="Not Admitted Because of")
	evaluation3 = fields.Char(string="Evaluation")
	reason3 = fields.Text(string="Not Admitted Because of")

	#work experience
	input_company1_name = fields.Char(string="Company Name")
	input_company1_role = fields.Char(string="Role")
	input_company1_address = fields.Char(string="Company Address")
	input_company1_start = fields.Date(string="Date Started")
	input_company1_end = fields.Date(string="Date Ended")

	schedule_state = fields.Char(string="Test Schedule State", compute="_compute_on_sched")
	test_scheduled = fields.Boolean(string="Scheduled")

	work_experience_ids = fields.One2many('esmis.admission.work.experience', 'admission_id', string="Work Experience")
	applicant_signature = fields.Image(string="E-Signature")
	footer_text = fields.Char(string="Report Footer", help="This will be displayed on reports footer")

	def _compute_on_sched(self):
		for rec in self:
			schedule = self.env['esmis.admission.test.schedule'].search([('esmis_admission_ids', 'in', rec.id), ('state', '!=', 'cancelled')], limit=1)
			if schedule:
				for sc in schedule:
					rec.schedule_state = sc.state
			else:
				rec.schedule_state = 'draft'

	def get_student_name(self, student_no_grad, student_no_undg, last_name, first_name, middle_name, name_suffix):
		"""Combine name fields"""
		name = ''
		stud_no = ''
		if student_no_grad:
			stud_no = '[' + student_no_grad + '] '
		elif student_no_undg:
			stud_no = '[' + student_no_undg + '] '
		if last_name:
			name += last_name + ', '
		if first_name:
			name += first_name + ' '
		if middle_name:
			name += middle_name + ' '
		name_suffix = name_suffix or ''
		full_name = name.title() + name_suffix
		return stud_no + full_name, full_name

	def get_current_curriculum(self, course_id):
		"""curriculum id getter"""
		curr = self.env["esmis.curriculum"].search([('course_id', '=', course_id)], order="id desc", limit=1)
		if curr:
			return curr[0].id
		else:
			return None

	def compute_age_from_dates (self, date_of_birth):
		"""age formatter"""
		now=datetime.strptime(str(fields.Datetime.now())[:10],'%Y-%m-%d')
		if (date_of_birth):
			dob = date_of_birth
			delta = relativedelta(now, dob)
			years_months_days = str(delta.years) + "y " + str(delta.months) + "m " + str(delta.days)+"d"
			years = str(delta.years)
		else:
			years_months_days = "No Birthdate!"
			years = "0"
		return years_months_days, years

	def send_mail_with_template(self, template, context={}, bulk=False):
		cancelled_auto_send_email = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_sending_of_email')
		if not cancelled_auto_send_email or bulk:
			mail_template = self.env.ref(template)
			result_mails_su, result_messages = self.with_context(context).message_post_with_template(template_id=mail_template.id)
			return result_messages
		return False

	def _get_mimetype(self, file_name):
		#safe eval
		self_file_name = safe_eval(expr='self.' + file_name + '_file', locals_dict={'self': self,})
		if self_file_name:
			mimetype = mimetypes.guess_type(self_file_name)[0]
			if mimetype.split('/')[0] == 'image':
				return False
			else:
				return True

		return True

	def check_mimetype(self):
		for attachment_name in ATTACHMENT_NAMES:
			is_pdf = self._get_mimetype(attachment_name)
			# expr = 'self.' + attachment_name + '_pdf = ' + str(is_pdf) 
			expr = "self.write({'" + attachment_name + '_pdf' + "': " + str(is_pdf) + "})"
			safe_eval(expr=expr, locals_dict={'self': self,})

	@api.depends('admission_type')
	def _compute_required_attachment(self):
		for rec in self:
			admission_required_id = False
			# try:
			# 	admission_required_id = self.env.ref('esmis_admission.default_requiring_form').sudo()
			# except Exception as e:
			# 	pass
			rec.tor_current_master_required = False
			rec.tor_current_doctor_required = False
			rec.birth_cert_required = False
			rec.employ_cert_required = False
			rec.honorable_dismissal_required = False
			rec.shs_report_card_required = False
			rec.gmc_cert_required = False
			rec.stud_personal_statement_required = False
			rec.passport_bio_required = False
			rec.birth_cert_foreign_required = False
			rec.english_cert_required = False
			rec.police_clearance_required = False

			rec.tor_required = False
			rec.tor_bachelor_required = False
			rec.tor_master_required = False
			if admission_required_id:
				
				if admission_required_id.tor_transferee and rec.admission_type == 'transferee':
					rec.tor_required = True
				if admission_required_id.tor_foreign and rec.admission_type == 'foreign':
					rec.tor_required = True
				if admission_required_id.tor_bachelor_graduate and rec.admission_type == 'graduate':
					rec.tor_bachelor_required = True
				if admission_required_id.tor_bachelor_continuing and rec.admission_type == 'continuing':
					rec.tor_bachelor_required = True
				if admission_required_id.tor_master and rec.admission_type == 'graduate2':
					rec.tor_master_required = True
				if admission_required_id.tor_current_master and rec.admission_type == 'transferee2':
					rec.tor_current_master_required = True
				if admission_required_id.tor_current_doctor and rec.admission_type == 'transferee3':
					rec.tor_current_doctor_required = True
				if admission_required_id.birth_cert_transferee and rec.admission_type == 'transferee':
					rec.birth_cert_required = True
				if admission_required_id.birth_cert_freshmen and rec.admission_type == 'freshmen':
					rec.birth_cert_required = True
				if admission_required_id.birth_cert_continuing and rec.admission_type == 'continuing':
					rec.birth_cert_required = True
				if admission_required_id.employ_cert_graduate and rec.admission_type == 'graduate':
					rec.employ_cert_required = True
				if admission_required_id.employ_cert_transferee2 and rec.admission_type == 'transferee2':
					rec.employ_cert_required = True
				if admission_required_id.employ_cert_graduate2 and rec.admission_type == 'graduate2':
					rec.employ_cert_required = True
				if admission_required_id.employ_cert_transferee3 and rec.admission_type == 'transferee3':
					rec.employ_cert_required = True
				if admission_required_id.honorable_dismissal_transferee and rec.admission_type == 'transferee':
					rec.honorable_dismissal_required = True
				if admission_required_id.honorable_dismissal_transferee2 and rec.admission_type == 'transferee2':
					rec.honorable_dismissal_required = True
				if admission_required_id.honorable_dismissal_transferee3 and rec.admission_type == 'transferee3':
					rec.honorable_dismissal_required = True
				if admission_required_id.shs_report_card and rec.admission_type == 'freshmen':
					rec.shs_report_card_required = True
				if admission_required_id.gmc_cert and rec.admission_type == 'freshmen':
					rec.gmc_cert_required = True
				if admission_required_id.stud_personal_statement and rec.admission_type == 'foreign':
					rec.stud_personal_statement_required = True
				if admission_required_id.passport_bio and rec.admission_type == 'foreign':
					rec.passport_bio_required = True
				if admission_required_id.birth_cert_foreign and rec.admission_type == 'foreign':
					rec.birth_cert_foreign_required = True
				if admission_required_id.english_cert and rec.admission_type == 'foreign':
					rec.english_cert_required = True
				if admission_required_id.police_clearance and rec.admission_type == 'foreign':
					rec.police_clearance_required = True

	@api.depends('birthdate')
	def _calc_age(self):
		for line in self:
			age = self.compute_age_from_dates(line.birthdate)
			line.age = age[0]
			line.age2 = age[1]

	@api.depends("raw_score", 'test_type_id')
	def _compute_entrance_test_score_calc(self):
		for rec in self:
			entrance_test_score_calc, entrance_test_score_interpret = rec.test_type_id.get_stanine_from_score(rec.raw_score)
			rec.stanine = entrance_test_score_calc
			rec.interpretation = entrance_test_score_interpret

	@api.model
	def get_footer_text(self):
		footer = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.admission_report_footer')
		if footer:
			return footer
		return ""

	@api.model
	def get_signatories(self):
		signatories_id = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.admission_signatory_id')
		if signatories_id:
			signatories_id = self.env['esmis.signatories'].search([('id', '=', int(signatories_id))])
		return signatories_id

	@api.model
	def admission_student_full_name(self):
		"""name formatter"""
		return (self.last_name + ", " + self.first_name +
				("" if self.middle_name == False else " " + self.middle_name) +
				("" if self.suffix == False else " " + self.suffix))

	@api.model
	def get_formatted_exam_date(self):
		if not self.test_date:
			return ""
		localtimezone = pytz.timezone('Asia/Manila')
		iso_dt = self.test_date.astimezone(localtimezone).isoformat(' ', timespec='minutes').replace('+08:00','')
		date_iso = datetime.strptime(iso_dt.split(' ')[0], DATE_FORMAT).strftime('%B %d, %Y')
		time_iso = datetime.strptime(iso_dt.split(' ')[1], '%H:%M').strftime('%I:%M %p')
		return str(date_iso + ' ' + time_iso)

	@api.model
	def create(self, vals):
		"""
			extends default create function
			set field name value
			set field admission_number value
			return dict
		"""
		if bool(self.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_admission')):
			raise ValidationError(_('Admission is currently disabled...'))
		if vals['name'] == '/' or vals['name'] == False:
			vals['name'] = (vals.get('last_name') + ", " + vals.get('first_name') +
							("" if not vals.get('middle_name') else " " + str(vals.get('middle_name'))) +
							("" if not vals.get('suffix') else " " + str(vals.get('suffix'))))
			vals['name'] = vals.get('name') + " Admission(" + datetime.today().strftime('%Y') + ")"
		admission_no = vals.get('admission_number', False)
		if not admission_no:
			admission_no_seq = self.env['ir.sequence'].sudo().next_by_code('esmis.admission') or '/'
			vals['admission_number'] = admission_no_seq
		vals['level_flag'] = True
		res = super(StudenAdmission, self.sudo()).create(vals)
		res.send_mail_with_template('esmis_admission.admission_on_save_mail')
		res.check_mimetype()
		return res

	def write(self, vals):
		for attachment_name in ATTACHMENT_NAMES:
			is_pdf = self._get_mimetype(attachment_name)
			vals[attachment_name+'_pdf'] = is_pdf
		vals['level_flag'] = True
		return super(StudenAdmission, self).write(vals)

	@api.model
	def confirmation_action(self, action):
		try:
			return eval(action)
		except Exception as e:
			raise e

	@api.model
	def action_esmis_my_department(self):
		return {
			"name": "By School/College",
			"view_mode": "tree,kanban,form",
			"res_model": "esmis.admission",
			"target": "current",
			"type": "ir.actions.act_window",
			"domain": [('qualified_department_id', 'in', self.env.user.department_ids.ids)],
			"help": 'Here you will see all qualified admission under your department',
			'target':'main',
		}

	@api.model
	def action_esmis_my_course(self):
		return {
			"name": "By Program",
			"view_mode": "tree,kanban,form",
			"res_model": "esmis.admission",
			"type": "ir.actions.act_window",
			"domain": [('active_course_id', 'in', self.env.user.course_ids.ids)],
			"help": 'Here you will see all admission under the program you manage',
			'target':'main',
		}

	@api.model
	def action_esmis_my_course_for_evaluation(self):
		return {
			"name": "For Evaluation",
			"view_mode": "tree,kanban,form",
			"res_model": "esmis.admission",
			"type": "ir.actions.act_window",
			"domain": ['&', ('active_course_id', 'in', self.env.user.course_ids.ids), ('state', '=', 'for_evaluation')],
			"help": 'Here you will see all for evaluation admission under the program you manage',
			'target':'main',
		}

	@api.model
	def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
		args = args or []
		domain = []
		if name:
			domain = ['|', ('admission_number', 'ilike', name), ('name', operator, name)]
			if operator in expression.NEGATIVE_TERM_OPERATORS:
				domain = ['&', '!'] + domain[1:]
		return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

	@api.model
	def _get_view(self, view_id=None, view_type='form', **options):
		arch, view = super()._get_view(view_id, view_type, **options)
		if view_type in ('tree', 'kanban') and bool(self.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_admission')):
			main_view = arch.xpath("//%s" %view_type)[0]
			main_view.set('create', "false")
		return arch, view

	@api.model
	def get_address(self):
		address = ""
		if self.street:
			if address != "":
				address = address + " " + self.street
			else:
				address = self.street
		if self.street2:
			if address != "":
				address = address + " " + self.street2
			else:
				address = self.street2
		if self.city_id:
			if address != "":
				address = address + " " + self.city_id.name
			else:
				address = self.city_id.name
		if self.zip:
			if address != "":
				address = address + " " + self.zip
			else:
				address = self.zip
		if self.state_id:
			if address != "":
				address = address + " " + self.state_id.name
			else:
				address = self.state_id.name
		if self.country_id:
			if address != "":
				address = address + " " + self.country_id.name
			else:
				address = self.country_id.name
		return address

	@api.model
	def get_latest_work(self, field):
		for rec in self.work_experience_ids:
			if rec.is_latest:
				if field == 'name':
					return rec.name
				if field == 'address':
					return rec.address
		return ""


	def notify_test_sched(self):
		""" test schedule email sender """
		return self.send_mail_with_template('esmis_admission.test_sched_notification')

	def send_application_confirmation_mail(self):
		""" application confirmation email sender """
		self.send_mail_with_template('esmis_admission.admission_on_save_mail')

	def receive_admission(self):
		""" for button 'For Entrance Exam' action """
		for rec in self:
			if rec.state in ('new','submitted', 'resubmitted'):
				admission_no = rec.admission_number
				if not admission_no:
					admission_no = self.env['ir.sequence'].next_by_code('esmis.admission') or '/'
				rec.update({
					'admission_number': admission_no,
					'received_by_user_id': self.env.user.id,
					'received_date': datetime.today(),
					'state': 'received',
				})
				# self.send_mail_with_template('esmis_admission.admission_confirmation_notice_email_template')
			else:
				raise ValidationError(_("Only new, submitted, or resubmitted admissions can be received."))

	def set_for_evaluation(self):
		for rec in self:
			if rec.state == 'received' and rec.raw_score > 0:
				rec.update({
					'for_evaluation_by_id': self.env.user.id,
					'for_evaluation_datetime': fields.Datetime.now(),
					'state': 'for_evaluation',
					'active_course_id': rec.course1_id.id,
				})
				# self.send_mail_with_template('esmis_admission.admission_test_result_mail')
			else:
				raise ValidationError(_("Only admissions who completed the entrance test can be set for evaluation."))

	def test_result_notification(self):
		message = "Action Successfully executed..."
		if self.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_sending_of_email'):
			message = "Unable to send email, please enable email sender or send the email manually."
		else:
			self.send_mail_with_template('esmis_admission.admission_test_result_mail')
		return {
			"type": "ir.actions.client",
			"tag": "display_notification",
			"params": {
				"title": _("Admission"),
				"message": message,
				"sticky": False,
				"type": "info",
				"next": {
					"type": "ir.actions.act_window_close",
				},
			},
		}

	''' for_evaluation '''
	def evaluate_with_confirm(self):
		if self._context.get('evaluate', False) == 'qualified':
			return self.evaluate_qualified()
		else:
			return self.evaluate_not_qualified()

	def evaluate_qualified(self):
		for rec in self:
			if self.active_course_id.id not in self.env.user.course_ids.ids:
				raise ValidationError(_('You are not allowed to evaluate this admission.'))
			if rec.state != 'for_evaluation':
				raise ValidationError(_("Only admissions who are being evaluated can be qualified."))
			rec.update({
				'evaluated_by_id': self.env.user.id,
				'evaluated_datetime': fields.Datetime.now(),
				'qualified_course_id': rec.active_course_id.id,
				'for_admission_by_id': self.env.user.id,
				'for_admission_datetime': fields.Datetime.now(),
				'state': 'for_admission',
			})
			if rec.student_id:
				rec.update({
					'student_no_undg': rec.student_id.student_no_undg,
					'student_no_grad': rec.student_id.student_no_grad,
				})
			else:
				student_no_grad = False
				student_no_undg = False
				if rec.admission_type_1 == "grad":
					student_no_grad = 'G' + str(self.env['ir.sequence'].next_by_code('esmis.student.no.grad'))
				else:
					student_no_undg = 'C' + str(self.env['ir.sequence'].next_by_code('esmis.student.no.undg'))
				rec.update({
					'student_no_undg': student_no_undg,
					'student_no_grad': student_no_grad,
				})

	def evaluate_not_qualified(self):
		for rec in self:
			if self.active_course_id.id not in self.env.user.course_ids.ids:
				raise ValidationError(_('You are not allowed to evaluate this admission.'))
			if rec.state == 'for_evaluation':
				active_course_id = False
				if rec.active_course_id.id == rec.course1_id.id:
					if rec.course2_id != False:
						active_course_id = rec.course2_id.id
				elif rec.active_course_id.id == rec.course2_id.id:
					if rec.course3_id != False:
						active_course_id = rec.course3_id.id
				course_id = rec.active_course_id.id
				return {
					"name": "Enter Reason",
					"view_mode": "form",
					"res_model": "esmis.admission.not.qualified.wiz",
					"view_id": rec.env.ref(
						"esmis_admission.esmis_admission_not_qualified_wizard_form_view"
					).id,
					"type": "ir.actions.act_window",
					"target": "new",
					'context': {
						'default_admission_id': rec.id,
						'default_course_id': course_id,
						'default_active_course_id': active_course_id,
					},
				}
			else:
				raise ValidationError(_("Only admissions who are being evaluated can be not qualified."))

	def admitted_record_name(self):
		name = (self.last_name + ", " + self.first_name +
				("" if not self.middle_name else " " + str(self.middle_name)) +
				("" if not self.suffix else " " + str(self.suffix)))
		return "[%s] %s" %(str(self.admission_number), name)

	def _get_admission_create_student_values(self):
		civil_status = False
		if self.civil_status:
			civil_status = self.civil_status.title()
		vals = {
			# 'lrn': rec.lrn,
			'name': self.admission_student_full_name(),
			'full_name': self.admission_student_full_name(),
			'student_image': self.student_image,
			'last_name': self.last_name,
			'first_name': self.first_name,
			'middle_name': self.middle_name,
			'suffix_name': self.suffix,
			'gender': self.gender.title(),
			"street":self.street,
			"street2":self.street2,
			"zip":self.zip,
			"city_id":self.city_id.id,
			"state_id":self.state_id.id,
			"country_id":self.country_id.id,
			'birthdate': self.birthdate,
			'father_full_name': self.father_name,
			'father_birthdate': self.father_birthdate,
			'father_educ_attain': self.father_educ_attain,
			'father_occupation': self.father_occupation,
			'father_company': self.father_company,
			'father_monthly_income': self.father_monthly_income,
			'father_contact_no': self.father_contact,
			'mother_full_name': self.mother_name,
			'mother_birthdate': self.mother_birthdate,
			'mother_educ_attain': self.mother_educ_attain,
			'mother_occupation': self.mother_occupation,
			'mother_company': self.mother_company,
			'mother_monthly_income': self.mother_monthly_income,
			'mother_contact_no': self.mother_contact,
			'guardian_full_name': self.guardian_name,
			'guardian_birthdate': self.guardian_birthdate,
			'guardian_educ_attain': self.guardian_educ_attain,
			'guardian_occupation': self.guardian_occupation,
			'guardian_company': self.guardian_company,
			'guardian_monthly_income': self.guardian_monthly_income,
			'guardian_contact_no': self.guardian_contact,
			'email': self.email_address,
			'mobile_number': self.mobile,
			'phone_number': self.phone,
			'birthplace': self.place_of_birth,
			'nationality': self.citizenship,
			'religion': self.religion,
			'civil_status':  civil_status,
			'student_no_undg': self.student_no_undg,
			'student_no_grad': self.student_no_grad,
			'qualified_course_id': self.qualified_course_id.id,
			'current_department_id': self.qualified_department_id.id,
			'is_student': True,
			'current_course_id': self.qualified_course_id.id,
			'current_year_level': 1,
			# 'qualified_department_id': current_curriculum_id,
		}
		return vals

	def admission_admit(self):
		for rec in self:
			if rec.qualified_course_id:
				# Get the current curriculum based on qualified_course_id
				current_curriculum_id = self.get_current_curriculum(rec.qualified_course_id.id)
				if current_curriculum_id:
					# Check if the student_id already exist
					if rec.student_id:
						# Update the admission record
						rec.update({
							'state': 'admitted',
							'admitted_by_user_id': self.env.user.id,
							'admitted_date': fields.Datetime.now(),
							'name': self.admitted_record_name(),
							# 'student_no_undg': rec.student_id.student_no_undg,
							# 'student_no_grad': rec.student_id.student_no_grad,
						})
						# Update the student record
						rec.student_id.update({
							'current_course_id': rec.qualified_course_id.id,
							# 'current_curriculum_id': current_curriculum_id,
							'current_year_level': 1,
							# 'admission_ids': Command.link(rec.id)
						})
					else:
						# Update the admission record
						rec.update({
							'state': 'admitted',
							'admitted_by_user_id': self.env.user.id,
							'admitted_date': fields.Datetime.now(),
							'name': self.admitted_record_name(),
						})
						
						student = self.env['res.partner'].sudo().create(rec._get_admission_create_student_values())
						rec.write({
							'student_id': student.id,
							})

				else:
					raise ValidationError("There are no curriculum configured for the qualified program selected.")
			else:
				raise UserError("The qualified program must be set to admit this applicant.")

	def cancel_with_confirm(self):
		return {
			"name": "Confirmation",
			"view_mode": "form",
			"res_model": "esmis.confirm.with.password.wiz",
			"view_id": self.env.ref(
				"esmis_admission.esmis_confirm_with_password_wiz_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			'context': {
				'default_admission_id': self.id,
				'with_model': False,
				'with_action': 'self.admission_cancel()',
			},
		}

	def admission_cancel(self):
		self.update({
			'state': 'cancelled',
			'cancelled_by_user_id': self.env.user.id,
			'cancelled_date': datetime.today(),
			})

	def admission_reconsider(self):
		current_courses = [(4, self.course1_id.id), (4, self.course2_id.id)]
		if self.course3_id:
			current_courses.append((4, self.course3_id.id))

		return {
			"name": "Select Courses",
			"view_mode": "form",
			"res_model": "admission.update.selected.courses",
			"view_id": self.env.ref(
				"esmis_admission.esmis_admission_update_selected_courses_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			'context': {
				'default_admission_id': self.id,
				'default_current_course_ids': current_courses,
				'default_whole_level': self.whole_level,
			},
		}

	@api.onchange('admission_type_1')
	def _level_selected(self):
		self.course1_id = False
		self.course2_id = False
		self.course3_id = False
		self.level_flag = False
		self.admission_type_2 = False
		self.admission_type_3 = False

	@api.onchange("admission_type_2")
	def _admission_type_2_onchange(self):
		for rec in self:
			if rec.admission_type_1 == "undergrad" and rec.admission_type_2:
				rec.whole_level = 'Undergraduate'
				rec.admission_type = rec.admission_type_2

	@api.onchange("admission_type_3")
	def _admission_type_3_onchange(self):
		for rec in self:
			if rec.admission_type_1 == "grad" and rec.admission_type_3:
				if rec.admission_type_3 in ['graduate', 'transferee2']:
					rec.whole_level = 'Masteral'
				elif rec.admission_type_3 in ['graduate2', 'transferee3']:
					rec.whole_level = 'Doctorate'
				rec.admission_type = rec.admission_type_3

	@api.onchange('course1_id')
	def _first_course_selection_change(self):
		self.course2_id = False
		self.course3_id = False

	@api.onchange('course2_id')
	def _second_course_selection_change(self):
		self.course3_id = False

	@api.onchange('email_address')
	def _email_unique_check(self):
		if self.email_address:
			user_with_email = self.env['res.users'].sudo().search_read([('login', '=', self.email_address)])
			if len(user_with_email):
				self.email_address = ""
				return {
					'warning': {'title': _('Admission'), 'message': _("Email Already Exists..."),},
				}

	@api.constrains('work_experience_ids')
	def check_latest_work(self):
		for rec in self:
			current_latest_work_exp_id = False
			for exp in rec.work_experience_ids:
				if current_latest_work_exp_id:
					if exp.start > current_latest_work_exp_id.start:
						current_latest_work_exp_id = exp
						exp.write({
							'is_latest': True
							})
					else:
						exp.write({
							'is_latest': False
							})

				else:
					current_latest_work_exp_id = exp
					exp.write({
						'is_latest': True
					})


class eSMISWorkExperience(models.Model):
	_name = 'esmis.admission.work.experience'
	_description = "eSMIS Admission Work Experience"

	name = fields.Char(string="Company Name", required=True)
	role = fields.Char(string="Role")
	address = fields.Char(string="Address")
	start = fields.Date(string="Date Started")
	end = fields.Date(string="Date Ended")
	is_latest = fields.Boolean(string="Date Ended")
	admission_id = fields.Many2one('esmis.admission', string="Admission")

class ResPartner(models.Model):
	_inherit = 'res.partner'

	@api.model
	@api.returns('self', lambda value: value.id)
	def find_or_create(self, email, assert_valid_email=False):
		parsed_name, parsed_email = self._parse_partner_name(email)
		if not parsed_email and assert_valid_email:
			raise ValueError(_('A valid email is required for find_or_create to work properly.'))
		partners = self.search([('email', '=ilike', parsed_email)], limit=1)
		if partners:
			res = super(ResPartner, self).find_or_create(email, assert_valid_email=assert_valid_email)
			return res
		create_values = {'name': parsed_name or "Test", 'last_name': parsed_name or "Test",'first_name': parsed_name or "Test", 'middle_name': parsed_name or "Test", 'suffix_name': parsed_name or "Test",}
		if parsed_email:  # keep default_email in context
			create_values['email'] = parsed_email
		return self.create(create_values)
