odoo.define('esmis_website_admission.admission_family_bg',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');

	publicWidget.registry.AdmissionFamilyBG = publicWidget.Widget.extend({
		selector: "#family_bg",
		events: {
			'change #guardian_contact': '_changeGuardianContact',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			var self = this;
			// $('#father_contact').focusout(function (ev) {
			// 	self.contacts_focusout(this);
			// });
			// $('#mother_contact').focusout(function (ev) {
			// 	self.contacts_focusout(this);
			// });
			// $('#guardian_contact').focusout(function (ev) {
			// 	self.contacts_focusout(this);
			// });
			return this._super(...arguments);
		},
		contacts_focusout: function(ev) {
			if ($(ev).val().length && !$(ev).hasClass('is-invalid')) {
				$(ev).val("+63" + $(ev).val().slice(-10))
			}
		},
		_changeGuardianContact: function(ev) {
			var mobile = $(ev.currentTarget);
			var mobileValue = mobile.val();
			var regex = /^(09\d{9}|9\d{9})$/; // Provided mobile regex pattern
			// ACCEPTED Values +639XXXXXXXXX, 09XXXXXXXXX, 9XXXXXXXXX

			if (!regex.test(mobileValue)) {
				mobile.addClass("is-invalid");
			} else {
				mobile.removeClass("is-invalid");
			}
		},
	});
});