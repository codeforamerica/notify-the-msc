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

    // Handle switching active fields
    $('fieldset .field').click(function() {
        var clicked_field = $(this);
        var parent_fieldset = clicked_field.parent('fieldset');
        
        // Clear out the currently active field
        parent_fieldset.find('.field').removeClass('field-active');

        // Make the clicked field active
        clicked_field.addClass('field-active');
    });

    // fetch active value from field
    function getSelectedFieldValue($fieldset) {
        return $fieldset.find('.field-active label').text()
    }

    // Handle submit button
    $('button').click(function(e) {
        e.preventDefault(); // Don't submit the form via browser mechanism

        var pickup_address = $('#pickup-address-field').val();
        // Show error if empty pickup address
        if (pickup_address === '') {
            show_error('Please enter an address.');
            return false;
        }

        var hospital = getSelectedFieldValue($('#hospital-field'));
        // Show error if empty hospital
        if (hospital === '') {
            show_error('Please select a hospital.');
            return false;
        }

        var interested = getSelectedFieldValue($('#interested-field'));
        // Show error if empty "interested?" field
        if (interested === '') {
            show_error('Please choose if the patient is interested in speaking with a caseworker.')
            return false;
        }

        var homeless = getSelectedFieldValue($('#homeless-field'));
        // Show error if empty "homeless?" field
        if (homeless === '') {
            show_error('Please choose if the patient is homeless.')
            return false;
        }

        data_to_submit = {
            pickup_address: pickup_address,
            hospital: hospital,
            interested: interested,
            homeless: homeless
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
