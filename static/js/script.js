console.log("test")
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
if (document.getElementById("install_date")) {
    let today = new Date();
    today.setDate(today.getDate() + 30)
    let day = today.getDate();
    if (day < 10) {
        day = "0" + day;
    }
    let month = today.getMonth()+1;
    if (month < 10) {
        month = "0" + month;
    }
    let year = today.getFullYear();
    today = year+"-"+month+"-"+day;
    document.getElementById("install_date").setAttribute("min", today);
};

// ----------------------------------------------------------------------------------------------------------Modals

// ------------------------------------------------Check for an element on the book.html page and run these rules on that page.
if (document.getElementById("launch-meter-id-modal-1")) {
// ------------------------------------------------Meter ID Modal
    document.getElementById("launch-meter-id-modal-1").addEventListener("click", function getElement() {
        document.getElementById("meter-id-modal").classList.remove("d-none");
    });

    document.getElementById("launch-meter-id-modal-2").addEventListener("click", function getElement() {
        document.getElementById("meter-id-modal").classList.remove("d-none");
    });

    document.getElementById("close-meter-id-modal").addEventListener("click", function getElement() {
        document.getElementById("meter-id-modal").classList.add("d-none");
    });

// ------------------------------------------------Meter Serial Number Modal
    document.getElementById("launch-msn-modal-1").addEventListener("click", function getElement() {
        document.getElementById("msn-modal").classList.remove("d-none");
    });

    document.getElementById("launch-msn-modal-2").addEventListener("click", function getElement() {
        document.getElementById("msn-modal").classList.remove("d-none");
    });

    document.getElementById("close-msn-modal").addEventListener("click", function getElement() {
        document.getElementById("msn-modal").classList.add("d-none");
    });
};

// ------------------------------------------------Delete Booking Modal

if (document.getElementById("lanch-delete-modal")) {
    document.getElementById("lanch-delete-modal").addEventListener("click", function getElement() {
        console.log("Test Delete")
        document.getElementById("delete-booking-modal").classList.remove("d-none");
    });

    document.getElementById("close-delete-booking-modal").addEventListener("click", function getElement() {
        document.getElementById("delete-booking-modal").classList.add("d-none");
    });
};
