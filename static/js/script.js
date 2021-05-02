$(document).ready(function () {
    $('.sidenav').sidenav({ edge: "right" });
    $(".dropdown-trigger").dropdown();
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('.datepicker').datepicker();
    $('select').formSelect();
    $('.slider').slider({ activeIndex: 1 }, 'pause');
    $('.slider').slider('pause');
    $('.left-arrow').on('click', function() {
        $('.slider').slider('prev')
    });
    $('.right-arrow').on('click', function() {
        $('.slider').slider('next')
    });
    $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: 'absolute'});
    setTimeout(function() {
    $('#flash-message').fadeOut('slow');
    }, 10000);
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
    // Initialisation for email.js

    (function () {
        emailjs.init("user_5OGKjNpFoPyKDbBVzTMSw");
    })();

    $(document).on('submit', '#contact_form', function (event) {
        event.preventDefault();
        emailjs.sendForm('service_34hzmeb', 'contact_form', '#contact_form')
            .then(function () {
                $("#modal2").modal("open");
                $("#contact_form")[0].reset();
                console.log("Form Submission SUCCESS");
            }, function (error) {
                $("#modal3").modal("open");
                $("#contact_form")[0].reset();
                console.log("Form Submission FAILED", error);
            });
    });
});