const textareas = document.querySelectorAll('.prompt-textarea');
const headers = document.querySelectorAll('.settings-dropdown-header');

textareas.forEach(textarea => {
    const adjustHeight = () => {
        textarea.style.height = 'auto'; // Reset height to auto to recalculate
        textarea.style.height = `${textarea.scrollHeight}px`; // Set height to fit content
    };

    textarea.addEventListener('input', adjustHeight);

    // Initialize the height on page load
    adjustHeight();
});

headers.forEach(header => {
    const content = header.nextElementSibling; // Assumes .settings-dropdown-content is directly after the header

    if (content) {
        // Preserve initial height (either 0px or 300px based on CSS)
        content.style.transition = 'height 0.3s'; // Smooth transition effect

        header.addEventListener('click', () => {
            // Toggle between 0px and 300px
            content.style.height = content.style.height === '0px' ? '300px' : '0px';
        });
    }
});