odoo.define('esmis_website_admission.admission_website_student_image', function(require){
	"use strict";
	var publicWidget = require('web.public.widget');
	var admission_register = require('esmis_website_admission.admission_register');

	admission_register.AdmissionWebsiteRegister.include({
		events:_.extend({}, admission_register.AdmissionWebsiteRegister.prototype.events || {}, {
			'change input#student_image': '_changeStudentImage',
			'change input#applicant_signature': '_changeSignatureImage',
		}),
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			return this._super(...arguments);
		},
		_changeStudentImage: function (ev) {
			var imgInp = $(ev.currentTarget);
			const [file] = imgInp.prop('files');
			if (file) {
				$('#student_image_display').attr('src', URL.createObjectURL(file));
			} else {
				$('#student_image_display').attr('src', '/esmis_website_admission/static/src/img/placeholder-avatar.jpg');
			}
		},
		_changeSignatureImage: function (ev) {
			var imgInp = $(ev.currentTarget);
			const [file] = imgInp.prop('files');
			if (file) {
				$('#applicant_signature_display').attr('src', URL.createObjectURL(file));
			} else {
				$('#applicant_signature_display').attr('src', '/esmis_website_admission/static/src/img/placeholder-avatar.jpg');
			}
		},
	});
});