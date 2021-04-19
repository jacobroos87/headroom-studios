$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $(".dropdown-trigger").dropdown();
    $('.quote-list > li:gt(0)').hide();
    setInterval(function() {
        $('.quote-list > li:first')
        .fadeOut(1500)
        .next()
        .delay(1500)
        .fadeIn(1500)
        .end()
        .appendTo('.quote-list');
        },  7000);
});