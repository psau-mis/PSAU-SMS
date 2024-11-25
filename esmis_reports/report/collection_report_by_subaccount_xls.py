from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError
import base64
import io
from odoo.modules.module import get_module_resource


class CollectionBySubAccountXlsx(models.AbstractModel):
	_name = 'report.esmis_reports.collection_by_subaccount_xls'
	_inherit = 'report.report_xlsx.abstract'



	def generate_xlsx_report(self, workbook, data, partners):
		print("asd", data['cashier'])
		sheet = workbook.add_worksheet('COLLECTION REPORT BY SUB-ACCOUNT')
		bold = workbook.add_format({'bold':True})
		bold_right = workbook.add_format({'align': 'right','bold':True})
		header_format = workbook.add_format({'align': 'center','bold':True,'border': 1})
		republic_format = workbook.add_format({'align': 'center','bold':True})
		psau_format = workbook.add_format({'align': 'left','bold':True, 'font':'monotype old english text', 'size':17})
		title_format = workbook.add_format({'align': 'left', 'size':15})
		date_format = workbook.add_format({'align': 'left', 'size':15})
		logo_format  = workbook.add_format({'align': 'center'})
		data_format = workbook.add_format({'align': 'center','bold':True})
		payer_format = workbook.add_format({'align': 'left','bold':True,'border': 1})
		grand_total_format = workbook.add_format({'align': 'right','bold':True,'border': 1})
		fund_code_format = workbook.add_format({'align': 'center','bold':True, 'size':13})
		parent_code_format = workbook.add_format({'align': 'center','bold':True, 'size':11})
		data_coa_format = workbook.add_format({'align': 'left','bold':False, 'size':11})
		total_per_coa_format = workbook.add_format({'align': 'left','bold':True, 'size':11})


		# sheet.insert_image('A1', 'logo.jpg')
		sheet.set_column(0, 1, 11)
		sheet.insert_image('A2', get_module_resource('esmis_reports', 'static/img', 'logo.jpg'), {'x_scale': 0.5, 'y_scale': 0.4})	
		sheet.merge_range('B2:L2', "PAMPANGA STATE AGRICULTURAL UNIVERSITY", psau_format)
		sheet.merge_range('B3:L3', "COLLECTIONS REPORTS BY SUB-ACCOUNT", title_format)
		sheet.merge_range('B4:L4', "DATE RANGE:" + " " + data['date_from'] + " " + data['date_to'], date_format)
		sheet.merge_range('B5:L5', "O.R COVERED:", date_format)


		date_from = data['date_from']
		date_to = data['date_to']
		fund_code_ids = self.env['esmis.fees.fund'].search([])
		cashier_ids = self.env['esmis.cashier'].search([('invoice_date','>=', date_from),('invoice_date','<=', date_to),('status','=', 'paid')])
		coa_ids = self.env['esmis.coa'].search([])
	


	
		row_data = 7
		col_data = 1
		fund_list = []
		grand_total = 0
		for rec in fund_code_ids:
			fund_list.append(rec.name)
			fund_list.append(rec.description)
			foo = True
			for recs in fund_list:
				if foo == True:
					sheet.write(row_data, col_data, rec.name, fund_code_format)
					foo = False
				else:
					sheet.merge_range(f'C{row_data+1}:F{row_data+1}', rec.description, fund_code_format)
					foo = True
			row_data+=1
			fund_list = []
			parent_code_list = []
			parent_code_list_id = []


			total_per_fund = 0
			for coa_record in coa_ids:
				if coa_record.fund_group.id == rec.id:
					if coa_record.parent_code:
						if coa_record.parent_code.id not in parent_code_list:
							parent_code_list.append(coa_record.parent_code.id)

							# parent_code_list.append(coa_record.parent_code.account_id)
							# parent_code_list.append(coa_record.parent_code.name)
							
							sheet.merge_range(f'C{row_data+1}:D{row_data+1}', coa_record.parent_code.account_id, parent_code_format)
						
							sheet.merge_range(f'E{row_data+1}:F{row_data+1}', coa_record.parent_code.name, parent_code_format)
							row_data+=1
							# row_data_1 = row_data
							cashier_lines = {}
							total_per_sub_coa = 0
							for cashier_rec in cashier_ids:
								for line in cashier_rec.cashier_line_ids:
									if coa_record.parent_code.id == line.fee_id.parent_code.id:
										coa_id = line.fee_id.id
										if coa_id not in cashier_lines:
											cashier_lines[coa_id] = {
												'coa_code': line.fee_id.account_id,
												'coa_name': line.fee_id.name,
												'coa_amount': 0
												
											}

										cashier_lines[coa_id]['coa_amount'] += line.amount_paid
										total_per_sub_coa += line.amount_paid
										total_per_fund += line.amount_paid
										grand_total += line.amount_paid
							for coa_id, coa_data in cashier_lines.items():

								sheet.write(row_data, 3, coa_data['coa_code'], data_coa_format)
								sheet.write(row_data, 5, coa_data['coa_name'], data_coa_format)
								sheet.write(row_data, 9, "{:.2f}".format(coa_data['coa_amount']), data_coa_format)
								row_data+=1

							sheet.write(row_data, 9, "{:.2f}".format(total_per_sub_coa), total_per_coa_format)
							row_data+=1
			if rec.description:
				sheet.write(row_data, 7, 'Total '+rec.description, data_format)
				sheet.write(row_data, 9, "{:.2f}".format(total_per_fund), total_per_coa_format)
				row_data+=1

							
			# row_data+=1
			parent_code_list = []
		sheet.write(row_data, 7, 'TOTAL COLLECTIONS', data_format)
		sheet.write(row_data, 9, "{:.2f}".format(grand_total), total_per_coa_format)
		# row_data+=1

	