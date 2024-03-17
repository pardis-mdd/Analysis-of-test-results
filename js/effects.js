$(document).ready(function () {
  $(".menu a").each(function (index, elemento) {
    $(this).css({
      top: "-200px",
    });

    $(this).animate(
      {
        top: "0",
      },
      2000 + index * 500
    );
  });


  if ($(window).width() > 800) {
    $("header .texts").css({
      opacity: 0,
      marginTop: 0,
    });

    $("header .texts").animate(
      {
        opacity: 1,
        marginTop: "-52px",
      },
      1500
    );
  }

  

  var acercaDe = $("#aboutCls").offset().top,
    menu = $("#platillos").offset().top,
    gallery = $("#gallery").offset().top,
    location = $("#location").offset().top;

  $("#btn-aboutCls").on("click", function (e) {
    e.preventDefault();
    $("html, body").animate(
      {
        scrollTop: acercaDe - 200,
      },
      500
    );
  });

  $("#analysisBtn").on("click", function (e) {
    e.preventDefault();
    $("html, body").animate(
      {
        scrollTop: menu,
      },
      500
    );
  });

  $("#aboutUsBtn").on("click", function (e) {
    e.preventDefault();
    $("html, body").animate(
      {
        scrollTop: gallery,
      },
      500
    );
  });

  $("#enterBtn").on("click", function (e) {
    e.preventDefault();
    $("html, body").animate(
      {
        scrollTop: location,
      },
      500
    );
  });
});
