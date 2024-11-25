odoo.define('esmis_website_portal.parent_grievance', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.ParentGrievance = publicWidget.Widget.extend({
        selector: "#parent_portal_layout",

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
                $('#child_academic_record').removeClass('d-none');
            } else {
                $('#child_academic_record').addClass('d-none');
            }
        },
    });
});
