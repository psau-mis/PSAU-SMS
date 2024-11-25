from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io
from odoo.modules.module import get_module_resource


class CollectionByPayerXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.collection_by_payer_xls'
	_inherit = 'report.report_xlsx.abstract'



	def generate_xlsx_report(self, workbook, data, partners):
		print("asd", data['cashier'])
		sheet = workbook.add_worksheet('Collection Reports by Payer')
		bold = workbook.add_format({'bold':True})
		republic_format = workbook.add_format({'align': 'center','bold':True})
		psau_format = workbook.add_format({'align': 'center','bold':True, 'font':'monotype old english text', 'size':15})
		title_format = workbook.add_format({'align': 'center', 'size':13})
		row = 9
		col = 0

		sheet.insert_image('C2', get_module_resource('esmis_reports', 'static/img', 'logo.jpg'), {'x_scale': 0.6, 'y_scale': 0.6})
		sheet.merge_range(1, 0, 1, 6, "Republic of the Philippines", republic_format)
		sheet.merge_range(2, 0, 2, 6, "Pampanga State Agricultural University", psau_format)
		sheet.merge_range(3, 0, 3, 6, "PAC, Magalang, Pampanga", republic_format)

		sheet.merge_range(6, 0, 6, 7, "COLLECTION REPORT BY PAYER", bold)
		sheet.merge_range(7, 0, 7, 7, "DATE RANGE:" + " " + data['date_from'] + " " + data['date_to'], bold)
		fix_header = ['#', 'OR No', 'DATE', 'STUDENT NO', 'PAYOR NAME', 'PROGRAM', 'LEVEL', 'AMOUNT']
		for head in fix_header:
			sheet.write(row, col, head, bold)
			col+=1
		# sheet.merge_range(0, 0, 2, 2, "Merged Cells", bold)
		sheet.set_column(0, 1, 10)
		sheet.set_column(2, 3, 20)
		sheet.set_column(4, 4, 35)
		sheet.set_column(5, 5, 50)
		sheet.set_column(6, 6, 10)
		sheet.set_column(7, 7, 20)



		date_from = data['date_from']
		date_to = data['date_to']
		# raise ValidationError(date_from)

		row_data = 10
		col_data = 0
		num_count = 1
		cashier_data = []
		mode_of_payment = ['bank', 'cash', 'check']
		cashier_ids = self.env['esmis.cashier'].search([('invoice_date','>=', date_from),('invoice_date','<=', date_to),('status','in', ('paid', 'voided'))])
		# raise ValidationError(str(cashier_ids))
		grand_total = 0
		for modes in mode_of_payment:
			if modes == 'bank':
				sheet.merge_range(row_data, col_data, row_data, 7, 'CARD PAYMENT', bold)
			elif modes == 'cash':
				sheet.merge_range(row_data, col_data, row_data, 7, 'CASH PAYMENT', bold)
			else:
				sheet.merge_range(row_data, col_data, row_data, 7, 'CHECK PAYMENT', bold)
			row_data+=1

			# sheet.write(row_data, col_data, str(recs), bold)
			total_amount = 0.00
			for rec in cashier_ids:
				mode_of_payment_id = self.env['esmis.mode.of.payment'].search([('cashier_id','=',rec.id),('mode_of_payment','=', modes)])
				if mode_of_payment_id:
					cashier_data.append(num_count)
					cashier_data.append(rec.or_no)
					cashier_data.append(rec.invoice_date)
					if rec.student_id.student_no_grad:
						cashier_data.append(rec.student_id.student_no_grad)
					else:
						cashier_data.append(rec.student_id.student_no_undg)
					if rec.status == 'paid':
						cashier_data.append(rec.payer_name)
						cashier_data.append(rec.enrollment_id.course_id.name)
						cashier_data.append(rec.enrollment_id.year_level)
						cashier_data.append("{:.2f}".format(rec.total_amount_paid))
						total_amount += rec.total_amount_paid
					else:
						cashier_data.append("*** Voided Transaction ***")
						cashier_data.append("")
						cashier_data.append("")
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
			if modes == 'bank':
				sheet.merge_range(row_data, 5, row_data, 6, 'CARD TOTAL', bold)
				sheet.write(row_data, 7, "{:.2f}".format(total_amount), bold)
			elif modes == 'cash':
				sheet.merge_range(row_data, 5, row_data, 6, 'CASH TOTAL', bold)
				sheet.write(row_data, 7, "{:.2f}".format(total_amount), bold)
			else:
				sheet.merge_range(row_data, 5, row_data, 6, 'CHECK TOTAL', bold)
				sheet.write(row_data, 7, "{:.2f}".format(total_amount), bold)
			row_data+=1
		sheet.merge_range(row_data, 5, row_data, 6, 'GRAND TOTAL', bold)
		sheet.write(row_data, 7, "{:.2f}".format(grand_total), bold)
