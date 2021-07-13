// Change visibility of category dropdown in navbar
document.getElementById("nav-dropdown").addEventListener("click", function(){$('.nav-subitem').toggle();});

// Closes category dropdown on click anywhere on page
$('body').click(function(e) {
    if ($(e.target).closest('.nav-dropdown').length === 0) {
        $('.nav-subitem').hide();
    }
});
