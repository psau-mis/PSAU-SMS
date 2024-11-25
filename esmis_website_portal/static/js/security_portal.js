odoo.define('esmis_website_portal.security_portal', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.SecurityPortal = publicWidget.Widget.extend({
        selector: "#portal_change_pass",

        events: {
            // 'input #new': '_onInputNewPass',
            // 'change #new2': '_onChangeNewPass2',
        },
        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            // this.$('#change_pass_submit').addClass('disabled');
            this._applyAlertStyle();
            return this._super(...arguments);
        },
        _applyAlertStyle: function () {
            var alertDiv = this.$('.alert.alert-danger');
            if (alertDiv.length) {
                var cleanedText = this._cleanText(alertDiv.text());
                alertDiv.text(cleanedText);
                alertDiv.css('white-space', 'pre-wrap');
            }
        },

        _cleanText: function (text) {
            return text.trim();
        },

        // _onInputNewPass: function (ev) {
        //     var newPassInput = $(ev.currentTarget);
        //     this.validatePassword(newPassInput);
        //     // this.validatePasswordMatch($('#new2'));
        //     if ($('#new2').val().trim() !== '') {
        //         this.validatePasswordMatch($('#new2'));
        //     } else {
        //         $('#new2').removeClass('is-valid is-invalid');
        //         $('#new2').next('.invalid-feedback').text('');
        //     }

        //     this.checkSubmitButton();
        // },

        // _onChangeNewPass2: function (ev) {
        //     var confirmPassInput = $(ev.currentTarget);
        //     // this.validatePasswordMatch(confirmPassInput);
        //     if (confirmPassInput.val().trim() !== '') {
        //         this.validatePasswordMatch(confirmPassInput);
        //     } else {
        //         confirmPassInput.removeClass('is-valid is-invalid');
        //         confirmPassInput.next('.invalid-feedback').text('');
        //     }

        //     this.checkSubmitButton();
        // },

        // validatePassword: function (input) {
        //     var password = input.val();
        //     var passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$/;

        //     var errorDiv = input.next('.invalid-feedback');
        //     if (passwordPattern.test(password)) {
        //         input.removeClass('is-invalid').addClass('is-valid');
        //         errorDiv.text('');
        //     } else {
        //         input.removeClass('is-valid').addClass('is-invalid');
        //         errorDiv.text('Password must be 8 to 16 characters long and include at least one uppercase letter, one digit, and one special character.');
        //     }

        //     this.checkSubmitButton();
        // },

        // validatePasswordMatch: function (confirmInput) {
        //     var newPassword = $('#new').val();
        //     var confirmPassword = confirmInput.val();

        //     var errorDiv = confirmInput.next('.invalid-feedback');
        //     if ($('#new').hasClass('is-valid') && newPassword === confirmPassword) {
        //         confirmInput.removeClass('is-invalid').addClass('is-valid');
        //         errorDiv.text('');
        //     } else {
        //         confirmInput.removeClass('is-valid').addClass('is-invalid');

        //         if ($('#new').hasClass('is-valid')) {
        //             errorDiv.text('Passwords do not match.');
        //         } else {
        //             errorDiv.text('Password must be 8 to 16 characters long and include at least one uppercase letter, one digit, and one special character.');
        //         }
        //     }

        //     this.checkSubmitButton();
        // },

        // checkSubmitButton: function () {
        //     if ($('#new').hasClass('is-valid') && $('#new2').hasClass('is-valid')) {
        //         this.$('#change_pass_submit').removeClass('disabled');
        //     } else {
        //         this.$('#change_pass_submit').addClass('disabled');
        //     }
        // },
    });
});
