odoo.define('esmis_website_admission.admission_website_personal_info',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');

	publicWidget.registry.AdmissionWebsiteAddress = publicWidget.Widget.extend({
		selector: "#input_personal_info",
		events: {
			'change #state_id': '_changeStates',
			'change #city_id': '_changeCities',
			'change #mobile': '_changeMobile',
			'change #phone': '_changePhone',
			'change #email_address': '_changeEmailAddress',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			return this._super(...arguments);
		},
		_changeStates: function(ev) {
			var states = $(ev.currentTarget);
			var self = this;
			this._rpc({
				route: "/esmis/states_info/" + states.val(),
				params: {},
			}).then(function (data) {
				// populate cities and display
				var selectCities = $("select[name='city_id']");
				if (data.cities.length) {
					selectCities.html('');
					_.each(data.cities, function (x) {
						var opt = $('<option>').text(x[1])
							.attr('value', x[0])
						selectCities.append(opt);
					});
					selectCities.trigger('change');
				}
			});
		},
		_changeCities: function(ev) {
			var city = $(ev.currentTarget);
			var self = this;
			this._rpc({
				route: "/esmis/cities_info/" + city.val(),
				params: {},
			}).then(function (data) {
				var selectBarangay = $("select[name='barangay_id']");
				if (data.barangay.length) {
					selectBarangay.html('');
					_.each(data.barangay, function (x) {
						var opt = $('<option>').text(x[1])
							.attr('value', x[0])
						selectBarangay.append(opt);
					});
				}
			});
		},
		_changeMobile: function(ev) {
			var mobile = $(ev.currentTarget);
			if (mobile.val().length == 10) {
				mobile.removeClass('is-invalid');
			} else {
				mobile.addClass('is-invalid');
			}
			
		},
		_changePhone: function(ev) {
			var phone = $(ev.currentTarget);
			var phone_regex = /^\(?([0-9]{2})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
			if (phone.val().length) {
				if (!phone_regex.test(phone.val())) {
					phone.addClass('is-invalid');
				} else {
					phone.removeClass('is-invalid');
				}
			} else {
				phone.removeClass('is-invalid');
			}
		},
		_changeEmailAddress: function(ev) {
			var email_address = $(ev.currentTarget);
			var admission_type = $('#admission_type').val();
			const exclude_type = ['continuing', 'graduate', 'graduate2'];
			if (!exclude_type.includes(admission_type)){ 
				this._rpc({
					route: "/esmis/check/email",
					params: {'email_address': email_address.val()},
				}).then(function (data) {
					if (data === 'exists') {
						email_address.addClass('is-invalid');
						$('#email_exist_message').removeClass('d-none');
					} else {
						email_address.removeClass('is-invalid');
						$('#email_exist_message').addClass('d-none');
					}
				});
			}
		},
	});

	publicWidget.registry.AdmissionApplicantName = publicWidget.Widget.extend({
		selector: "#input_applicant_name",
		events: {
			'change #last_name': '_changeLastName',
			'change #first_name': '_changeFirstName',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			this.has_first_name = false;
			this.has_last_name = false;
			return this._super(...arguments);
		},
		_changeFirstName: function(ev) {
			var first_name = this.$(ev.currentTarget).val();
			if (first_name) {
				this.has_first_name = true;
			}
			if (this.has_first_name && this.has_last_name) {
				if ($('#o_web_sign_name_input_1').length) {
					var name_combine = this.$('#first_name').val() + ' ' + this.$('#last_name').val();
					$('#o_web_sign_name_input_1').val(name_combine);
					$('#o_web_sign_name_input_1').trigger('input');
				}
			}
		},
		_changeLastName: function(ev) {
			var last_name = this.$(ev.currentTarget).val();
			if (last_name) {
				this.has_last_name = true;
			}
			if (this.has_first_name && this.has_last_name) {
				if ($('#o_web_sign_name_input_1').length) {
					var name_combine = this.$('#first_name').val() + ' ' + this.$('#last_name').val();
					$('#o_web_sign_name_input_1').val(name_combine);
					$('#o_web_sign_name_input_1').trigger('input');
				}
			}
		},
	});
});