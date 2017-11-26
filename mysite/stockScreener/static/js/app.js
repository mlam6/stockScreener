$(window).on("scroll touchmove", function() {

    // Change .home navbar css styles
    if ($(document).scrollTop() >= $("#home").position().top) {
      $('body').css('background-color','white');
      $('#mainNav').css('background-color','#333');
      $('#mainNav li a').css('color','#ccc');
      $('#nav-1 a').css('color','#ccc');
      $('#mainNav li a').css('font-weight','400');
      $('#mainNav li a').css('text-transform','none');
      $('#nav-1 a').css('font-weight','700');
      $('#nav-1 a').css('text-transform','uppercase');
      $('a.navbar-brand.page-scroll').css('color','#ccc');
    }
    // Change .about background/navbar css styles
    if ($(document).scrollTop() >= $("#watchlist").position().top) {
        console.log("About escapes me!");
        $('body').css('background-color','white');
        $('#mainNav').css('background-color','#333');
        $('#mainNav li a').css('color','#ccc');
        $('#nav-2 a').css('color','#ccc');
        $('#mainNav li a').css('font-weight','400');
        $('#mainNav li a').css('text-transform','none');
        $('#nav-2 a').css('font-weight','700');
        $('#nav-2 a').css('text-transform','uppercase');
        $('a.navbar-brand.page-scroll').css('color','#ccc');
    }
    // Change .menu background/navbar css styles
    if($(document).scrollTop() >= $("#generate").position().top) {
        console.log("Menu escapes me!");
        $('body').css('background-color','white');
        $('#mainNav').css('background-color','#333');
        $('#mainNav li a').css('color','#ccc');
        $('#nav-3 a').css('color','#ccc');
        $('#mainNav li a').css('font-weight','400');
        $('#mainNav li a').css('text-transform','none');
        $('#nav-3 a').css('font-weight','700');
        $('#nav-3 a').css('text-transform','uppercase');
        $('a.navbar-brand.page-scroll').css('color','#ccc');
    }
});

$(document).ready(function () {

    $('.navbar-collapse a').on('click',function(){
        $('.navbar-collapse').collapse('hide');
    });

})
