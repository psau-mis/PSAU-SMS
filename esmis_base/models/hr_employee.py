import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import Command, api, fields, models, _

from odoo.exceptions import ValidationError,Warning

_logger = logging.getLogger(__name__)

   
class InheritEmployee(models.Model):
	_inherit = "hr.employee"



	@api.model
	def default_password(self):
		default_pass =  self.env['res.config.settings'].sudo().search([], limit=1)
		return default_pass.password_default


	@api.model
	def create(self, vals):
		email_exists = vals.get('email') and self.env['hr.employee'].sudo().search_count([('email', '=', vals['work_email'])]) > 0
		default_pass = self.env.user.company_id.password_default or "Psau!2024"
		if email_exists:
			raise UserError("Email address is already associated with another employee.")
		# return super(CustomModel, self).create(vals)

		employee = super(InheritEmployee, self).create(vals)

		if vals.get('work_email'):
			
			user = self._create_portal_user(employee, vals.get('work_email'), default_pass)
			# raise ValidationError("here")
			if user:
				# employee.user_id = user.id
				# employee.work_email = user.login
				employee.write({'user_id': user.id})
				employee.write({'work_email': user.login})
			else:
				raise ValidationError("Failed to create the user. Please check the email address.")
			# raise ValidationError(employee.name)
			
			
		else:
			raise ValidationError("Failed to create the user. Please check the email address.")
				
		return employee
		

	def _create_portal_user(self, employee, work_email, defaut_pass):
		# x_group_teacher_user = self.env.ref('base.group_user')
		is_teacher = self.env.ref('esmis_base.group_esmis_teacher') or False
		# raise ValidationError(employee.name)
		vals_user = {
			'create_employee_id': employee.id,
			"name": employee.name,
			# "email": work_email,
			"login": work_email,
			"password":defaut_pass,
			# 'partner_id': employee.id,
			'groups_id': [(6, 0, [is_teacher.id])],

			
		}
	   
		return self.env['res.users'].sudo().create(vals_user)


        # self.ensure_one()
        # if self.user_id:
        #     raise ValidationError(_("This employee already has an user."))
        # return {
        #     'name': _('Create User'),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'res.users',
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('hr.view_users_simple_form').id,
        #     'target': 'new',
        #     'context': {
        #         'default_create_employee_id': self.id,
        #         'default_name': self.name,
        #         'default_phone': self.work_phone,
        #         'default_mobile': self.mobile_phone,
        #         'default_login': self.work_email,
        #     }
        # }


	# def write(self, vals):
	# 	if 'work_email' in vals:
	# 		email_exists = self.env['hr.employee'].search_count([('work_email', '=', vals['work_email']), ('id', '!=', self.id)]) > 0
	# 		if email_exists:
	# 			raise UserError("Email address is already associated with another parent record.")

	# 		for rec in self:
	# 			user = self.env['res.users'].sudo().search([('work_email', '=', rec.work_email)], limit=1)
	# 			if user:
	# 				user.write({'work_email': vals['work_email']})

	# 	res = super(InheritEmployee, self).write(vals)
	# 	if 'work_email' in vals or 'name' in vals:
	# 		for rec in self:
	# 			user = self.env['res.users'].sudo().search([('work_email', '=', rec.work_email)], limit=1)
	# 			if user:
	# 				user.write({
	# 					'name': rec.name,
	# 					'login': rec.work_email,
	# 					# 'password': "123456"
						
	# 				})
	# 	return res
