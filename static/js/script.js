console.log("test")
// ----------------------------------------------------------------------------------------------------------Address Lookup
// The below code was initially copied from: https://getaddress.io/
// Free plan = 20 calls/day limit
$(document).ready(function () {
    $('#postcode_lookup').getAddress(
        {
        api_key: '7uqDAifL90eY9LxKOdzO_Q30023',  
        output_fields:{
            line_1: '#first_address_line',
            line_2: '#second_address_line',
            line_3: '#third_address_line',
            post_town: '#town',
            county: '#county',
            postcode: '#postcode'
        }
    });
});