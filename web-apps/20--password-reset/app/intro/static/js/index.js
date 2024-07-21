/*
This is vanilla JavaScript code (no frameworks like jQuery involved)
that adds an action if the "Change Banner Color" button is clicked.
*/

// Wait for the page to be loaded before executing the nested code
window.addEventListener('load', function (event) {
    // Get a reference to "div.banner" the banner element
    let banner = document.querySelector("div.banner");
    // Add a click event handler for the banner color-changing button
    window.addEventListener('click', function (event) {
        // Check whether the click event originated from the button
        if (event.target.matches('#change-banner-color')) {
            // Select a random color from bannerColors
            let color = bannerColors[Math.floor( Math.random() * bannerColors.length )];
            banner.style.backgroundColor = color;
            console.log("Change Button Color clicked");
            console.log("color:", color);
        }
    });
});
