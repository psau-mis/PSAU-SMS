from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class ReportOfCollectionWiz(models.TransientModel):
	_name = 'esmis.report.of.collection.wiz'


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
			return self.env.ref('esmis_reports.report_of_collection_xlsx').report_action(self, data=data)
		
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
			return self.env.ref('esmis_reports.report_of_collection_pdf').report_action(self, data=data)
		
class ReportOfCollectionPdf(models.AbstractModel):
	_name = 'report.esmis_reports.detailed_report_of_collection_pdf'

	def _get_report_values(self, docids, data=None):

		docs = self.env['esmis.cashier'].search([
			('invoice_date','>=', data['date_from']),
			('invoice_date','<=', data['date_to']),
			('status','=', 'paid'),
		])

		totals = []
		totality = 0
		for doc in docs:
			total_amount = sum(line.amount_paid for line in doc.cashier_line_ids)
			totals.append(total_amount)
			totality += total_amount

		return {
			'doc_ids': docids,
			'doc_model': 'esmis.cashier',
			'docs': docs,
			'data': data,
			'totals': totality,
		}
