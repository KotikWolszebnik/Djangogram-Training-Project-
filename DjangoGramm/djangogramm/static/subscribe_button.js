// import "./jquery/dist/jquery.js";

function subscribe_or_unsubscribe( event ) {
    if ( $( event.currentTarget ).attr( 'action' ) === "/subscribe/" ) {
        var url = "/subscribe/";
        var new_action = "/unsubscribe/";
        var new_button_string = 'Unsubscribe <i class="bi bi-person-dash"></i>'
        var message = 'You are subscribed';
    } else {
        var url = "/unsubscribe/";
        var new_action = "/subscribe/";
        var new_button_string = 'Subscribe <i class="bi bi-person-plus"></i>'
        var message = '';
    };
    event.preventDefault();
    $.ajax(
        {
            method: "POST",
            url: url,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: $( event.currentTarget ).children( 'input[name="csrfmiddlewaretoken"]' ).attr( "value" ),
                addressee: $( event.currentTarget ).children( 'input[name="addressee"]' ).attr( "value" )
            }
        }
    ).done(
        function() {
            $("#subscribed_message").html(message)
            event.currentTarget.action = new_action;
            var new_button = event.currentTarget[2];
            new_button.innerHTML = new_button_string;
        }
    );
};


$( '#subscribe_unsubscribe' ).on( "submit", subscribe_or_unsubscribe );