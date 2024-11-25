// for testing ~ Jonas

odoo.define('esmis_website.admission_setup_template', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.admissionDetails = publicWidget.Widget.extend({
        selector: '#admission_form_set_up',
        events: {
            'change #select_level': '_onSelectLevelChange',
        },
        start: function () {
            this._super.apply(this, arguments);
            this._toggleAdmissionSections();
        },
        _onSelectLevelChange: function (ev) {
            this._toggleAdmissionSections();
        },
        _toggleAdmissionSections: function () {
            var selectedLevel = $('#select_level').val();
            if (selectedLevel === 'Undergraduate') {
                $('#undergrad-selection').show();
                $('#grad-selection').hide();
            } else if (selectedLevel === 'Graduate') {
                $('#undergrad-selection').hide();
                $('#grad-selection').show();
            } else {
                $('#undergrad-selection').hide();
                $('#grad-selection').hide();
            }
        },
    });
});
