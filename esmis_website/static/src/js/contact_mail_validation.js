odoo.define("esmis_website.contact_mail_validation", function (require) {
    "use strict";
    var publicWidget = require("web.public.widget");

    publicWidget.registry.ContactEmailValidation = publicWidget.Widget.extend({
        selector: "#admission_register_main",
        events: {
            "change #mobile": "_infoMobile",
            "change #email_address": "_infoEmail", // Add email validation event
            "change #father_contact": "_fatherMobile",
            "change #mother_contact": "_motherMobile",
        },
        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            return this._super(...arguments);
        },
        _infoMobile: function (ev) {
            var mobile = $(ev.currentTarget);
            var mobileMsg = $("#mobileError");
            var mobileValue = mobile.val();
            var regex = /^(09\d{9}|9\d{9})$/; // Provided mobile regex pattern
            // ACCEPTED Values +639XXXXXXXXX, 09XXXXXXXXX, 9XXXXXXXXX

            if (!regex.test(mobileValue)) {
                mobile.addClass("is-invalid");
                mobileMsg.removeClass("d-none");
            } else {
                mobile.addClass("is-valid");
                mobile.removeClass("is-invalid");
                mobileMsg.addClass("d-none");
            }
        },
        _infoEmail: function (ev) {
            var email = $(ev.currentTarget);
            var emailMsg = $("#emailError");
            var emailValue = email.val();
            var emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/; // Email regex pattern

            if (!emailRegex.test(emailValue)) {
                email.addClass("is-invalid");
                emailMsg.removeClass("d-none");
            } else {
                email.addClass("is-valid");
                email.removeClass("is-invalid");
                emailMsg.addClass("d-none");
            }
        },
        _fatherMobile: function (ev) {
            var mobile = $(ev.currentTarget);
            var mobileMsg = $("#mobileErrorFather");
            var mobileValue = mobile.val();
            var regex = /^(09\d{9}|9\d{9})$/; // Provided mobile regex pattern
            // ACCEPTED Values +639XXXXXXXXX, 09XXXXXXXXX, 9XXXXXXXXX

            if (!regex.test(mobileValue)) {
                mobile.addClass("is-invalid");
                mobileMsg.removeClass("d-none");
            } else {
                mobile.addClass("is-valid");
                mobile.removeClass("is-invalid");
                mobileMsg.addClass("d-none");
            }
        },
        _motherMobile: function (ev) {
            var mobile = $(ev.currentTarget);
            var mobileMsg = $("#mobileErrorMother");
            var mobileValue = mobile.val();
            var regex = /^(09\d{9}|9\d{9})$/; // Provided mobile regex pattern
            // ACCEPTED Values +639XXXXXXXXX, 09XXXXXXXXX, 9XXXXXXXXX

            if (!regex.test(mobileValue)) {
                mobile.addClass("is-invalid");
                mobileMsg.removeClass("d-none");
            } else {
                mobile.addClass("is-valid");
                mobile.removeClass("is-invalid");
                mobileMsg.addClass("d-none");
            }
        },
    });
});
