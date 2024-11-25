odoo.define('esmis_website_admission.admission_notice_snippet',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');
	var AdmissionNotice = publicWidget.Widget.extend({
		selector: ".admission_notice",
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			var self = this;
			this._rpc({
				route: '/admission_notice_data',
				params: {},
			}).then(function (result) {
				if (result === false) {
					$('.notice_active').addClass('d-none');
					$('.notice_inactive').removeClass('d-none');
				} else {
					$('.notice_active').removeClass('d-none');
					$('.notice_inactive').addClass('d-none');
					console.log(result);
					$('.active_school_year').text(result);
				}
			});
			return this._super(...arguments);
		},
	});
	publicWidget.registry.dynamic_snippet_blog = AdmissionNotice;
	return AdmissionNotice;
});