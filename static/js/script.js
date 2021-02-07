$(document).ready(function() {
    // ----------------------------------------------------------------------------------------------------------Modals
    // ------------------------------------------------Meter ID Modal
    // Open Meter ID modal when icons with class launch-meter-id-modal are clicked.
    $(".launch-meter-id-modal").click(function() {
        $("#meter-id-modal").fadeIn();
    });
    // Close Meter ID modal when icon with ID close-meter-id-modal is clicked.
    $("#close-meter-id-modal").click(function() {
        $("#meter-id-modal").fadeOut();
    });

    // ------------------------------------------------Meter Serial Number Modal
    // Open MSN modal when icons with class launch-msn-modal are clicked.
    $(".launch-msn-modal").click(function() {
        $("#msn-modal").fadeIn();
    });
    // Close MSN modal when icon with ID close-msn-modal is clicked.
    $("#close-msn-modal").click(function() {
        $("#msn-modal").fadeOut();
    });

    // ------------------------------------------------Delete Booking Modal
    // Open Delete Booking modal when button with id launch-delete-modal is clicked.
    $("#launch-delete-modal").click(function() {
        $("#delete-booking-modal").fadeIn();
    });
    // Close Delete Booking modal when icon with id close-delete-modal is clicked.
    $("#close-delete-modal").click(function() {
        $("#delete-booking-modal").fadeOut();
    });

    // ------------------------------------------------Update Booking Modal
    // Open Update Booking modal when button with id submit-button is clicked.
    $("#submit-button").click(function() {
        $("#update-booking-modal").fadeIn();
    });
    // Close Update Booking modal when icon with id close-update-modal is clicked.
    $("#close-update-modal").click(function() {
        $("#update-booking-modal").fadeOut();
    });

    // ------------------------------------------------Delete Account Modal
    // Open Delete Account modal when button with id launch-delete-account-modal is clicked.
    $("#launch-delete-account-modal").click(function() {
        $("#delete-account-modal").fadeIn();
    });
    // Close Delete Booking modal when icon with id close-delete-modal is clicked.
    $("#close-delete-account-modal").click(function() {
        $("#delete-account-modal").fadeOut();
    });

    // ----------------------------------------------------------------------------------------------------------Form authorisation
    // Enable and disable the submit form button when the user checks/unchecks the authorisation checkbox.
    // Used on both the book.html and update_booking.html pages.
    // Below solution reached with the aid of:  https://stackoverflow.com/questions/7031226/jquery-checkbox-change-and-click-event
    $("#supplier_authorisation").change(function() {
        if ($("#supplier_authorisation").is(":checked")) {
            $("#submit-button").prop("disabled", false)
        } else {
            $("#submit-button").prop("disabled", true)
        }
    })
    
    // ----------------------------------------------------------------------------------------------------------Booking form date picker
    // Set up the install date with a datepicker widget using jQuery UI:  https://api.jqueryui.com/datepicker/
    $("#install_date" ).datepicker({
        // Change format, limit range to no earlier than 30 days from today and no later than 2 years from today.
        dateFormat: "dd/mm/yy",
        minDate: 30,
        maxDate: "+2y",
        firstDay: 1,
        // Below solution for preventing Sundays taken from: https://stackoverflow.com/questions/31770976/disable-specific-days-in-jquery-ui-datepicker
        beforeShowDay: function(date) {
            let day = date.getDay();
            return [(day != 0)];
        }
    });

});