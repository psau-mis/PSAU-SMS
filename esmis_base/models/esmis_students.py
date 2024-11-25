# -*- coding: utf-8 -*-
# import math 
# from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _
from lxml import etree


   
class EsmisStudents(models.Model):
	_inherit = "res.partner"
	_description = "Students"
	_rec_name = "full_name"

	

	state = fields.Selection([('Unlocked', 'Unlocked'),('Locked', 'Locked')],'Status', default="Unlocked")
	is_student = fields.Boolean()

	student_image = fields.Binary(string="Student Image")

	name = fields.Char(string="Name", default="/")
	full_name = fields.Char(string="Name", compute="_compute_name", store=True)
	last_name = fields.Char(string="Last Name", required=True)
	first_name = fields.Char(string="First Name", required=True)
	middle_name = fields.Char(string="Middle Name")
	suffix_name = fields.Char(string="Suffix Name")

	student_no_undg = fields.Char("Student Number (Undergraduate)")
	student_no_grad = fields.Char("Student Number (Graduate)")

	street = fields.Char()
	street2 = fields.Char()
	zip = fields.Char(change_default=True)
	city = fields.Char()
	state_id = fields.Many2one("res.country.state", string='State/Province', domain="[('country_id', '=?', country_id)]")
	country_id = fields.Many2one('res.country', string='Country')

	email = fields.Char(string="Email Address")
	mobile_number = fields.Char(string="Mobile No.")
	phone_number = fields.Char(string="Phone No.")

	gender = fields.Selection([('Male', 'Male'),('Female', 'Female')], string="Gender")
	birthdate = fields.Date(string="Date of Birth")
	age = fields.Char(compute='_calc_age', string="Age", size=50, readonly=True)
	age2 = fields.Char(compute='_calc_age', string="Age", size=50, readonly=True)
	civil_status = fields.Selection([('Single', 'Single'),
		('Married', 'Married'),
		('Seperated', 'Seperated'),
		('Divorced', 'Divorced'),
		('Widowed', 'Widowed')], string="Civil Status")
	birthplace = fields.Char(string="Place of Birth")
	nationality = fields.Char(string="Citizenship")
	religion = fields.Char(string="Religion")

	# family background fields
	father_full_name = fields.Char(string="Name")
	father_birthdate = fields.Date(string="Birthdate")
	father_educ_attain = fields.Char(string="Highest Educational Attainment")
	father_occupation = fields.Char(string="Occupation/Employement")
	father_company = fields.Char(string="Company Name/Address")
	father_monthly_income = fields.Char(string="Monthly Income")
	father_contact_no = fields.Char(string="Contact No.")

	mother_full_name = fields.Char(string="Name")
	mother_birthdate = fields.Date(string="Birthdate")
	mother_educ_attain = fields.Char(string="Highest Educational Attainment")
	mother_occupation = fields.Char(string="Occupation/Employement")
	mother_company = fields.Char(string="Company Name/Address")
	mother_monthly_income = fields.Char(string="Monthly Income")
	mother_contact_no = fields.Char(string="Contact No.")

	guardian_full_name = fields.Char(string="Name")
	guardian_birthdate = fields.Date(string="Birthdate")
	guardian_educ_attain = fields.Char(string="Highest Educational Attainment")
	guardian_occupation = fields.Char(string="Occupation/Employement")
	guardian_company = fields.Char(string="Company Name/Address")
	guardian_monthly_income = fields.Char(string="Monthly Income")
	guardian_contact_no = fields.Char(string="Contact No.")

	# current_acad
	current_course_id = fields.Many2one('esmis.course', string="Current Program")
	current_department_id = fields.Many2one('esmis.department', string="School/College")
	current_year_level = fields.Integer(string="Current Year Level")
	major = fields.Char(string="Major", related='current_course_id.major')


	date_of_graduation = fields.Date()
	year_graduated = fields.Char(compute="get_year_graduated", store=True)

	entrance_credentials = fields.Char(string="Entrance Credentials")
	# senior_high_school_name = fields.Char(string="High School", default=_default_high_school)
	tag_as_graduate = fields.Selection([('graduate','Graduate')])

	@api.depends('date_of_graduation')
	def get_year_graduated(self):
		for rec in self:
			if rec.date_of_graduation:
				rec.year_graduated = str(datetime.strftime(rec.date_of_graduation, '%Y'))


	@api.model
	def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
		args = list(args or [])
		if name :
			args += ['|', '|' , ('name', operator, name), ('student_no_undg', operator, name),
						('student_no_grad', operator, name)]
		return self._search(args, limit=limit, access_rights_uid=name_get_uid)
	# date_graduated = fields.Date
	# @api.model
	# def get_view(self, view_id=None, view_type='form', **options):
	# 	result = super().get_view(view_id, view_type, **options)

	# 	# Disabling the import button for users who are not in import group
	# 	if view_type == 'tree' or view_type == 'form' or view_type == 'kanban':
	# 		doc = etree.XML(result['arch'])
	# 		# if not self.env.user.has_group('esmis_enrollment.group_esmis_manager'):
	# 		 # When the user is not part of the import group
	# 		for node in doc.xpath("//tree"):
	# 			# Set the import to false
	# 			node.set('import', 'true')
	# 			node.set('create', 'false')
				

	# 		for node in doc.xpath("//form"):
	# 			# Set the import to false
				
	# 			node.set('create', 'false')
	# 			# node.set('import', 'false')

	# 		for node in doc.xpath("//kanban"):
	# 			# Set the import to false
				
	# 			node.set('create', 'false')
	# 			node.set('import', 'true')	
	# 		result['arch'] = etree.tostring(doc)

	# 	return result 

	@api.depends('last_name', 'first_name', 'middle_name', 'suffix_name')
	def _compute_name(self):    
		for recs in self:
			
			name = ''
			if recs.last_name:
				name += recs.last_name + ', '
			if recs.first_name:
				name += recs.first_name + ' '
			if recs.middle_name:
				name += recs.middle_name + ' '
			if recs.suffix_name:
				name+= recs.suffix_name

			recs.full_name = name
			
			if recs.name == "/":
				recs.name = name
			else:
				recs.name = recs.name
					
			
	def lock_student(self):
		self.state = "Locked"
	def unlock_student(self):
		self.state = "Unlocked"

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

	@api.depends('birthdate')
	def _calc_age(self):
		for line in self:
			age = self.compute_age_from_dates(line.birthdate)
			line.age = age[0]
			line.age2 = age[1]

