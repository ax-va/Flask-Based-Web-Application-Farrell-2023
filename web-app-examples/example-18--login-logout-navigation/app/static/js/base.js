/**
This self-invoking function displays all the Flask flash messages that are queued up.
The JavaScript code has to run every time a template that inherits from base.html is rendered.
**/
(function() {
    const option = {
        animation: true,
        delay: 5000, // Show 5 seconds
    };
    // Create the toastElements array variable containing all the toast HTML DOM elements on the page
    let toastElements = [].slice.call(document.querySelectorAll('.toast'));
    // Apply a function to each element in the array using the arras' map method
    toastElements.map((toastElement) => {
        toast = new bootstrap.Toast(toastElement, option);
        toast.show();
    });
})();
