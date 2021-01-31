// ----------------------------------------------------------------------------------------------------------Address Lookup
// The below code was initially copied from: https://getaddress.io/
// Free plan = 20 calls/day limit
// $(document).ready(function () {
//     $('#postcode_lookup').getAddress(
//         {
//         api_key: '7uqDAifL90eY9LxKOdzO_Q30023',  
//         output_fields:{
//             line_1: '#first_address_line',
//             line_2: '#second_address_line',
//             line_3: '#third_address_line',
//             post_town: '#town',
//             county: '#county',
//             postcode: '#postcode'
//         }
//     });
// });

// ----------------------------------------------------------------------------------------------------------Booking form date picker
// Enforce a minimum date on the Booking form date picker.  Earliest booking date must be made 30 days in advance of today.
// Solution found here:  https://stackoverflow.com/questions/32378590/set-date-input-fields-max-date-to-today
// And here: https://stackoverflow.com/questions/44827066/add-30-days-to-a-current-date-js


// if (document.getElementById("install_date")) {
//     let today = new Date();
//     today.setDate(today.getDate() + 30)
//     let day = today.getDate();
//     if (day < 10) {
//         day = "0" + day;
//     }
//     let month = today.getMonth()+1;
//     if (month < 10) {
//         month = "0" + month;
//     }
//     let year = today.getFullYear();
//     today = year+"-"+month+"-"+day;
//     document.getElementById("install_date").setAttribute("min", today);
// };

// ----------------------------------------------------------------------------------------------------------Modals

$(document).ready(function() {

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

    // Set up the install date with a datepicker widget using jQuery UI:  https://api.jqueryui.com/datepicker/
    // $("#install_date" ).datepicker();
    // $.datepicker.formatDate("dd/mm/yyyy");

    // ------------------------------------------------Delete Booking Modal
    // Open Delete Booking modal when button with id launch-delete-modal is clicked.
    $("#launch-delete-modal").click(function() {
        $("#delete-booking-modal").fadeIn();
    });
    // Close Delete Booking modal when icon with id close-delete-modal is clicked.
    $("#close-delete-modal").click(function() {
        $("#delete-booking-modal").fadeOut();
    });

});