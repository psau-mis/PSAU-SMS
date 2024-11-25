from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import date,datetime,timedelta


class AdmissionHealthServicesLogbookWizard(models.TransientModel):
	_name = 'esmis.health.services.logbook.wiz'

	log_id = fields.Many2one('esmis.health.services.logbook')
	name = fields.Char(string="Name")
	log_time = fields.Datetime(string="Time", default=lambda self: fields.datetime.now()) 
	client_type = fields.Selection([('Employee', 'Employee'),('Student', 'Student'),('Outsider', 'Outsider')], 'Client Type', default="Student")
	student_id = fields.Many2one('res.partner', string="Student", domain="[('is_student', '=', True)]")
	employee_id = fields.Many2one('res.partner', string="Employee", domain="[('is_employee', '=', True)]")
	student_type = fields.Selection([('CAS', 'CAS'),
		('CAST', 'CAST'),
		('CHEFS', 'CHEFS'),
		('COECS', 'COECS'),
		('COED', 'COED'),
		('CVM', 'CVM'),
		('GRADE 11', 'GRADE 11'),
		('GRADE 12', 'GRADE 12'),
		('GRADUATE', 'GRADUATE')], string="Student Type", default="CAS")
	employee_type = fields.Selection([('Faculty', 'Faculty'),('Admin', 'Admin'),], string="Employee Type", default="Faculty")
	first_name = fields.Char(string="First Name")
	last_name = fields.Char(string="last Name")
	purpose = fields.Selection([('Medical', 'Mecical'),('Dental', 'Dental')], 'Purpose', default="Medical")
	dx = fields.Text(string="DX")

	@api.onchange('employee_id', 'student_id', 'client_type', 'first_name', 'last_name')
	def get_name(self):
		if not self.last_name:
			self.last_name = ""
		if not self.first_name:
			self.first_name = ""
		if self.client_type == "Employee":
			self.name = self.employee_id.full_name
			self.student_id = False
			self.student_type = False
		elif self.client_type == "Student":
			self.name = self.student_id.full_name
			self.employee_id = False
		else:
			self.name = str(self.last_name) +", "+ str(self.first_name)
			self.employee_id = False
			self.student_id = False

	def create_record(self):

		return {
			"name": "Create Record",
			"view_mode": "form",
			"res_model": "esmis.health.services.logbook.wiz",
			"view_id": self.env.ref(
				"esmis_medical.esmis_health_services_logbook_wizard_form_view"
			).id,
			"type": "ir.actions.act_window",
			"target": "new",
			"context": self.env.context,
		}
