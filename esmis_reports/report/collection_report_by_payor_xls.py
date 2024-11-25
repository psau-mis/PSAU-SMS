from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io
from odoo.modules.module import get_module_resource

class CollectionByPayorXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.collection_by_payor_xls'
	_inherit = 'report.report_xlsx.abstract'



	def generate_xlsx_report(self, workbook, data, partners):
		print("asd", data['cashier'])
		sheet = workbook.add_worksheet('Collection Reports by Payor')
		bold = workbook.add_format({'bold':True})
		bold_right = workbook.add_format({'align': 'right','bold':True})
		psau_format = workbook.add_format({'align': 'left','bold':True, 'font':'monotype old english text', 'size':15})
		title_format = workbook.add_format({'align': 'left', 'size':13})
		date_format = workbook.add_format({'align': 'left', 'size':13})
		row = 9
		col = 0

	
		sheet.insert_image('A2', get_module_resource('esmis_reports', 'static/img', 'logo.jpg'), {'x_scale': 0.5, 'y_scale': 0.4})	
		sheet.merge_range('B2:L2', "PAMPANGA STATE AGRICULTURAL UNIVERSITY", psau_format)
		sheet.merge_range('B3:L3', "COLLECTIONS REPORTS BY PAYOR", title_format)
		sheet.merge_range('B4:L4', "DATE RANGE:" + " " + data['date_from'] + " " + data['date_to'], date_format)
		sheet.merge_range('B5:L5', "O.R COVERED:", date_format)

		fix_header = ['#', 'OR No', 'DATE', 'PAYOR NAME', 'AMOUNT', 'CASHIER']
		for head in fix_header:
			sheet.write(row, col, head, bold)
			col+=1
		# sheet.merge_range(0, 0, 2, 2, "Merged Cells", bold)
		sheet.set_column(0, 1, 11)
		sheet.set_column(2, 2, 20)
		sheet.set_column(3, 3, 50)
		sheet.set_column(4, 4, 20)
		sheet.set_column(5, 5, 20)




		date_from = data['date_from']
		date_to = data['date_to']
		# raise ValidationError(date_from)

		row_data = 10
		col_data = 0
		num_count = 1
		cashier_data = []
		cashier_ids = self.env['esmis.cashier'].search([('invoice_date','>=', date_from),('invoice_date','<=', date_to),('status','in', ('paid','voided'))])
		# raise ValidationError(str(cashier_ids))
		grand_total = 0
	
		total_amount = 0
		for rec in cashier_ids:
			
			cashier_data.append(num_count)
			cashier_data.append(rec.or_no)
			cashier_data.append(rec.invoice_date)
			if rec.status == 'paid':
				cashier_data.append(rec.payer_name)
				cashier_data.append("{:.2f}".format(rec.total_amount_paid))
				total_amount += rec.total_amount_paid
			else:
				cashier_data.append("*** Void Transaction ***")
				cashier_data.append("{:.2f}".format(0))
			
			
			num_count+=1

			# raise ValidationError(str(cashier_data))

		
			for recs in cashier_data:
				sheet.write(row_data, col_data, str(recs), bold)
				col_data+=1
			col_data=0
			row_data+=1
			cashier_data = []
		num_count = 1

		grand_total += total_amount
		
		
		sheet.write(row_data, 3, 'TOTAL', bold_right)
		sheet.write(row_data, 4, "{:.2f}".format(grand_total, bold))
