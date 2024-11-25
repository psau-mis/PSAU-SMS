odoo.define('esmis_website_admission.admission_website_select_type',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');

	publicWidget.registry.AdmissionSelectType = publicWidget.Widget.extend({
		selector: "#select_admission_type",
		events: {
			'change #admission_type_1': '_changeAdmissionType1',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			return this._super(...arguments);
		},
		_changeAdmissionType1: function(ev) {
			var admission_type_1 = $(ev.currentTarget);
			var selectAdmission = $("select[name='select_admission']");
			if (admission_type_1.val().length) {
				$('#admission_type_two_to_three').css('display', 'block');
				const admission_type_2 = {
					"freshmen": "New Student",
					"transferee": "Transferee",
					"continuing": "Second Courser",
					"foreign": "Foreign Applicant",
				}
				const admission_type_3 = {
					"graduate": "Graduate Level: Masteral (New Student)",
					"transferee2": "Graduate Level: Masteral (Transferee)",
					"graduate2": "Graduate Level: Doctoral (New Student)",
					"transferee3": "Graduate Level: Doctoral (Transferee)",
				}
				
				if (admission_type_1.val() == 'undergrad') {
					selectAdmission.html('');
					Object.entries(admission_type_2).forEach(entry => {
						const [key, value] = entry;
						var opt = $('<option>').text(value)
							.attr('value', key)
						selectAdmission.append(opt)
					});
				} else {
					selectAdmission.html('');
					Object.entries(admission_type_3).forEach(entry => {
						const [key, value] = entry;
						var opt = $('<option>').text(value)
							.attr('value', key)
						selectAdmission.append(opt)
					});
				}
			} else {
				selectAdmission.html('');
				$('#admission_type_two_to_three').css('display', 'none');
			}
		},
	});
});