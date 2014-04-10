$(document).ready(function() {
    var show_error = function(msg) {
        $('#success-message').hide();
        $('#error-window').text(msg);
        $('#error-window').show();
    }

    var show_success = function() {
        $('#error-window').hide();
        $('#success-message').show();
    }

    $('button').click(function(e) {
        e.preventDefault(); // Don't submit the form via browser mechanism

        var pickup_address = $('#pickup-address-field').val();

        // Show error if empty pickup address
        if (pickup_address == '') {
            show_error('Please enter an address.');
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
                show_success();
            },
            error: function() {
                show_error("It looks like this didn't send. Try again?");
            }
        });

        return false;
    });
});
