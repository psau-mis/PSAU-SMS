odoo.define('esmis_website_admission.admission_website_attachment', function(require){
	"use strict";
	var publicWidget = require('web.public.widget');

	publicWidget.registry.AdmissionWebsiteAttachment = publicWidget.Widget.extend({
		selector: "#admission_attachments_container",
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			var self = this;
			this.$target.find('input[type="file"]').each(function() {
				$(this).on('change', function (argument) {
					if ($(argument.currentTarget).val().length){
						const name = $(argument.currentTarget).attr('name');
						if (this.files[0].size > 3000000) {
							$(argument.currentTarget).addClass('is-invalid');
							$('#' + name + '_message').removeClass('d-none');
						} else {
							$(argument.currentTarget).removeClass('is-invalid');
							$('#' + name + '_message').addClass('d-none');
						}
					}
				});
			});
			return this._super(...arguments);
		},
	});
});