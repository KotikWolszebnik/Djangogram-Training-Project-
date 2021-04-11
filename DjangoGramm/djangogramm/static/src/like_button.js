import "./bootstrap-5.0.0-beta2-dist/css/bootstrap.min.css";
import "./style.css";
import "./bootstrap-icons-1.4.1/bootstrap-icons.css";

import "./bootstrap-5.0.0-beta2-dist/js/bootstrap.min.js";
import * as $ from "./jquery/dist/jquery.js";

function like_or_unlike( event ) {
    if ( $( event.currentTarget ).attr( 'action' ) === "/post/like/" ) {
        var url = "/post/like/";
        var new_action = "/post/unlike/";
        var new_style = "font-size: 1.5rem; color: forestgreen;";
        var new_class = "bi bi-suit-heart-fill";
    } else {
        var url = "/post/unlike/";
        var new_action = "/post/like/";
        var new_style = "font-size: 1.5rem;";
        var new_class = "bi bi-suit-heart";
    };
    event.preventDefault();
    $.ajax(
        {
            method: "POST",
            url: url,
            dataType: "json",
            data: {
                csrfmiddlewaretoken: $( event.currentTarget ).children( 'input[name="csrfmiddlewaretoken"]' ).attr( "value" ),
                slug: $( event.currentTarget ).children( 'input[name="slug"]' ).attr( "value" )
            }
        }
    ).done(
        function( response ) {
            event.currentTarget.action = new_action;
            var heart = event.currentTarget[2].children[0];
            $( heart ).attr(
                {
                'class': new_class,
                'style': new_style
                }
            );
            var likes_number = event.currentTarget[2].children[1];
            likes_number.innerHTML = response[ 'likes_number' ];
        }
    );
};

$( 'form[action="/post/like/"]' ).on( "submit", like_or_unlike );
$( 'form[action="/post/unlike/"]' ).on( "submit", like_or_unlike );