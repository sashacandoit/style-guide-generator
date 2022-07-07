//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($(".sticky-nav-activate").offset().top > 1) {
        $(".fixed-top").addClass("nav-scroll");
    } else {
        $(".fixed-top").removeClass("nav-scroll");
    }
});

//jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $(document).on('click', 'a.smooth-scroll', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
