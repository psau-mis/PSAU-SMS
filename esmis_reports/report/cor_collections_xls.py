from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io


class CorCollectionsXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.cor_collections_xls'
	_inherit = 'report.report_xlsx.abstract'

	def generate_xlsx_report(self, workbook, data, partners):
		print("asd", data['enrollments'])
		sheet = workbook.add_worksheet('COR')
		bold = workbook.add_format({'bold':True})
		row = 0
		col = 0
		row_data = 0
		col_data = 0
		fix_header = ['Academic Year and Term', 'Student No. Undergraduate', 'Student No. Graduate', 'LRN', 'Last Name', 'First Name', 'Middle Initial', 'Student Name',
		'Campus', 'College Name', 'Program Code', 'Program Name', 'Section Name', 'Year Level', 'Gender', 'Email', 'Phone Number',
		'Lab Units', 'Acad Units', 'Credit Units', 'NSTP Units', 'NSTP Enrolled', 'Calculated Tuition Fee', 'Template ID', 'Template Code', 'UniFast Scholar']
		student_id = self.env['res.partner'].search([('is_student', '=', True)])
		for head in fix_header:
			sheet.write(row, col, head, bold)
			col+=1

		# for fee in data['fees']:
		# 	sheet.write(row, col, fee['name'], bold)
		# 	col+=1

		for rec in data['enrollments']:
			row+=1
			sheet.write(row, col_data, rec['school_year_id'][1], bold)
			for stud in student_id:
				student_no_undg = ""
				student_no_grad = ""
				lrn = ""
				last_name = ""
				first_name = ""
				middle_name = ""
				full_name = ""
				campus = "CAMPUS"
				college_name = ""
				program_code = ""
				course = ""
				section = ""
				year_level = ""
				gender = ""
				email = ""
				mobile = ""
				total_lab_unit = 0
				total_unit = 0
				tota_unit_credit = 0
				nstp_unit = "NSTP UNIT"
				nstp_enrolled = "NSTP ENROLLED"
				calculated_tuition = "CALCULATED TUITION"
				template_id = "TEMPLATE ID"
				template_code = "TEMPLATE CODE"
				unifast_scholar = 0

				if stud.student_no_undg:
					student_no_undg = stud.student_no_undg
				if stud.student_no_grad:
					student_no_grad = stud.student_no_grad
				for adminsion_id in stud.admission_ids:
					if adminsion_id.lrn:
						lrn = adminsion_id.lrn
				if stud.last_name:
					last_name = stud.last_name
				if stud.first_name:
					first_name = stud.first_name
				if stud.middle_name:
					middle_name = stud.middle_name
				if stud.full_name:
					full_name = stud.full_name
				# if campus:
				if rec['department_id'][1]:
					college_name = rec['department_id'][1]
				program_code = self.env['esmis.course'].search([('id', '=', rec['course_id'][0])])
				if program_code.acronym:
					program_code = program_code.acronym
				if rec['course_id'][1]:
					course = rec['course_id'][1]
				sec_id = self.env['esmis.sections'].search([('id', 'in', rec['section_id'])])
				for secs in sec_id:
					if secs:
						section = str(section) + "" + str(secs.name) + ","
				if rec['year_level']:
					year_level = rec['year_level']
				if stud.gender:
					gender = stud.gender
				if stud.email:
					email = stud.email
				if stud.mobile_number:
					mobile = stud.mobile_number
				if rec['total_lab_units']:
					total_lab_unit = rec['total_lab_units']
				if rec['total_units']:
					total_unit = rec['total_units']
				if rec['total_units']:
					total_unit_credit = rec['total_units']
				# if nstp unit:
				# if nstp enrolled:
				# if calculated_tuition:
				# if temp_id:
				# if temp_code:
				# if unifast_scholar:

				# raise ValidationError(rec['student_id'][0])
				if stud.id == rec['student_id'][0]:
					
					sheet.write(row, col_data+1, student_no_undg, bold)
					sheet.write(row, col_data+2, student_no_grad, bold)		
					sheet.write(row, col_data+3, lrn, bold)
					sheet.write(row, col_data+4, last_name, bold)
					sheet.write(row, col_data+5, first_name, bold)
					sheet.write(row, col_data+6, middle_name, bold)
					sheet.write(row, col_data+7, full_name, bold)
					sheet.write(row, col_data+8, campus, bold)
					sheet.write(row, col_data+9, college_name, bold)
					# program_code = self.env['esmis.course'].search([('id', '=', rec['course_id'][0])])
					sheet.write(row, col_data+10, program_code, bold)
					sheet.write(row, col_data+11, course, bold)
					# section = ""
					# # for secs in rec['section_id']:
					# sec_id = self.env['esmis.sections'].search([('id', 'in', rec['section_id'])])
					# for secs in sec_id:
					# 	section = str(section) + "" + str(secs.name) + ","
					sheet.write(row, col_data+12, section, bold)
					sheet.write(row, col_data+13, year_level, bold)
					sheet.write(row, col_data+14, gender, bold)
					sheet.write(row, col_data+15, email, bold)
					sheet.write(row, col_data+16, mobile, bold)
					sheet.write(row, col_data+17, total_lab_unit, bold)
					sheet.write(row, col_data+18, total_unit, bold)
					sheet.write(row, col_data+19, total_unit_credit, bold)
					sheet.write(row, col_data+20, nstp_unit, bold)
					sheet.write(row, col_data+21, nstp_enrolled, bold)
					sheet.write(row, col_data+22, calculated_tuition, bold)
					sheet.write(row, col_data+23, template_id, bold)
					sheet.write(row, col_data+24, template_code, bold)
					sheet.write(row, col_data+25, unifast_scholar, bold)

		for fee in data['fees']:
			sheet.write(0, col, fee['name'], bold)
			
			for rec in data['enrollments']:
				row_data+=1
				for fee_line in rec['fee_line_ids']:
					fee_lines = self.env['esmis.enrollment.fees'].search([('id', '=',fee_line)])
					# raise ValidationError(str(fee['id']))
					if fee_lines.name.id == fee['id']:

						# fee_lines = self.env['esmis.enrollment.fees'].search([('fee_id', '=',fee_line)])
						sheet.write(row_data, col, float(format(fee_lines.amount_paid, ".2f")), bold)
						break
					else:
						sheet.write(row_data, col, 0, bold)
			
			row_data = 0
			col+=1