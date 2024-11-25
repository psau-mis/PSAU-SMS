odoo.define('esmis_website_portal.student_grades', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.StudentGrades = publicWidget.Widget.extend({
        selector: "#student_portal_layout",

        events: {
            'change #school_year': '_filterGradeLines',
            'click #refresh_grade': '_filterGradeLines',
        },
        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            var self = this;

            // $("#school_year").val("1");

            self._filterGradeLines();

            // this.$('#school_year').change(function () {
            //     self._filterGradeLines();
            // });
            return this._super(...arguments);
        },

        _filterGradeLines: function () {
            var selectedOption = $("#school_year option:selected");
            var selectedYear = selectedOption.attr("data-school-year"); //the school year id from esmis.school.year
            var selectedSchoolYear = $("#school_year").val(); //the grade id from esmis.grade.management.line
            var self = this;
            this._rpc({
                route: '/portal/filter_grade_lines',
                params: {
                    grade_school_year_id: selectedYear,
                },
            }).then(function (data) {
                var tbody = $('#grade_lines_table tbody');
                if (data.grades.length > 0) {
                    tbody.empty();
                    self._renderGradeLines(data.grades, selectedYear);
                }
                var fileName = 'COG - Certificate Of Grade';
                $('#download_cog_link').attr('href', '/portal/student_cog_download/' + selectedSchoolYear + '/' + fileName);
            });
        },

        _renderGradeLines: function (grades) {
            var tbody = $("#grade_lines_table tbody");
            tbody.empty();
            var counter = 1;
            $.each(grades, function (index, grade) {
                var re_exam = grade.re_exam ? grade.re_exam : '0.00';
                var row = '<tr>' +
                    '<td class="text-center">' + counter + '</td>' +
                    '<td class="text-center">' + grade.subject_code + '</td>' +
                    '<td class="text-center">' + grade.subject_description + '</td>' +
                    '<td class="text-center">' + grade.subject_units + '</td>' +
                    '<td class="text-center">' + grade.section + '</td>' +
                    '<td class="text-center">' + grade.final_eq + '</td>' +
                    '<td class="text-center">' + re_exam + '</td>' +
                    '<td class="text-center">' + grade.final_eq + '</td>' +
                    '<td class="text-center text-info">' + grade.final_eq + '</td>' +
                    '<td class="text-center text-info">' + grade.remarks + '</td>' +
                    '</tr>';
                counter++;
                tbody.append(row);
            });
        },
    });
});
