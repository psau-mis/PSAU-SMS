odoo.define("esmis_website_portal.student_enrollment_multistep", function (require) {
    "use strict";
    var publicWidget = require("web.public.widget");
    var ajax = require("web.ajax");

    publicWidget.registry.EnrollmentMultistep = publicWidget.Widget.extend({
        selector: "#smartwizard",
        events: {
            // Define events here
        },
        start: function () {
            // The leaveStep event triggers just before leaving from a step. You can cancel the event by returning false,
            // so the navigation is also be cancelled and the wizard will retain the current state.
            // Leave step event is used for validating the forms console log each to see
            $("#smartwizard").on("leaveStep", function (e, anchorObject, currentStepIdx, nextStepIdx, stepDirection) {});

            // The showStep event triggers when a step is shown.
            // EVENT PARAMETERS
            // The event will receive the following parameters:
            //// anchorObject - (object) jQuery object of the anchor element.
            //// stepIndex (integer) Index of the step.
            //// stepDirection - (string) Step direction.
            //// stepPosition - (string) Step position.
            $("#smartwizard").on("showStep", function (e, anchorObject, stepIndex, stepDirection, stepPosition) {
                console.log("You are on step " + stepIndex + " now");
                if (stepPosition === "last") {
                    $("#btnFinish").removeClass("d-none");
                    $("#btnFinish1").removeClass("d-none");
                    $("#btnFinish2").removeClass("d-none");
                } else {
                    $("#btnFinish").addClass("d-none");
                    $("#btnFinish1").addClass("d-none");
                    $("#btnFinish2").addClass("d-none");
                }
            });

            // Smart Wizard parameters
            $("#smartwizard").smartWizard({
                selected: 0, // Initial selected step, 0 = first step
                theme: "dots", // basic, arrows, square, round, dots
                justified: true, // Nav menu justification. true/false
                autoAdjustHeight: true, // Automatically adjust content height
                backButtonSupport: true, // Enable the back button support
                enableUrlHash: true, // Enable selection of the step based on url hash
                transition: {
                    animation: "none",
                },
                toolbar: {
                    position: "bottom", // none/ top/ both bottom
                    showNextButton: true, // show/hide a Next button
                    showPreviousButton: true, // show/hide a Previous button
                    extraHtml: `<button class="btn btn-success ms-1 d-none" id="btnFinish">Print Pre-Assessment</button>
                                <button class="btn btn-success ms-1 d-none" id="btnFinish1">Print COR</button>
                                <button class="btn btn-success ms-1 d-none" id="btnFinish2">Print Student Actual Load</button>`, // Extra html to show on toolbar
                },
                anchor: {
                    enableNavigation: false, // Enable/Disable anchor navigation
                    enableNavigationAlways: false, // Activates all anchors clickable always
                    enableDoneState: true, // Add done state on visited steps
                    markPreviousStepsAsDone: true, // When a step selected by url hash, all previous steps are marked done
                    unDoneOnBackNavigation: true, // While navigate back, done state will be cleared
                    enableDoneStateNavigation: true, // Enable/Disable the done state navigation
                },
                keyboard: {
                    keyNavigation: false, // Enable/Disable keyboard navigation(left and right keys are used if enabled)
                    keyLeft: [37], // Left key code
                    keyRight: [39], // Right key code
                },
                lang: {
                    // Language variables for button
                    next: "Continue",
                    previous: "Back",
                },
                disabledSteps: [], // Array Steps disabled
                errorSteps: [], // Array Steps error
                warningSteps: [], // Array Steps warning
                hiddenSteps: [], // Hidden steps
                getContent: null, // Callback function for content loadings
            });
        },
    });
});
