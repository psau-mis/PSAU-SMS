odoo.define('esmis_website_portal.parent_child_subjects', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.ParentChildSubjects = publicWidget.Widget.extend({
        selector: "#parent_portal_layout",

        events: {
            'change #school_year_subject': '_filterEnrolledSubjects',
            'click #refresh_subject': '_filterEnrolledSubjects',
        },

        start: function (data) {
            var self = this;

            // $("#school_year_subject").val("1");

            self._filterEnrolledSubjects();

            // this.$('#school_year_subject').change(function () {
            //     self._filterEnrolledSubjects();
            // });
            return this._super(...arguments);
        },

        _filterEnrolledSubjects: function () {
            var selectedOption = $("#school_year_subject option:selected");
            var selectedYear = selectedOption.attr("data-school-year"); //the school year id from esmis.school.year
            var selectedSchoolYear = $("#school_year_subject").val(); //the enrollment record id from esmis.enrollment
            var self = this;
            this._rpc({
                route: '/parent/filter_child_subjects',
                params: {
                    subject_school_year_id: selectedYear,
                },
            }).then(function (data) {
                var childId = data.child_id;

                localStorage.setItem('child_id', childId);

                $('#enrolled_subjects_table tbody').empty();
                self._renderEnrolledSubjects(data.enrolled_subjects, data.total_units_array, selectedYear);

                var fileName = 'COR - ' + (data.child_id);
                $('#download_cor_link').attr('href', '/parent/download_cor/' + selectedSchoolYear + '/' + fileName );
            });
        },

        _renderEnrolledSubjects: function (enrolledSubjects, totalUnitsArray) {
            var tbody = $("#enrolled_subjects_table tbody");
            tbody.html('');
            var counter = 1;
            $.each(enrolledSubjects, function (index, subject) {
                var subject_lines = '<tr>' +
                        '<td>' + counter + '</td>' +
                        '<td>' + subject.subject_code + '</td>' +
                        '<td>' + subject.subject_desc + '</td>' +
                        '<td>' + subject.units + '</td>' +
                        '<td>' + subject.lec_hrs_week + '</td>' +
                        '<td>' + subject.lab_hrs_week + '</td>' +
                        '<td>' + subject.section + '</td>' +
                        '<td>' + subject.sched_display + '</td>' +
                        '<td>' + subject.teacher_name + '</td>' +
                    '</tr>';
                counter++;
                tbody.append(subject_lines);
            });
            $.each(totalUnitsArray, function (index, total) {
                var totalRow = '<tr>' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td>' + total.total_units + '</td>' +
                    '<td>' + total.total_lec_units + '</td>' +
                    '<td>' + total.total_lab_units + '</td>' +
                    '<td></td>' +
                    '<td></td>' +
                    '<td></td>' +
                '</tr>';
                tbody.append(totalRow);
            });
        },
    });
});
