document.querySelector(".logo").onclick = function() {
	window.location.href = "/";
};
document.addEventListener("DOMContentLoaded", function () {
    // Get all elements with the class 'fade-in'
    const fadeElements = document.querySelectorAll('.fade-in');

    // Function to check if an element is in the viewport
    function isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // Function to handle the fade-in effect
    function fadeInElements() {
        fadeElements.forEach((element) => {
            if (isInViewport(element)) {
                element.classList.add('visible');
            }
        });
    }

    // Initial check on page load
    fadeInElements();

    // Listen for scroll events and check for visibility on each scroll
    document.addEventListener('scroll', fadeInElements);
});