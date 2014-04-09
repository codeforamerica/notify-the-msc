$(document).ready(function() {
    $('button').click(function() {
        var pickup_address = $('#pickup-address-field').val();

        if (pickup_address == '') {
            $('#error-window').text('Please enter an address.');
            $('#error-window').show();
            $('#success-message').hide();
            return false;
        }

        data_to_submit = {
            pickup_address: pickup_address
        };

        $.ajax({
            url: '/incidents', 
            data: data_to_submit, 
            method: 'POST',
            success: function(data) {
                $('#success-message').show();
                $('#error-window').hide();
            },
            error: function() {
                $('#error-window').text("It looks like this didn't send. Try again?");
                $('#error-window').show();
            }
        });
        


        return false;
    }); 
});