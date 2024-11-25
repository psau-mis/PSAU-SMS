from odoo import api, fields, models, tools, _
from datetime import datetime
from odoo.tools.safe_eval import safe_eval


class eSMISStudents(models.Model):
	_inherit = 'res.partner'

	admission_ids = fields.Many2many('esmis.admission', string="Admissions", compute="_compute_student_admissions")
	city_id = fields.Many2one('res.city', string="City")
	qualified_course_id = fields.Many2one('esmis.course', string="Qualified Course")
	senior_high_school_name = fields.Char(string="High School", related="admission_ids.senior_high_school_name")

	def _default_high_school(self):
		for rec in self.admission_ids:
			return rec.senior_high_school_name

	def _compute_student_admissions(self):
		for rec in self:
			student_admission = rec.env['esmis.admission'].search([('student_id', '=', rec.id)])
			rec.admission_ids = [(4, admission.id) for admission in student_admission]

	@api.model
	def student_cog_selection(self):
		return {
			"name": "Student COG",
			"view_mode": "form",
			"res_model": "student.cog.wiz",
			"view_id": self.env.ref(
				"esmis_admission.student_cog_wiz_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
		}

	@api.model
	def certification_of_latin_honors_input(self):
		return {
			"name": "Certification of Latin Honors",
			"view_mode": "form",
			"res_model": "certification.latin.honor.wiz",
			"view_id": self.env.ref(
				"esmis_admission.esmis_certification_latin_honor_wiz_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
		}

	@api.model
	def cav_input(self):
		return {
			"name": "CERTIFICATION, AUTHENTICATION AND VERIFICATION",
			"view_mode": "form",
			"res_model": "cav.wiz",
			"view_id": self.env.ref(
				"esmis_admission.esmis_cav_wiz_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
		}

	@api.model
	def get_date_and_user_print(self):
		return '%s | %s' %(str(fields.Datetime.now()), self.env.user.name)

	@api.model
	def check_instance(self, value):
		try:
			return float(value)
		except Exception as e:
			return False

	@api.model
	def get_clh_signatories(self):
		signatories_id = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.university_registrar_id')
		if signatories_id:
			signatories_id = self.env['esmis.signatories'].search([('id', '=', int(signatories_id))])
		return signatories_id

	#not usable anymore
	def get_lec_lab_from_curriculum(self, subject_id):
		enrolled_id = False
		for enrollment in self.enrollment_ids.filtered(lambda enrollment: enrollment.status == 'enrolled'):
			enrolled_id = enrollment
		curriculum_one2many_fields = ['rec_1st_1st', 'rec_1st_2nd', 'rec_1st_3rd', 'rec_2nd_1st', 'rec_2nd_2nd',
			'rec_2nd_3rd', 'rec_3rd_1st', 'rec_3rd_2nd', 'rec_3rd_3rd', 'rec_4th_1st', 'rec_4th_2nd', 'rec_4th_3rd',
			'rec_5th_1st', 'rec_5th_2nd', 'rec_5th_3rd', 'rec_6th_1st', 'rec_6th_2nd', 'rec_6th_3rd', 'rec_7th_1st', 
			'rec_7th_2nd', 'rec_7th_3rd', 'rec_8th_1st', 'rec_8th_2nd', 'rec_8th_3rd', 'rec_9th_1st', 'rec_9th_2nd',
			'rec_9th_3rd']
		for subject in curriculum_one2many_fields:
			if enrolled_id:
				rec_with_existing_subject = safe_eval('curriculum_id.' + str(subject) + '.filtered(lambda sbjct: sbjct.subject_id.id == '+str(subject_id)+')', locals_dict={'curriculum_id': enrolled_id.curriculum_id,})
				if len(rec_with_existing_subject):
					for rec_sbjct in rec_with_existing_subject:
						return rec_sbjct.lec_hrs_week_1.unit, rec_sbjct.lab_hrs_week_1.unit
		return 0, 0

	def get_lec_lab_from_enrollment(self, subject_id, sy_id):
		for enrollment in self.enrollment_ids.filtered(lambda enrollment: enrollment.school_year_id.id == sy_id):
			subject_enrolled = enrollment.subject_enrolled.filtered(lambda sbjct: sbjct.subject_id.subject_id.id == subject_id)
			for sbjcte in subject_enrolled:
				return sbjcte.lec_hrs_week.unit, sbjcte.lab_hrs_week.unit
		return 0, 0

	def get_year_level_from_enrollment(self, sy_id):
		for enrollment in self.enrollment_ids.filtered(lambda enrollment: enrollment.school_year_id.id == sy_id):
			if enrollment.year_level:
				return enrollment.year_level + " Year"
		return ""

	@api.model
	def get_gpa_detail(self):
		"""
		returns list
		gpa dictionary of dictionaries, school year id is the key and dictionary of grade details is the value
		need more improvements, sort sy and sem
		"""
		gpa = []
		school_years = []
		for rec in self.grades_ids:

			float_grade_point = 0.0
			grade_point = False
			try:
				grade_point = '{0:.2f}'.format(float(rec.subject_id.subject_unit) * float(rec.actual_final_ave))
				float_grade_point = float(rec.subject_id.subject_unit) * float(rec.actual_final_ave)
			except Exception as e:
				grade_point = rec.actual_final_ave
			curriculum_subject_lec, curriculum_subject_lab = self.get_lec_lab_from_enrollment(rec.subject_id.id, rec.school_year_id.id)
			gpa.append({
				'subject_code': rec.subject_id.subject, 'subject_unit': rec.subject_id.subject_unit,
				'subject_unit_str': '{0:.1f}'.format(rec.subject_id.subject_unit),
				'grade': rec.actual_final_ave, 'grade_point': grade_point, 'float_grade_point': float_grade_point,
				'year_from': rec.school_year_id.year_from, 'year_to': rec.school_year_id.year_to,
				'sem': rec.school_year_id.sem, 'subject_title': rec.subject_id.descriptive_title,
				'subject_lec': curriculum_subject_lec, 'subject_lab': curriculum_subject_lab,
				'year_level': self.get_year_level_from_enrollment(rec.school_year_id.id),
				})
			
			if [rec.school_year_id.year_from, rec.school_year_id.year_to] not in school_years:
				school_years.append([rec.school_year_id.year_from, rec.school_year_id.year_to])
		school_years.sort(key = lambda year: year[0])
		grouped_school_years = []
		for sy in school_years:
			first_sem = list(filter(lambda group: group['year_from'] == sy[0] and group['year_to'] == sy[1] and group['sem'] == '1st Semester', gpa))
			second_sem = list(filter(lambda group: group['year_from'] == sy[0] and group['year_to'] == sy[1] and group['sem'] == '2nd Semester', gpa))
			mid_term = list(filter(lambda group: group['year_from'] == sy[0] and group['year_to'] == sy[1] and group['sem'] == 'Mid-Term', gpa))
			
			fs_total_units = sum([sem['subject_unit'] for sem in first_sem])
			fs_total_grade_point = sum([sem['float_grade_point'] for sem in first_sem])
			ss_total_units = sum([sem['subject_unit'] for sem in second_sem])
			ss_total_grade_point = sum([sem['float_grade_point'] for sem in second_sem])
			mt_total_units = sum([sem['subject_unit'] for sem in mid_term])
			mt_total_grade_point = sum([sem['float_grade_point'] for sem in mid_term])
			
			fs_gpa = (fs_total_grade_point / fs_total_units) if fs_total_grade_point != 0 and fs_total_units != 0 else 0.00
			ss_gpa = (ss_total_grade_point / ss_total_units) if ss_total_grade_point != 0 and ss_total_units != 0 else 0.00
			my_gpa = (mt_total_grade_point / mt_total_units) if mt_total_grade_point != 0 and mt_total_units != 0 else 0.00
			list_of_totals = [
				{'total_units': fs_total_units, 'total_units_str': '{0:.1f}'.format(fs_total_units), 'total_grade_point':fs_total_grade_point, 'total_grade_point_str':'{0:.2f}'.format(fs_total_grade_point), 'gpa': '{0:.2f}'.format(fs_gpa), 'total_lab': sum([sem['subject_lab'] for sem in first_sem]), 'total_lec': sum([sem['subject_lec'] for sem in first_sem]), 'sem': '1st Semester'},
				{'total_units': ss_total_units, 'total_units_str': '{0:.1f}'.format(ss_total_units), 'total_grade_point':ss_total_grade_point, 'total_grade_point_str':'{0:.2f}'.format(ss_total_grade_point), 'gpa': '{0:.2f}'.format(ss_gpa), 'total_lab': sum([sem['subject_lab'] for sem in second_sem]), 'total_lec': sum([sem['subject_lec'] for sem in second_sem]), 'sem': '2nd Semester'},
				{'total_units': mt_total_units, 'total_units_str': '{0:.1f}'.format(mt_total_units), 'total_grade_point':mt_total_grade_point, 'total_grade_point_str':'{0:.2f}'.format(mt_total_grade_point), 'gpa': '{0:.2f}'.format(my_gpa), 'total_lab': sum([sem['subject_lab'] for sem in mid_term]), 'total_lec': sum([sem['subject_lec'] for sem in mid_term]), 'sem': 'Mid-Term'},
			]
			current_sy = (sy + [list_of_totals], [])
			current_sy[1].append(first_sem if len(first_sem) else False)
			current_sy[1].append(second_sem if len(second_sem) else False)
			current_sy[1].append(mid_term if len(mid_term) else False)
			grouped_school_years.append(current_sy)
		return grouped_school_years

	@api.model
	def get_datetime_today(self):
		return datetime.today()

	@api.model
	def get_date_graduation_formatted(self):
		#For reports
		if self.date_of_graduation:
			return self.date_of_graduation.strftime('%B %d, %Y')
		return ''

	@api.model
	def get_some_student_data(self):
		curriculum = ""
		major = ""
		for enrollment in self.enrollment_ids:
			if enrollment.status == 'enrolled':
				curriculum = enrollment.curriculum_id.name or ""
				major = enrollment.curriculum_id.major or ""

		return [curriculum, major]

	@api.model
	def get_student_first_enrolment(self):
		for enrollment in self.enrollment_ids.sorted('create_date'):
			return enrollment.school_year_id.name

		return ""
