# Part of eSMIS App. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)


class eSMISEnrollment(models.Model):
	_name = "esmis.enrollment"
	_description = "Student Enrollment"
	_order = "id asc"
	_rec_name = "enrollment_no"
	_inherit = ["mail.thread", "mail.activity.mixin"]

	company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company.id)

	enrollment_no = fields.Char('Enrollment No.')
	student_id = fields.Many2one('res.partner', string="Student", domain="[('is_student','=',True)]")
	admission_id = fields.Many2one('esmis.admission', string="Student", domain="[('state','=','admitted')]")

	# Courses
	course_id = fields.Many2one('esmis.course', "Course", store=True)
	department_id = fields.Many2one('esmis.department', "School/College",
									related="course_id.department_id", readonly=True, store=True)

	subject_ids = fields.Many2many('esmis.subjects')

	validate_by_id = fields.Many2one("res.users", "Validated By", readonly=True)
	validate_datetime = fields.Datetime("Date Validated", readonly=True)

	enrolled_by_id = fields.Many2one("res.users", "Enrolled By", readonly=True)
	enrolled_datetime = fields.Datetime("Date Enrolled", readonly=True)

	cancelled_by_id = fields.Many2one("res.users", "Cancelled By", readonly=True)
	cancelled_datetime = fields.Datetime("Date Cancelled", readonly=True)

	company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
	status = fields.Selection([('new', 'New'), ('validate', 'Validated'),
							  ('enrolled', 'Enrolled'), ('complete', 'Completed'),
							  ('drop', 'Dropped'), ('cancelled', 'Cancelled')],
							  required=True, default='new')

	school_year_id = fields.Many2one('esmis.school.year', string="School Year", domain="[('state','=','Active')]")
	student_image = fields.Binary("Student Image", related="student_id.student_image")
	# stud_image_filename = fields.Char("Student Image Filename", related="student_id.stud_image_filename")

	year_level = fields.Selection([("1st", "1st Year"),
						 ("2nd", "2nd Year"),
						 ("3rd", "3rd Year"),
						 ("4th", "4th Year"),
						 ("5th", "5th Year"),
						 ("6th", "6th Year"),
						 ("7th", "7th Year"),
						 ("8th", "8th Year"),
						 ("9th", "9th Year"),], required=True)
	auto_email_deactive = fields.Boolean(string="Auto Email", compute="_compute_auto_email")
	scholar = fields.Selection([('ched', 'CHED')], string="Scholarship")
	scholar1 = fields.Selection([('ched', 'CHED')], string="CHED")
	has_portal = fields.Boolean('Have Portal Access?', default=False)

	def _compute_auto_email(self):
		for rec in self:
			rec.auto_email_deactive = rec.env['ir.config_parameter'].sudo().get_param('esmis_enrollment.enrollment_disable_sending_of_email')

	@api.onchange('student_id')
	def get_course(self):
		for rec in self:
			rec.course_id = rec.student_id.current_course_id


	def send_mail_with_template(self, template, context={}):
		mail_template = self.env.ref(template)
		self.with_context(context).message_post_with_template(template_id=mail_template.id)

	def undo_validation(self):
		for rec in self:
			rec.status = "new"

	def on_validate(self):
		for rec in self:
			rec.status = "validate"

	@api.model
	def default_password(self):
		default_pass = self.env.user.company_id.generate_password()
		return default_pass


	def on_enrolled(self):

		x_group_portal_user = self.env.ref('base.group_portal')
		default_pass = self.default_password()
		password_write_date = datetime.now() - timedelta(days=1)
		for rec in self:
			if not rec.enrollment_no:
				rec.enrollment_no = self.env['ir.sequence'].next_by_code('esmis.enrollment.no')
			rec.status = "enrolled"
			rec.has_portal = True

			vals = {
				"name": rec.student_id.name,
				"login": rec.student_id.email,
				"password": default_pass,
				'password_write_date': password_write_date,
				'partner_id': rec.student_id.id,
				'groups_id': [(6, 0, [x_group_portal_user.id])]
			}
			

			for recs in rec.student_id:
				
				civil_status = False
				if recs.civil_status:
					civil_status = recs.civil_status.title()
				name = ''
				if recs.last_name:
					name += recs.last_name + ', '
				if recs.first_name:
					name += recs.first_name + ' '
				if recs.middle_name:
					name += recs.middle_name + ' '
				if recs.suffix_name:
					name+= recs.suffix_name
					
				# student_profile = {
				# 	# 'lrn': rec.lrn,
				# 	# 'student_image': rec.student_image,
				# 	'name': name,
				# 	'full_name': name,
				# 	'last_name': recs.last_name,
				# 	'first_name': recs.first_name,
				# 	'middle_name': recs.middle_name,
				# 	'suffix_name': recs.suffix,
				# 	'student_no_undg': recs.student_no_undg,
				# 	'student_no_grad': recs.student_no_grad,
				# 	'gender': recs.gender.title(),
				# 	'birthdate': recs.birthdate,
				# 	'father_full_name': recs.father_name,
				# 	'father_birthdate': recs.father_birthdate,
				# 	'father_educ_attain': recs.father_educ_attain,
				# 	'father_occupation': recs.father_occupation,
				# 	'father_company': recs.father_company,
				# 	'father_monthly_income': recs.father_monthly_income,
				# 	'father_contact_no': recs.father_contact,
				# 	'mother_full_name': recs.mother_name,
				# 	'mother_birthdate': recs.mother_birthdate,
				# 	'mother_educ_attain': recs.mother_educ_attain,
				# 	'mother_occupation': recs.mother_occupation,
				# 	'mother_company': recs.mother_company,
				# 	'mother_monthly_income': recs.mother_monthly_income,
				# 	'mother_contact_no': recs.mother_contact,
				# 	'guardian_full_name': recs.guardian_name,
				# 	'guardian_birthdate': recs.guardian_birthdate,
				# 	'guardian_educ_attain': recs.guardian_educ_attain,
				# 	'guardian_occupation': recs.guardian_occupation,
				# 	'guardian_company': recs.guardian_company,
				# 	'guardian_monthly_income': recs.guardian_monthly_income,
				# 	'guardian_contact_no': recs.guardian_contact,
				# 	'email': recs.email_address,
				# 	'mobile_number': recs.mobile,
				# 	'phone_number': recs.phone,
				# 	'birthplace': recs.place_of_birth,
				# 	'nationality': recs.citizenship,
				# 	'religion': recs.religion,
				# 	'civil_status': civil_status,
				# 	'current_course_id': recs.qualified_course_id.id,
				# 	'current_department_id': recs.qualified_department_id.id,
				# 	'is_student': True,
					
				# }

				# student_prof = self.env['res.partner'].search([('student_no_undg','=', recs.student_no_undg),('student_no_grad','=',recs.student_no_grad),('is_student','=',True)])
				# # raise ValidationError(student_profile)
				# if not student_prof:
				# 	# raise ValidationError("qwe")
				# 	self.env["res.partner"].sudo().create(student_profile)
				# else:
				# 	raise ValidationError("zxczc")
			

		student_user = self.env['res.users'].search([('login','=', self.student_id.email),('groups_id','=',x_group_portal_user.id)])
		if student_user:
			pass
		else:
			self.env["res.users"].create(vals)

		has_portal_access = False
		ctr = 0
		enrollment_ids = self.env['esmis.enrollment'].search([('student_id','=', self.student_id.id),('status','in', ('enrolled','complete'))])
		for rec in enrollment_ids:
			ctr+=1
			if rec.has_portal:  
				has_portal_access = True

		if self.auto_email_deactive:
			message = "Unable to send email, please enable email sender or send the email manually."
		else:	
			message = "Email Sent"
			if ctr > 1 and has_portal_access:	
				self.send_mail_with_template('esmis_enrollment.enrollment_notice_mail_old_student')
			else:
				self.send_mail_with_template('esmis_enrollment.enrollment_notice_mail', context={"password": default_pass})
			return {
					"type": "ir.actions.client",
					"tag": "display_notification",
					"params": {
						"title": _("Enrollment Details & Portal Access"),
						"message": message,
						"sticky": False,
						"type": "info",
						"next": {
							"type": "ir.actions.act_window_close",
						},
					},
				}

	def test_email(self):
			self.send_mail_with_template('esmis_enrollment.enrollment_notice_mail')

	def on_complete(self):
		for rec in self:
			rec.status = "complete"

	def on_drop(self):
		for rec in self:
			rec.status = "drop"

	def on_cancelled(self):
		for rec in self:
			rec.status = "cancelled"

	def print_enrollment_form(self):
		for rec in self:
			return self.env.ref('esmis_enrollment.action_report_enrollment').report_action(rec)

	def error_msg_cor(self):
		raise ValidationError("Unable to print COR. There are unenrolled students selected. To print, filter enrolled students only then print again.")

	
	@api.model
	def student_full_name(self):
		"""name formatter"""
		return (self.student_id.last_name + ", " + self.student_id.first_name +
				("" if self.student_id.middle_name == False else " " + self.student_id.middle_name) +
				("" if self.student_id.suffix_name == False else " " + self.student_id.suffix_name))