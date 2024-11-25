odoo.define('esmis_website_admission.admission_website_select_course_program',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');

	publicWidget.registry.AdmissionSelectCourseProgram = publicWidget.Widget.extend({
		selector: "#select_course_program",
		events: {
			'change #course1_id': '_changeFirstChoice',
			'change #course2_id': '_changeSecondChoice',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			return this._super(...arguments);
		},
		_changeFirstChoice: function(ev) {
			var first_choice = $(ev.currentTarget);
			$('#course2_id').prop('selectedIndex',0).trigger('change');
			$('#course3_id').prop('selectedIndex',0);
			$('#course2_id').find('option:hidden').each(function () {
				$(this).show();
			});
			if (first_choice.val().length) {
				$('#course2_id').removeAttr('disabled');
				$('#course2_id').find('option').each(function () {
					if ($(this).val() == first_choice.val()) {
						$(this).hide();
					}
				});
			} else {
				$('#course2_id').attr('disabled', true);
			}
		},
		_changeSecondChoice: function(ev) {
			var first_choice = $('#course1_id');
			var second_choice = $(ev.currentTarget);
			$('#course3_id').prop('selectedIndex',0);
			$('#course3_id').find('option:hidden').each(function () {
				$(this).show();
			});
			if (second_choice.val().length) {
				$('#course3_id').removeAttr('disabled');
				$('#course3_id').find('option').each(function () {
					if ($(this).val() == first_choice.val() || $(this).val() == second_choice.val()) {
						$(this).hide();
					}
				});
			} else {
				$('#course3_id').attr('disabled', true);
			}
		},
	});
});