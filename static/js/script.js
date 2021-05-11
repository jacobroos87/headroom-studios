$(document).ready(function () {

    //  Initializing Materialize animations and functionality

    $('.sidenav').sidenav({ edge: "right" });
    $(".dropdown-trigger").dropdown();
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('select').formSelect();

    //  Changed calendar to not show dates in the past

    $('.datepicker').datepicker({
        minDate: new Date(),
        format: 'dd mmm yyyy',
    });
    
    // Changed slider to always start at the first image and to not auto-scroll
    
    $('.slider').slider({ activeIndex: 1 }, 'pause');
    $('.slider').slider('pause');

    // Left and Right on click functions to replace materialize dot selector

    $('.left-arrow').on('click', function() {
        $('.slider').slider('prev')
    });
    $('.right-arrow').on('click', function() {
        $('.slider').slider('next')
    });

    // Added required to the select dropdowns on the bookings page

    $("select[required]").css({display: "block", height: 0, padding: 0, width: 0, position: 'absolute'});

    // Added a timeout function for the flash message to automatically fade out after 10s

    setTimeout(function() {
    $('#flash-message').fadeOut('slow');
    }, 10000);

    // Function for the fading quotes on the Home Page

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

    

    // Copyright current year //

    $("#copyright").text(new Date().getFullYear());

    // Initialisation for email.js

    (function () {
        emailjs.init("user_5OGKjNpFoPyKDbBVzTMSw");
    })();

    $(document).on('submit', '#contact_form', function (event) {
        event.preventDefault();
        emailjs.sendForm('service_34hzmeb', 'contact_form', '#contact_form')
            .then(function () {
                // Success Modal
                $("#modal2").modal("open");
                $("#contact_form")[0].reset();
                console.log("Form Submission SUCCESS");
            }, function (error) {
                // Error Modal
                $("#modal3").modal("open");
                $("#contact_form")[0].reset();
                console.log("Form Submission FAILED", error);
            });
    });
});