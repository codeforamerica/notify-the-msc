$(document).ready(function() {
    // Setup.
    var character_limit = 50;
    $('#report').text(character_limit);

    var show_error = function(msg) {
        $('#success-message').hide();
        $('#error-window').text(msg);
        $('#error-window').show();
    };

    var show_success = function() {
        $('#error-window').hide();
        $('#success-message').show();
    };

    // Character limit reporting for clothing description field.
    $('#clothing-description-field').keyup(function() {
        current_length = $('#clothing-description-field').val().length;
        var remaining = character_limit - current_length;
        $('#report').text(remaining);
    });

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
        return $fieldset.find('.field-active label').text();
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

        var language = getSelectedFieldValue($('#language-field'));
        // Show error if empty language
        if (language == '') {
            show_error('Please select a language.');
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
            show_error('Please indicate whether the patient is interested in speaking with a caseworker.');
            return false;
        }

        var superutilizer = getSelectedFieldValue($('#superutilizer-field'));
        // Show error if empty "superutilizer?" field
        if (superutilizer === '') {
            show_error('Please select whether the patient is a frequent EMS utilizer.');
            return false;
        }

        var clothing_description = $('#clothing-description-field').val();
        // Show error if empty clothing description
        if (clothing_description === '') {
            show_error("Please enter a description of the person's clothing.");
            return false;
        }
        // Enforce the character limit
        if (clothing_description.length > character_limit) {
            show_error("Your description of the person's clothing is too long. The limit is " + character_limit + " characters.");
            return false;
        }

        data_to_submit = {
            pickup_address: pickup_address,
            hospital: hospital,
            interested: interested,
            superutilizer: superutilizer,
            language: language,
            clothing_description: clothing_description
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
