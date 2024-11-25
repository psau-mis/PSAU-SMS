from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io
from odoo.modules.module import get_module_resource


class ReportOfCollectionXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.report_of_collection_xls'
	_inherit = 'report.report_xlsx.abstract'



	def generate_xlsx_report(self, workbook, data, partners):
		print("asd", data['cashier'])
		sheet = workbook.add_worksheet('REPORT OF COLLECTIONS')
		bold = workbook.add_format({'bold':True})
		bold_right = workbook.add_format({'align': 'right','bold':True})
		header_format = workbook.add_format({'align': 'center','bold':True,'border': 1})
		republic_format = workbook.add_format({'align': 'center','bold':True})
		psau_format = workbook.add_format({'align': 'center','bold':True, 'font':'monotype old english text', 'size':15})
		title_format = workbook.add_format({'align': 'center', 'size':13})
		date_format = workbook.add_format({'align': 'center', 'size':10})
		logo_format  = workbook.add_format({'align': 'center'})
		data_format = workbook.add_format({'align': 'center','border': 1})
		payer_format = workbook.add_format({'align': 'left','bold':True,'border': 1})
		grand_total_format = workbook.add_format({'align': 'right','bold':True,'border': 1})

		right_align_format = workbook.add_format({'align': 'right','border': 1})

		# sheet.insert_image('A1', 'logo.jpg')
		
		sheet.insert_image('C2', get_module_resource('esmis_reports', 'static/img', 'logo.jpg'), {'x_scale': 0.6, 'y_scale': 0.6})
		sheet.merge_range(1, 0, 1, 6, "Republic of the Philippines", republic_format)
		sheet.merge_range(2, 0, 2, 6, "Pampanga State Agricultural University", psau_format)
		sheet.merge_range(3, 0, 3, 6, "PAC, Magalang, Pampanga", republic_format)
		sheet.merge_range(4, 0, 4, 6, "REPORT OF COLLECTIONS", title_format)
		sheet.merge_range(5, 0, 5, 6, "DATE RANGE:" + " " + data['date_from'] + " " + data['date_to'], date_format)

		row = 9
		col = 0
		fix_header = ['No', 'Official Receipt', 'Account']
		sub_header = ['Date', 'Number', 'Payer', 'Code', 'Name', 'Amount']
		for head in fix_header:
			sheet.write(row, col, head, header_format)
			col+=1
		row=10
		col=1
		sheet.merge_range(9, 1, 9, 2, "Official Receipt", header_format)
		sheet.write(9, 3, '', header_format)
		sheet.merge_range(9, 4, 9, 6, "Account", header_format)

		for head in sub_header:
			sheet.write(row, col, head, header_format)
			col+=1
		sheet.write(row, 0, '', header_format)
		# sheet.merge_range(9, 0, 2, 2, "Merged Cells", bold)
		

		sheet.set_column(0, 0, 9)
		sheet.set_column(1, 2, 20)
		sheet.set_column(3, 3, 50)
		sheet.set_column(4, 4, 12)
		sheet.set_column(5, 5, 32)
		sheet.set_column(6, 6, 20)


		date_from = data['date_from']
		date_to = data['date_to']
		# raise ValidationError(date_from)

		row_data = 11
		col_data = 0
		num_count = 1
		cashier_data = []
		cashier_ids = self.env['esmis.cashier'].search([('invoice_date','>=', date_from),('invoice_date','<=', date_to),('status','=', 'paid')])
		# raise ValidationError(str(cashier_ids))
		grand_total = 0
	
		total_amount = 0
		for rec in cashier_ids:
			for recs in rec.cashier_line_ids:
				
				cashier_data.append(num_count)
				cashier_data.append(rec.invoice_date)
				cashier_data.append(rec.or_no)
				cashier_data.append(rec.payer_name)
				cashier_data.append(recs.fee_id.account_id)
				cashier_data.append(recs.fee_id.name)
				cashier_data.append("{:.2f}".format(recs.amount_paid))
				total_amount += recs.amount_paid
				num_count+=1
		
				for recs in cashier_data:
					if col_data == 0:
						sheet.write(row_data, col_data, str(recs), right_align_format)
					elif col_data == 3:
						sheet.write(row_data, col_data, str(recs), payer_format)
					elif col_data == 6:
						sheet.write(row_data, col_data, str(recs), right_align_format)
					else:
						sheet.write(row_data, col_data, str(recs), data_format)
					col_data+=1
				col_data=0
				row_data+=1
				for recs in cashier_data:
					sheet.write(row_data, col_data, '', payer_format)
					
					col_data+=1
				col_data=0
				row_data+=1
				cashier_data = []
		num_count = 1

		grand_total += total_amount
		
		sheet.merge_range(row_data, 0, row_data, 5, "GRAND TOTAL", grand_total_format)
		sheet.write(row_data, 6, "{:.2f}".format(grand_total), data_format)
