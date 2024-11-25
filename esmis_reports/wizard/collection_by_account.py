import logging

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError

_logger = logging.getLogger(__name__)
try:
    from num2words import num2words
except ImportError:
    _logger.warning("The num2words python library is not installed, amount-to-text features won't be fully available.")
    num2words = None


class CollectionReportsByAccountWiz(models.TransientModel):
	_name = 'esmis.collection.by.account.wiz'


	date_from = fields.Date(string="Date From", required=True)
	date_to = fields.Date(string="Date To", required=True)
	coa_id = fields.Many2one('esmis.coa')

	def print_xlsx(self):
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise ValidationError("Invalid input of date")

			cashier_ids = self.env['esmis.cashier'].search_read([('invoice_date','<=', self.date_from),('invoice_date','>=', self.date_to)])
			data = {
				'cashier': cashier_ids,
				'account': self.coa_id.id,
				'date_from': self.date_from,
				'date_to': self.date_to,
				}
			return self.env.ref('esmis_reports.report_collection_by_account_xlsx').report_action(self, data=data)
	
	def print_pdf(self):
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise ValidationError("Invalid Input date")

			cashier_ids = self.env['esmis.cashier'].search_read([('invoice_date','>=', self.date_from),('invoice_date','<=', self.date_to)])
			data = {
				'cashier': cashier_ids,
				'account': self.coa_id.id,
				'date_from': self.date_from,
				'date_to': self.date_to,
				}
			return self.env.ref('esmis_reports.report_collection_by_account_pdf').report_action(self, data=data)

class CollectionReportByAccountPdf(models.AbstractModel):
	_name = 'report.esmis_reports.report_by_account_pdf'

	def _get_report_values(self, docids, data=None):
		# raise ValidationError(data['date_from'])
		account = self.env['esmis.coa'].search([('id','=', data['account'])])
		docs = self.env['esmis.cashier'].search([
			('invoice_date','>=', data['date_from']),
			('invoice_date','<=', data['date_to']),
			('status','=', 'paid'),
			('cashier_line_ids.fee_id.id','=', data['account']),
		], order='invoice_date ASC')

		total_collections = sum(
			line.amount_paid for doc in docs for line in doc.cashier_line_ids if line.fee_id.id == data['account']
		)
		text_amount = num2words(total_collections)
		# print("TOTAL AMOUNT: ", total_collections)
		return {
			'doc_ids': docids,
			'doc_model': 'esmis.cashier',
			'docs': docs,
			'data': data,
			'coa': account,
			'total_collections': total_collections,
			'text_amount': text_amount,
		}
