from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io
from odoo.modules.module import get_module_resource

class CollectionByFundXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.collection_by_fund_xls'
	_inherit = 'report.report_xlsx.abstract'



	def generate_xlsx_report(self, workbook, data, partners):
		sheet = workbook.add_worksheet('Collection Reports by Fund')
		bold = workbook.add_format({'bold':True})
		bold_right = workbook.add_format({'align': 'right','bold':True})
		psau_format = workbook.add_format({'align': 'left','bold':True, 'font':'monotype old english text', 'size':15})
		title_format = workbook.add_format({'align': 'left', 'size':13})
		date_format = workbook.add_format({'align': 'left', 'size':13})
		header_format = workbook.add_format({'align': 'center','bold':True,'border': 1})
		row = 9
		col = 0


		sheet.set_column(0, 1, 11)
		sheet.insert_image('A2', get_module_resource('esmis_reports', 'static/img', 'logo.jpg'), {'x_scale': 0.5, 'y_scale': 0.4})	
		sheet.merge_range('B2:L2', "PAMPANGA STATE AGRICULTURAL UNIVERSITY", psau_format)
		sheet.merge_range('B3:L3', "COLLECTIONS REPORTS BY FUND", title_format)
		sheet.merge_range('B4:L4', "DATE RANGE:" + " " + data['date_from'] + " " + data['date_to'], date_format)


		fix_header = ['#', 'CODE', 'CLASSIFICATION', 'AMOUNT']
		for head in fix_header:
			sheet.write(row, col, head, bold)
			col+=1
		# sheet.merge_range(0, 0, 2, 2, "Merged Cells", bold)
		sheet.set_column(0, 1, 10)
		sheet.set_column(2, 2, 50)
		sheet.set_column(3, 3, 20)
	
		date_from = data['date_from']
		date_to = data['date_to']
		
		fund_code_ids = self.env['esmis.fees.fund'].search([])
		cashier_ids = self.env['esmis.cashier'].search([('invoice_date','>=', date_from),('invoice_date','<=', date_to),('status','=', 'paid')])
		cashier_line_ids = self.env['esmis.cashier.line'].search([])

		

		row_data = 10
		col_data = 0
		num_count = 1
		fund_data = []

		total_collections = 0
		for rec in fund_code_ids:
			total_per_fund = 0
			for record in cashier_ids:
				for recs in record.cashier_line_ids:
					if recs.fee_id.fund_group.id == rec.id:
						total_per_fund+=recs.amount_paid
						total_collections+=recs.amount_paid
			fund_data.append(num_count)
			fund_data.append(rec.name)
			fund_data.append(rec.description)
			fund_data.append("{:.2f}".format(total_per_fund))

			for recs in fund_data:
				sheet.write(row_data, col_data, str(recs), bold)
				col_data+=1
			col_data=0
			num_count+=1
			row_data+=1
			fund_data = []

		sheet.write(row_data, 2, 'TOTAL COLLECTIONS', bold_right)
		sheet.write(row_data, 3, "{:.2f}".format(total_collections), bold_right)

	