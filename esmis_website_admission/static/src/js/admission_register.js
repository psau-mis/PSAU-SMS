odoo.define('esmis_website_admission.admission_register',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');
	var signature_form = require('portal.signature_form');

	publicWidget.registry.AdmissionWebsiteRegister = publicWidget.Widget.extend({
		selector: "#admission_register_main",
		events: {
			'click #submit_main_admission': '_clickSubmit',
			'click #modal_button_sign_submit': '_clickShowSignSubmitModal',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			var self = this;
			var student_id = $('input[name="student_id"]');
			if (student_id.length) {
				const info_field = [
					'email_address', 'mobile', 'phone', 'street', 'street2',
					'state_id', 'city_id', 'barangay_id', 'gender',
					'birthdate', 'civil_status', 'place_of_birth',
					'citizenship', 'religion',
					'father_name', 'father_birthdate', 'father_educ_attain', 'father_occupation', 'father_company',
					'father_monthly_income', 'father_contact', 'mother_name', 'mother_birthdate',
					'mother_educ_attain', 'mother_occupation', 'mother_company',
					'mother_monthly_income', 'mother_contact', 'guardian_name', 'guardian_birthdate',
					'guardian_educ_attain', 'guardian_occupation', 'guardian_company',
					'guardian_monthly_income', 'guardian_contact',
					];
				this._rpc({
					route: "/esmis/student_info",
					params: {'student_id': student_id.val()},
				}).then(function (server_response) {
					info_field.forEach(function (item, index) {
						
						if (server_response[0].hasOwnProperty(item)) {
							var data_value = server_response[0][item] || "";
							if (typeof data_value === "object") {
								$('input[name="'+item+'"]').val(data_value[0]);
								$('select[name="'+item+'"]').val(data_value[0]);
							} else {
								$('input[name="'+item+'"]').val(data_value);
								$('select[name="'+item+'"]').val(data_value);
							}
						}
					});
					$('input[name="father_contact"]').val(server_response[0]['father_contact_no'] || "");
					$('input[name="mother_contact"]').val(server_response[0]['mother_contact_no'] || "");
					$('input[name="guardian_contact"]').val(server_response[0]['guardian_contact_no'] || "");
					$('input[name="email_address"]').val(server_response[0]['email'] || "");
					$('input[name="mobile"]').val(server_response[0]['mobile_number'] || "");
					$('input[name="phone"]').val(server_response[0]['phone_number'] || "");
					$('input[name="father_name"]').val(server_response[0]['father_full_name'] || "");
					$('input[name="mother_name"]').val(server_response[0]['mother_full_name'] || "");
					$('input[name="guardian_name"]').val(server_response[0]['guardian_full_name'] || "");
					$('select[name="gender"]').val(server_response[0]['gender'] ? server_response[0]['gender'].toLowerCase() : "");
					if ('civil_status' in server_response[0]) {
						if (server_response[0]['civil_status']) {
							$('select[name="civil_status"]').val(server_response[0]['civil_status'] ? server_response[0]['civil_status'].toLowerCase() : "");
						}
					}
					$('input[name="place_of_birth"]').val(server_response[0]['birthplace'] || "");
					$('input[name="citizenship"]').val(server_response[0]['nationality'] || "");
				});
			}
			$('form').on('submit', function (argument) {
				const invalid_input = $(argument.currentTarget).find('.is-invalid');
				
				if (invalid_input.length) {
					argument.preventDefault();
					invalid_input.each(function () {
						var position = $(this).offset().top - $(argument.currentTarget).offset().top + $(argument.currentTarget).scrollTop();
						$([document.documentElement, document.body]).animate({
							scrollTop: position
						}, 1000);
						return false;
					});
				}
			});
			return this._super(...arguments);
		},
		_clickSubmit: function (ev) {
			const fd = new FormData(ev.currentTarget.form);
			let size = 0

			for(let pair of fd.entries()) {
				if (pair[1] instanceof Blob)
					size += pair[1].size
				else
					size += pair[1].length
			}
		},
		_clickShowSignSubmitModal: async function (ev) {
			ev.preventDefault();
			var self = this;
			var $admission_submit_btn = $('#submit_main_admission');
			const required_input = $('form').find('input[required]');
			const required_select = $('form').find('select[required]');
			var has_unfilled_required = false;
			required_input.each(function () {
				if ($(this).attr('type') !== 'checkbox') {
					if(!($(this).val().length)) {
						has_unfilled_required = true;
						$admission_submit_btn.trigger('click');
					}
				} else {
					if (!$(this).is(':checked')) {
						has_unfilled_required = true;
						$admission_submit_btn.trigger('click');
					}
				}
			});
			required_select.each(function () {
				if(!($(this).val().length)) {
					has_unfilled_required = true;
					$admission_submit_btn.trigger('click');
				}
			})
			const last_name = $('form').find('input#last_name').val();
			const first_name = $('form').find('input#first_name').val();
			const middle_name = $('form').find('input#middle_name').val();
			const suffix = $('form').find('select#suffix').val();
			const birthdate = $('form').find('input#birthdate').val();
			const admission_type_1 = $('form').find('input#admission_type_1').val();
			await self._rpc({
				route: "/admission_check_exist",
				params: {'last_name': last_name,'first_name': first_name,'middle_name': middle_name,'suffix': suffix,'birthdate': birthdate,'admission_type_1':admission_type_1},
			}).then(function (server_response) {
				has_unfilled_required = true;
				if (server_response){
					$('#existing_admission').removeClass('d-none');
					has_unfilled_required = true;
				} else {
					$('#existing_admission').addClass('d-none');
				}
			});

			if (!has_unfilled_required) {
				$('#sign_and_submit_modal').modal('show');
			}
		},
	});
	signature_form.SignatureForm.include({
		_onClickSignSubmit: function (ev) {
			const rec = this._super(...arguments);
			var $admission_submit_btn = $('#submit_main_admission');
			if ($admission_submit_btn.length != 0) {
				$('#sign_and_submit_modal').modal('hide');
				try {
					return rec.then(function (data) {
						$admission_submit_btn.click();
					});
				} catch (e) {
					return rec;
				}
			}
			return rec;
		}
	});
	return {
		AdmissionWebsiteRegister: publicWidget.registry.AdmissionWebsiteRegister,
	}
});