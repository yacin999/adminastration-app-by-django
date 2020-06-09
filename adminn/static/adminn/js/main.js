$(function() {
    var winH = $(window).height(),
        upperNavH = $('.upper-bar').innerHeight(),
        navH = $('.navbar').innerHeight();

    $('.slider, .carousel-item').height( winH - (upperNavH + navH));    
});