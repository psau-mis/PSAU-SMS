from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CorCollectionsWiz(models.TransientModel):
	_name = 'esmis.cor.collections.wiz'

	"""
		pass context
		with_action = callable function on string format
		admission_id = id of the admission where the action will be executed
	"""

	school_year_id = fields.Many2many("esmis.school.year", string="School Year")
	section_id = fields.Many2one('esmis.sections', string="Section")


	def print_xlsx(self):
		sec_ids = []
		sy_ids = []
		if self.school_year_id:	
			for rec in self.school_year_id:
				sy_ids.append(rec.id)
			if self.section_id:
				for secs in self.section_id:
					sec_ids.append(secs.id)
				enrollments = self.env['esmis.enrollment'].search_read([('school_year_id','in', sy_ids), ('status','=', 'enrolled'), ('section_id','in', sec_ids)])
			else:
				enrollments = self.env['esmis.enrollment'].search_read([('school_year_id','in', sy_ids), ('status','=', 'enrolled')])
		else:

			if self.section_id:
				for secs in self.section_id:
					sec_ids.append(secs.id)
				enrollments = self.env['esmis.enrollment'].search_read([('status','=', 'enrolled'), ('section_id','in', sec_ids)])
			else:
				enrollments = self.env['esmis.enrollment'].search_read([('status','=', 'enrolled')])
		fees = self.env['esmis.coa'].search_read([])
		# raise ValidationError(str(enrollments))
		data = {
			'enrollments': enrollments,
			'fees': fees,
			'form_date':self.read()[0]
		}
		return self.env.ref('esmis_reports.report_cor_collections_xlsx').report_action(self, data=data)



# import time
# import datetime
# from dateutil.relativedelta import relativedelta
# from odoo import fields, models, api, _
# from odoo.tools import float_is_zero
# from odoo.tools import date_utils
# import io
# import json
# try:
#    from odoo.tools.misc import xlsxwriter
# except ImportError:
#    import xlsxwriter


# class CorCollectionsWiz(models.TransientModel):
# 	_name = 'esmis.cor.collections.wiz'

# 	"""
# 		pass context
# 		with_action = callable function on string format
# 		admission_id = id of the admission where the action will be executed
# 	"""

# 	enrollment_ids = fields.Many2many("esmis.enrollment", string="Enrollment")


# 	start_date = fields.Datetime(string="Start Date",
# 								default=time.strftime('%Y-%m-01'),
# 								required=True)
# 	end_date = fields.Datetime(string="End Date",
# 							  default=datetime.datetime.now(),
# 							  required=True)
# 	def print_xlsx(self):
# 		if self.start_date > self.end_date:
# 			raise ValidationError('Start Date must be less than End Date')
# 		data = {
# 			'start_date': self.start_date,
# 			'end_date': self.end_date,
# 		}
# 		return {
# 			'type': 'ir.actions.report',
# 			'data': {'model': 'esmis.cor.collections.wiz',
# 					'options': json.dumps(data,
# 										  default=date_utils.json_default),
# 					'output_format': 'xlsx',
# 					'report_name': 'Excel Report',
# 					},
# 			'report_type': 'xlsx',
# 		}
# 	def get_xlsx_report(self, data, response):
# 		from_date = data['from_date']
# 		to_date = data['to_date']
# 		output = io.BytesIO()
# 		workbook = xlsxwriter.Workbook(output, {'in_memory': True})
# 		sheet = workbook.add_worksheet()
# 		cell_format = workbook.add_format(
# 		   {'font_size': '12px', 'align': 'center'})
# 		head = workbook.add_format(
# 		   {'align': 'center', 'bold': True, 'font_size': '20px'})
# 		txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
# 		sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
# 		sheet.merge_range('A6:B6', 'From Date:', cell_format)
# 		sheet.merge_range('C6:D6', from_date, txt)
# 		sheet.write('F6', 'To Date:', cell_format)
# 		sheet.merge_range('G6:H6', to_date, txt)
# 		workbook.close()
# 		output.seek(0)
# 		response.stream.write(output.read())
# 		output.close()	