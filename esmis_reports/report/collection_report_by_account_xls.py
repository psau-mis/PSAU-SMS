from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io
from odoo.modules.module import get_module_resource

class CollectionByAccountXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.collection_by_account_xls'
	_inherit = 'report.report_xlsx.abstract'



	def generate_xlsx_report(self, workbook, data, partners):
		sheet = workbook.add_worksheet('Collection Reports by Fund')
		bold = workbook.add_format({'bold':True})
		bold_center = workbook.add_format({'align': 'center','bold':True})
		psau_format = workbook.add_format({'align': 'left','bold':True, 'font':'monotype old english text', 'size':15})
		row = 9
		col = 0

		sheet.insert_image('A2', get_module_resource('esmis_reports', 'static/img', 'logo.jpg'), {'x_scale': 0.5, 'y_scale': 0.4})	
		sheet.merge_range('B2:L2', "PAMPANGA STATE AGRICULTURAL UNIVERSITY", psau_format)
		sheet.merge_range(5, 0, 5, 7, "COLLECTION REPORT BY ACCOUNT", bold_center)
		sheet.merge_range(6, 0, 6, 7, "DATE RANGE:" + " " + data['date_from'] + " " + data['date_to'], bold_center)
		fix_header = ['#', 'OR#', 'DATE', 'PAYER', 'ACCOUNT', 'AMOUNT']
		for head in fix_header:
			sheet.write(row, col, head, bold)
			col+=1
		# sheet.merge_range(0, 0, 2, 2, "Merged Cells", bold)
		sheet.set_column(0, 1, 10)
		sheet.set_column(2, 2, 20)
		sheet.set_column(3, 3, 50)
		sheet.set_column(4, 5, 30)
	
		date_from = data['date_from']
		date_to = data['date_to']
		account = data['account']
		cashier_ids = self.env['esmis.cashier'].search([('invoice_date','>=', date_from),('invoice_date','<=', date_to),('status','=', 'paid')])

		row_data = 10
		col_data = 0
		num_count = 1
		account_data = []

		total_collections = 0
		for rec in cashier_ids:
			for recs in rec.cashier_line_ids:
				if account == recs.fee_id.id:
					account_data.append(num_count)
					account_data.append(rec.or_no)
					account_data.append(rec.invoice_date)
					account_data.append(rec.payer_name)
					account_data.append(recs.fee_id.account_id)
					account_data.append("{:.2f}".format(recs.amount_paid))
					total_collections+=recs.amount_paid

					for recs in account_data:
						sheet.write(row_data, col_data, str(recs), bold)
						col_data+=1

					col_data=0
					num_count+=1
					row_data+=1
					account_data = []
		sheet.write(row_data, 4, 'TOTAL COLLECTIONS', bold_center)
		sheet.write(row_data, 5, "{:.2f}".format(total_collections), bold_center)

