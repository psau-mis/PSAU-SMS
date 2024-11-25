from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CollectionReportsBySubAccountWiz(models.TransientModel):
	_name = 'esmis.collection.by.subaccount.wiz'


	date_from = fields.Date(string="Date From", required=True)
	date_to = fields.Date(string="Date To", required=True)

	def print_xlsx(self):
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise ValidationError("Invalid input of date")

			cashier_ids = self.env['esmis.cashier'].search_read([('invoice_date','<=', self.date_from),('invoice_date','>=', self.date_to)])
			data = {
				'cashier': cashier_ids,
				'date_from': self.date_from,
				'date_to': self.date_to,
				}
			return self.env.ref('esmis_reports.report_collection_by_subaccount_xlsx').report_action(self, data=data)

	def print_pdf(self):
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise ValidationError("Invalid input of date")

			cashier_ids = self.env['esmis.cashier'].search_read([('invoice_date','>=', self.date_from),('invoice_date','<=', self.date_to)])
			data = {
				'cashier': cashier_ids,
				'date_from': self.date_from,
				'date_to': self.date_to,
				}
			return self.env.ref('esmis_reports.report_collection_by_subaccount_pdf').report_action(self, data=data)
class CollectionReportBySubAccountPdf(models.AbstractModel):
	_name = 'report.esmis_reports.report_by_subaccount_pdf'

	def _get_report_values(self, docids, data=None):

		docs = self.env['esmis.cashier'].search([
			('invoice_date','>=', data['date_from']),
			('invoice_date','<=', data['date_to']),
		])
		
		fund_codes = self.env['esmis.fees.fund'].search([])
		chart_of_accounts = self.env['esmis.coa'].search([
			('fund_group', 'in', fund_codes.ids),
		])

		# Initialize data structure for the total amounts
		fund_code_totals = []
		TOTAL_COLLECTIONS = 0

		for fund_code in fund_codes:
			related_coas = chart_of_accounts.filtered(lambda coa: coa.fund_group == fund_code)

			coa_totals = []
			fund_total = 0
			for coa in related_coas:
				total_amount_paid = sum(
					line.amount_paid for doc in docs for line in doc.cashier_line_ids if line.fee_id == coa
				)
				coa_totals.append({
					'coa_name': coa.name,
					'account_num': coa.account_id,
					'total_amount_paid': total_amount_paid,
				})
				fund_total += total_amount_paid

			fund_code_totals.append({
				'fund_code_name': fund_code.name,
				'fund_code_description': fund_code.description,
				'coa_totals': coa_totals,
				'fund_total': fund_total,
			})

			TOTAL_COLLECTIONS += fund_total

		# FOR LOGGING/PRINTING PURPOSES
		# for fund_code in fund_codes:
		# 	print(f"~~~~~~Fund Group: {fund_code.name} | Description: {fund_code.description}~~~~~~")  # Print the Fund Group name
			
		# 	related_coas = chart_of_accounts.filtered(lambda coa: coa.fund_group == fund_code)

		# 	total_for_fund_code = 0
			
		# 	for coa in related_coas:
		# 		total_amount_paid = sum(
		# 			line.amount_paid for doc in docs for line in doc.cashier_line_ids if line.fee_id == coa
		# 		)
				
		# 		print(f"→→ {coa.name} | Total: {total_amount_paid}")
		# 		total_for_fund_code += total_amount_paid

		# 	print(f"~~~~~~TOTAL {fund_code.description.upper()}: {total_for_fund_code}~~~~~~")

		last_or_no = docs and docs[0].or_no or None
		first_or_no = docs and docs[-1].or_no or None

		return {
			'doc_ids': docids,
			'doc_model': 'esmis.cashier',
			'docs': docs,
			'data': data,
			'first_or_no': first_or_no,
            'last_or_no': last_or_no,
			'fund_code_totals': fund_code_totals,
			'total_collections': TOTAL_COLLECTIONS,
		}