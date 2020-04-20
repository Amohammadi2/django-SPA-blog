$(document).ready(function(){

    /* animations for the buttons*/
    $(".side-bar-item").click(function(){
        $(this).children(".side-bar-item-anim").css({
            "width": "100%",
            "opacity": ".5",
            "left": "0%",
        });
        setTimeout(() => {
            $(this).children(".side-bar-item-anim").css({
                "opacity": ".0",
                "color": "none",
            });
        }, 100);
        setTimeout(() => {
            $(this).children(".side-bar-item-anim").css({
                "width": "0%",
                "left": "50%",
            });
        }, 200);
    });


    /* sidebar toggler animations*/
    function sidebarToggler(){
        var $darkAreaDisplay = $(".dark-area").css("display");
        $(".dark-area").css({
            "display": $darkAreaDisplay == "none" ? "block" : "none",
            "opacity": $darkAreaDisplay == "none" ? "1" : "0",
        });
        // if $darkAreaDisplay is none so load the sidebar otherwide hide it
        $("div#sb").css({
            "left": $darkAreaDisplay == "none" ? "0" : "-50%",
        });
    }

    // toggle the sidebar if user clicks on sidebar toggler button
    $("li#side-bar-toggler").click(function(){
        sidebarToggler();
    });

    
    // change the position of magic line when user hovers on elements in navbar
    $(".nav-item").hover(function(){
        var position = $(this).offset();
        var left = position.left;
        $(".magic-line").css("left", left);
        $(".magic-line").css("width", $(this).width());
    });

    // collapse toggler
    $(".side-bar-item-header").click(function(){
        $(this).siblings('.collapse').collapse("toggle");
        var $text = $(this).children(".target").text();
        // if text is + then - otherwise +
        $(this).children(".target").text($text == "+" ? "-" : "+");
    });

    $(".nav-item").click(function (){
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    });

    $(".dark-area").click(function (){
        sidebarToggler();
    });

    // initialize all bootstrap tooltips [code snippet from w3schools.com]
    $('[data-toggle="tooltip"]').tooltip();
});