// Change visibility of category dropdown in navbar
document.getElementById("navbar-dropdown").addEventListener("click", function(){$('.dropdown-item').toggle();});

// Closes category dropdown on click anywhere on page
$('body').click(function(e) {
    if ($(e.target).closest('.cant-close').length === 0) {
        $('.dropdown-item').hide();
    }
});

// Change visibility of mobile menu items
document.getElementById("toogle-menu").addEventListener("click", function(){$('.navbar-links').toggle();});

// Change visibility of components menu
document.getElementById("components").addEventListener("click", function(){$('.dropdown-components').toggle();});

// Change visibility of accessories menu
document.getElementById("accessories").addEventListener("click", function(){$('.dropdown-accessories').toggle();});

// Change visibility of  peripherials menu
document.getElementById("peripherials").addEventListener("click", function(){$('.dropdown-peripherials').toggle();});

// Change visibility of mobile-devices menu
document.getElementById("mobile-devices").addEventListener("click", function(){$('.dropdown-mobile-devices').toggle();});