odoo.define('esmis_website_portal.student_grievance', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.ParentGrievance = publicWidget.Widget.extend({
        selector: "#student_portal_layout",

        events: {
            'change #grievance_category': '_showAcademicRecord',
        },
        init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
            var self = this;

			return this._super(...arguments);
		},
        _showAcademicRecord: function () {
            var grievanceCategory = $('#grievance_category').val();
            
            if (grievanceCategory === 'academic') {
                $('#student_academic_record').removeClass('d-none');
            } else {
                $('#student_academic_record').addClass('d-none');
            }
        },
    });
});
