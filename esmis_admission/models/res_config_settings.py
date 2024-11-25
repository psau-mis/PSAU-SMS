# -*- coding:utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
	_inherit = "res.config.settings"

	disable_sending_of_email = fields.Boolean(string="Disable auto sending of email", config_parameter="esmis_admission.disable_sending_of_email")
	disable_admission = fields.Boolean(string="Disable Admission", config_parameter="esmis_admission.disable_admission")
	requirements_submission_due = fields.Integer(string="Submission of Requirements", config_parameter="esmis_admission.requirements_submission_due")
	admission_signatories_id = fields.Many2one('esmis.iso.printouts', string="Admission Signatories", config_parameter="esmis_admission.admission_signatories_id")
	admission_signatory_id = fields.Many2one('esmis.signatories', string="Admission Signatory", config_parameter="esmis_admission.admission_signatory_id")
	test_sched_signatories_id = fields.Many2one('esmis.iso.printouts', string="Test Signatories", config_parameter="esmis_admission.test_sched_signatories_id")
	test_sched_signatory_id = fields.Many2one('esmis.signatories', string="Test Signatory", config_parameter="esmis_admission.test_sched_signatory_id")
	university_registrar_id = fields.Many2one('esmis.signatories', string="University Registrar Signatory", config_parameter="esmis_admission.university_registrar_id")
	sms_app_key = fields.Char(string="SMS App Key", config_parameter="esmis_admission.sms_app_key")
	sms_app_secret = fields.Char(string="SMS App Secret", config_parameter="esmis_admission.sms_app_secret")
	sms_shortcode_mask = fields.Char(string="SMS Shortcode Mask", config_parameter="esmis_admission.sms_shortcode_mask")
	require_first_choice = fields.Boolean(string="Require 1st Course Choice", default=True, config_parameter="esmis_admission.require_first_choice")
	require_second_choice = fields.Boolean(string="Require 2nd Course Choice", default=True, config_parameter="esmis_admission.require_second_choice")
	require_third_choice = fields.Boolean(string="Require 3rd Course Choice", config_parameter="esmis_admission.require_third_choice")
	admission_report_footer = fields.Char(string="Admission Report Footer", config_parameter="esmis_admission.admission_report_footer")
	guidance_report_footer = fields.Char(string="Guidance Report Footer", config_parameter="esmis_admission.guidance_report_footer")
