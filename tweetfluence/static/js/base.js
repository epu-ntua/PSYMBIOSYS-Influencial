/**
 * Created by user on 11/10/2015.
 */
$(document).ready(function() {

    $(window).on('scroll', function() {
        isScrolledOutOfElement(document.getElementsByClassName('landing-section'))
    });

    $('#landing-section-chevron').on('click', function() {

        $('html, body').animate({
            scrollTop: $("#content").offset().top - $('.datefilter').height()
        }, 2000);
    });


});




$('.dropdown').hover(function() {
	  $(this).find('.dropdown-menu').stop(true, true).fadeIn();
	}, function() {
	  $(this).find('.dropdown-menu').stop(true, true).delay(50).fadeOut();
});

$('body').on('hidden.bs.modal', '.modal', function () {
	$(this).removeData('bs.modal');
});

function Loading(){
	$("#overlay").show();
}

function Done(){
	$("#overlay").hide();
}

function getCookie(name) {
    var cookieValue = null;
    if ((document.cookie) && (document.cookie != '')) {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// To remove an item from the associative array
function findAndRemove(array, properties, values) {

    var fieldMatch;
    var i;

    array.forEach(function(result, index) {

        fieldMatch = true;

        for (i=0; i < properties.length; i++)
            if (result[properties[i]] !== values[i])
                fieldMatch = false;

        if(fieldMatch) {

            //Remove from array
            array.splice(index, 1);

        }
    });
}

// This function checks if a elem is visible at the current scroll
function isScrolledOutOfElement(elem)
{
    var $elem = $(elem);
    var $window = $(window);
    var $navbar = $('.navbar');

    if ($window.scrollTop() >= $elem.height() - $navbar.height())
        $navbar.addClass('navbar-scrolled');
    else
        $navbar.removeClass('navbar-scrolled')

}


