import * as $ from "./jquery/dist/jquery.js";

function delete_post( event ) {
    var slug = $( event.currentTarget ).children( 'input[name="slug"]' ).attr( "value" )
    event.preventDefault();
    $.ajax(
        {
            method: "POST",
            url: "/post/delete/",
            dataType: "json",
            data: {
                csrfmiddlewaretoken: $( event.currentTarget ).children( 'input[name="csrfmiddlewaretoken"]' ).attr( "value" ),
                slug: slug
            }
        }
    ).done(
        function( response ) {
            $( `#post_card_${slug}` ).remove()
        }
    );
};

$( "form[action='/post/delete/']" ).on( "submit", delete_post );