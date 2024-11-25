from odoo import _, api, fields, models
from odoo.exceptions import AccessError, ValidationError


class CollectionReportsByFundWiz(models.TransientModel):
	_name = 'esmis.collection.by.fund.wiz'


	date_from = fields.Date(string="Date From", required=True)
	date_to = fields.Date(string="Date To", required=True)


	def print_xlsx(self):
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise ValidationError("asd")

			cashier_ids = self.env['esmis.cashier'].search_read([('invoice_date','<=', self.date_from),('invoice_date','>=', self.date_to)])
			data = {
				'cashier': cashier_ids,
				'date_from': self.date_from,
				'date_to': self.date_to,
				}
			return self.env.ref('esmis_reports.report_collection_by_fund_xlsx').report_action(self, data=data)

	def print_pdf(self):
		if self.date_from and self.date_to:
			if self.date_from > self.date_to:
				raise ValidationError("Invalid Input date")

			cashier_ids = self.env['esmis.cashier'].search_read([('invoice_date','>=', self.date_from),('invoice_date','<=', self.date_to)])
			data = {
				'cashier': cashier_ids,
				'date_from': self.date_from,
				'date_to': self.date_to,
				}
			return self.env.ref('esmis_reports.report_collection_by_fund_pdf').report_action(self, data=data)


class CollectionReportByPayerPdf(models.AbstractModel):
	_name = 'report.esmis_reports.report_by_fund_pdf'

	def _get_report_values(self, docids, data=None):
		docs = self.env['esmis.cashier'].search([('invoice_date','>=', data['date_from']),('invoice_date','<=', data['date_to']),('status','=', 'paid')])
		esmis_fund = self.env['esmis.fees.fund'].search([])


		return {
			'doc_ids': docids,
			'doc_model': 'esmis.cashier',
			'docs': docs,
			'esmis_fund': esmis_fund,
			'data': data,
		}

