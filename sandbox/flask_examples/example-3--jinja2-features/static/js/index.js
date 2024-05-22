/*
This is vanilla JavaScript code (no frameworks like jQuery involved)
that adds an action if the "Change Banner Color" button is clicked.
*/

// Waits for the page to be loaded before executing the nested code
window.addEventListener('load', function (event) {
    // Gets a reference to "#header h1" the banner element
    let banner = document.querySelector("#header h1");
    // Adds a click event handler for the banner color-changing button
    window.addEventListener('click', function (event) {
        // Checks whether the click event originated from the button
        if (event.target.matches('.change-banner-color')) {
            // Selects a random color from bannerColors
            let color = bannerColors[Math.floor(Math.random() * bannerColors.length)];
            banner.style.backgroundColor = color;
        }
    })
});
