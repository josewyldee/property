$('.onboarding-modal.show-on-load').modal('show');
// $(".onboarding-modal .onboarding-slider-w").not('.slick-initialized').slick()
  if ($('.onboarding-modal .onboarding-slider-w').length) {
   $(".onboarding-modal .onboarding-slider-w").not('.slick-initialized').slick({
      dots: true,
      infinite: false,
      adaptiveHeight: true,
      slidesToShow: 1,
      slidesToScroll: 1,

    });
    $('.onboarding-modal').on('shown.bs.modal', function (e) {
      $('.onboarding-modal .onboarding-slider-w').slick('setPosition');

    });
  }
  $('.onboarding-modal').on('shown.bs.modal', function (e) {
    
    modal=$(this).attr("data-tab");
    if (modal=="sub_modal"){
      // alert("sub");
     
      $('.onboarding-modal .sub_modal').slick('slickGoTo', 0);
    }else if(modal=="alert_modal"){
      // alert("alert");
      $('.onboarding-modal .onboarding-slider-w').slick('setPosition');

    }else{
      // alert("main");
      
      $('.onboarding-modal .onboarding-slider-w').slick('slickGoTo', 0);
    }
  
  });
    
