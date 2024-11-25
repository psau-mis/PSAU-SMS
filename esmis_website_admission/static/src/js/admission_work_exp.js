odoo.define('esmis_website_admission.admission_website_work_exp',function(require){
	"use strict";
	var publicWidget = require('web.public.widget');

	publicWidget.registry.AdmissionWorkExperienceTable = publicWidget.Widget.extend({
		selector: "#work_experience_dyn",
		events: {
			'click #work_exp_add_more': '_clickAddMoreWorkExp',
			'click #delete_work_exp_line': '_clickDeleteWorkExp',
		},
		init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
			this.work_row_counter = 1;
			return this._super(...arguments);
		},
		_clickAddMoreWorkExp: function (ev) {
			var table = $('#work_exp_table');
			this.work_row_counter += 1;
			var counter = table.find('tbody').find('tr').length + 1;
			var data = `<tr data-tr-num="${this.work_row_counter}">
				<td>
					<input id="company_name_${this.work_row_counter}" name="company_name_${this.work_row_counter}" type="text" class="form-control" required="True"/>
				</td>
				<td>
					<input id="company_role_${this.work_row_counter}" name="company_role_${this.work_row_counter}" type="text" class="form-control"/>
				</td>
				<td>
					<input id="company_address_${this.work_row_counter}" name="company_address_${this.work_row_counter}" type="text" class="form-control"/>
				</td>
				<td>
					<input id="company_star_${this.work_row_counter}t" name="company_start_${this.work_row_counter}" type="date" class="form-control"/>
				</td>
				<td>
					<input id="company_end_${this.work_row_counter}" name="company_end_${this.work_row_counter}" type="date" class="form-control"/>
				</td>
				<td>
				<button type="button" id="delete_work_exp_line"><i class="fa fa-trash-o"></i></button>
				</td>

			</tr>`;
			table.find('tbody').append(data);
			$('#company_counter').val(this.work_row_counter);
		},
		_clickDeleteWorkExp: function (ev) {
			var btn = $(ev.currentTarget);
			btn.closest('tr').remove();
		},
	});
});