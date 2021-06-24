// Initialize LightGallery

$(document).ready(function () {

    $("#media").lightGallery({
        speed: 0,
        toogleThumb: false,
        backdropDuration: 0,
        slideEndAnimatoin: false,
        startClass: '',
        zoom: true,
        preload: 5,
        selector: '.lg-selector'
    });

});


$(document).keypress(function (e) {
    if (e.which === 61) {
        // zoom in on =
        $('#lg-zoom-in').click();
    } else if (e.which === 45) {
        // zoom out on -
        $('#lg-zoom-out').click();
    } else if (e.which === 48) {
        // reset on 0
        $('#lg-actual-size').click();
    }
});
