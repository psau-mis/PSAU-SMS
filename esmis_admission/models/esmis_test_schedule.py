from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError, AccessError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime, timedelta
import pytz


class eSMISTestSchedule(models.Model):
	_name = 'esmis.admission.test.schedule'
	_description = "Schedule Test Admission"

	name = fields.Char(string="Name", default="/", required=True, help="Leave/set the value to '/' and the system will generate a name on the first time it is saved")
	exam_format = fields.Selection([('online', 'Online'), ('pen_and_paper', 'Pen & Paper')], string="Exam Format", default="online", required=True)
	schedule = fields.Selection([('fall', 'Fall'), ('spring', 'Spring')], string="Schedule")
	program_type = fields.Selection([('undergraduate', 'Undergraduate'), ('graduate', 'Graduate'), ('masteral', 'Masteral'), ('doctorate', 'Doctorate')], string="Program Type", required=True)
	state = fields.Selection([('draft', 'Draft'), ('running', 'Running'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], string="State", default="draft")
	test_date = fields.Datetime(string="Date", required=True)
	venue = fields.Char(string="Venue", required=True)
	user_id = fields.Many2one('res.users', string="Responsible")
	assessor_user_id = fields.Many2one('res.users', domain="[('partner_id.is_student', '=', False)]", string="Proctor")
	assessor_name = fields.Char(string="Proctor", required=True)
	assessor_e_signature = fields.Image(string="Proctor E-Signature")
	approver_user_id = fields.Many2one('res.users', domain="[('partner_id.is_student', '=', False)]", string="Approver")
	# employee_id = fields.Many2one('hr.employee', string="Assessor", required=True)
	test_type_id = fields.Many2one('esmis.admission.test.type', string="Interpretation", domain="[('active', '=', True)]", required=True, store=True)
	esmis_admission_ids = fields.Many2many('esmis.admission', string='Admissions Table', domain="[('state', '=', 'received'), ('test_scheduled', '=', False)]", required=True)
	no_show_admission_ids = fields.Many2many('esmis.admission', 'esmis_admission_no_show', string='No Show Admissions')
	auto_email_deactive = fields.Boolean(string="Auto Email", compute="_compute_auto_email")
	footer_text = fields.Char(string="Report Footer", help="This will be displayed on reports footer")

	def test_schedule_datetime_formatted(self, test_datetime):
		test_date = datetime.strptime(test_datetime, DATETIME_FORMAT)
		localtimezone = pytz.timezone('Asia/Manila')
		iso_dt = test_date.astimezone(localtimezone).isoformat(' ', timespec='minutes').replace('+08:00','')
		date_iso = datetime.strptime(iso_dt.split(' ')[0], DATE_FORMAT).strftime('%B %d, %Y')
		time_iso = datetime.strptime(iso_dt.split(' ')[1], '%H:%M').strftime('%I:%M %p')
		return str(date_iso)

	@api.model
	def get_footer_text(self):
		footer = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.guidance_report_footer')
		if footer:
			return footer
		return ""

	@api.model
	def create(self, vals):
		user_id = vals.get('user_id')
		if vals['name'] == '/' or vals['name'] == False:
			user = self.env['res.users'].browse(user_id)
			vals['name'] = "Admission Test(%s %s)" % (user.name, self.test_schedule_datetime_formatted(vals.get('test_date')))
		res = super(eSMISTestSchedule, self).create(vals)
		return res

	@api.model
	def get_signatories(self):
		signatories_id = self.env['ir.config_parameter'].sudo().get_param('esmis_admission.test_sched_signatory_id')
		if signatories_id:
			signatories_id = self.env['esmis.signatories'].search([('id', '=', int(signatories_id))])
		return signatories_id

	def unlink(self):
		for rec in self:
			if rec.state in ('completed', 'cancelled'):
				raise UserError(_('Completed or Cancelled form cannot be deleted'))
			for record in rec.esmis_admission_ids:
				record.write({
					'test_scheduled': False,
					'test_type_id': False,
					'raw_score': 0,
					})
		return super().unlink()

	def write(self, vals):
		admission_ids = vals.get('esmis_admission_ids', False)
		if admission_ids:
			try:
				if admission_ids[0][2]:
					unlinked_admission_ids = self.esmis_admission_ids.filtered(lambda  line: line.id not in admission_ids[0][2])
					for admission in unlinked_admission_ids:
						admission.write({
							'test_scheduled': False
							})
			except Exception as e:
				pass
			
		return super(eSMISTestSchedule, self).write(vals)

	@api.constrains('esmis_admission_ids')
	def _check_esmis_admission_ids_lines(self):
		for record in self:
			if len(record.esmis_admission_ids) > 70:
				esmis_admission_ids = record.esmis_admission_ids.ids
				excess_esmis_admission_ids = esmis_admission_ids[70:]
				for exc in excess_esmis_admission_ids:
					self.env['esmis.admission'].browse(exc).write({'test_scheduled': False})
				record.esmis_admission_ids = [(3,excess) for excess in excess_esmis_admission_ids]
			# 	raise ValidationError('You cannot select more than 70 line in the Admission field.')
			# if len(record.esmis_admission_ids) == 0:
			# 	raise ValidationError('Please Select Admission.')
			for admission in record.esmis_admission_ids:
				admission.write({
					'test_scheduled': True
					})

			if record.state == 'completed' and not record.env.user.has_group('esmis_admission.group_esmis_admission_guidance_officer'):
				raise AccessError(_('You do not have the access to update this field/s.'))

	@api.onchange('esmis_admission_ids', 'test_type_id')
	def _admission_ids_change(self):
		if len(self.esmis_admission_ids) and self.test_type_id:
			for rec in self.esmis_admission_ids:
				rec.update({
					'test_type_id': self.test_type_id.id
					})

	@api.onchange('test_date')
	def _check_test_date(self):
		if self.test_date != False:
			if datetime.today() > self.test_date :
				self.test_date = datetime.today() + timedelta(days=1)
				return {
					'warning': {'title': _('Test Scheduling'), 'message': _("Past dates are not allowed..."),},
				}

	def _compute_auto_email(self):
		for rec in self:
			rec.auto_email_deactive = rec.env['ir.config_parameter'].sudo().get_param('esmis_admission.disable_sending_of_email')

	def notify_test_sched(self):
		message = "Action Successfully executed..."
		if self.auto_email_deactive:
			message = "Unable to send email, please enable email sender or send the email manually."
		else:
			for rec in self.esmis_admission_ids:
				rec.with_context({'venue': self.venue}).notify_test_sched()
		return {
			"type": "ir.actions.client",
			"tag": "display_notification",
			"params": {
				"title": _("Test Scheduling"),
				"message": message,
				"sticky": False,
				"type": "info",
				"next": {
					"type": "ir.actions.act_window_close",
				},
			},
		}

	def set_as_running(self):
		if not len(self.esmis_admission_ids):
			return {
				"type": "ir.actions.client",
				"tag": "display_notification",
				"params": {
					"title": _("Test Scheduling"),
					"message": 'Please select admission.',
					"sticky": True,
					"type": "info",
					"next": {
						"type": "ir.actions.act_window_close",
					},
				},
			}
		for rec in self.esmis_admission_ids:
			rec.write({
				'test_date': self.test_date,
				'test_venue': self.venue
				})
		self.write({
			'state': 'running'
			})

	def set_as_complete(self):
		for rec in self.esmis_admission_ids:
			if rec.is_no_show:
				rec.write({'test_scheduled': False, 'is_no_show': False})
				self.write({'esmis_admission_ids': [(3, rec.id)], 'no_show_admission_ids': [(4, rec.id)]})
				continue
			rec.write({
				'test_date': self.test_date,
				'test_type_id': self.test_type_id.id,
				})
			rec.set_for_evaluation()
		self.write({
			'state': 'completed'
			})

	def set_as_cancelled(self):
		for rec in self.esmis_admission_ids:
			rec.write({
				'test_date': False,
				'test_venue': False,
				'test_scheduled': False,
				})
		self.write({
			'state': 'cancelled'
			})