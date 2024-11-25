odoo.define('esmis_website_portal.auth_signup', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.AuthSignUp = publicWidget.Widget.extend({
        selector: "#auth_signup",

        events: {
            'input #password': '_onInputNewPass',
            'change #confirm_password': '_onChangeNewPass2',
        },
        init: function () {
			this._super.apply(this, arguments);
		},
		start: function() {
            this.$('#auth_change_pass').addClass('disabled');
			return this._super(...arguments);
		},
        _onInputNewPass: function (ev) {
            var newPassInput = $(ev.currentTarget);
            this.validatePassword(newPassInput);
            // this.validatePasswordMatch($('#confirm_password'));
            if ($('#confirm_password').val().trim() !== '') {
                this.validatePasswordMatch($('#confirm_password'));
            } else {
                $('#confirm_password').removeClass('is-valid is-invalid');
                $('#confirm_password').next('.invalid-feedback').text('');
            }

            this.checkSubmitButton();
        },

        _onChangeNewPass2: function (ev) {
            var confirmPassInput = $(ev.currentTarget);
            // this.validatePasswordMatch(confirmPassInput);
            if (confirmPassInput.val().trim() !== '') {
                this.validatePasswordMatch(confirmPassInput);
            } else {
                confirmPassInput.removeClass('is-valid is-invalid');
                confirmPassInput.next('.invalid-feedback').text('');
            }

            this.checkSubmitButton();
        },

        validatePassword: function (input) {
            var password = input.val();
            var passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$/;

            var errorDiv = input.next('.invalid-feedback');
            if (passwordPattern.test(password)) {
                input.removeClass('is-invalid').addClass('is-valid');
                errorDiv.text('');
            } else {
                input.removeClass('is-valid').addClass('is-invalid');
                errorDiv.text('Password must be 8 to 16 characters long and include at least one uppercase letter, one digit, and one special character.');
            }

            this.checkSubmitButton();
        },

        validatePasswordMatch: function (confirmInput) {
            var newPassword = $('#password').val();
            var confirmPassword = confirmInput.val();

            var errorDiv = confirmInput.next('.invalid-feedback');
            if ($('#password').hasClass('is-valid') && newPassword === confirmPassword) {
                confirmInput.removeClass('is-invalid').addClass('is-valid');
                errorDiv.text('');
            } else {
                confirmInput.removeClass('is-valid').addClass('is-invalid');

                if ($('#password').hasClass('is-valid')) {
                    errorDiv.text('Passwords do not match.');
                } else {
                    errorDiv.text('Password must be 8 to 16 characters long and include at least one uppercase letter, one digit, and one special character.');
                }
            }

            this.checkSubmitButton();
        },

        checkSubmitButton: function () {
            if ($('#password').hasClass('is-valid') && $('#confirm_password').hasClass('is-valid')) {
                this.$('#auth_change_pass').removeClass('disabled');
            } else {
                this.$('#auth_change_pass').addClass('disabled');
            }
        },
    });
});
