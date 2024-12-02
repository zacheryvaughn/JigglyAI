// Auto-adjust textarea height
const textareas = document.querySelectorAll('.prompt-textarea');
textareas.forEach(textarea => {
    const adjustHeight = () => {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
    };

    textarea.addEventListener('input', adjustHeight);
    adjustHeight();

    // Add border to container on focus
    const promptContainer = textarea.closest('#prompt-container'); // Find the closest container
    if (promptContainer) {
        textarea.addEventListener('focus', () => {
            promptContainer.classList.add('focused');
        });

        textarea.addEventListener('blur', () => {
            promptContainer.classList.remove('focused');
        });
    }
});

const menuButtonList = document.getElementById('menu-button-list');
const headerMenuButton = document.getElementById('header-menu-button');
let closeTimeout;
const closeMenu = () => {
    menuButtonList.classList.remove('open');
};
const startCloseTimer = () => {
    clearTimeout(closeTimeout);
    closeTimeout = setTimeout(closeMenu, 3000);
};
const cancelCloseTimer = () => {
    clearTimeout(closeTimeout);
};
headerMenuButton.addEventListener('click', () => {
    const isOpen = menuButtonList.classList.toggle('open');
    if (isOpen) {
        startCloseTimer();
    }
});
document.addEventListener('click', (event) => {
    const isClickInside = menuButtonList.contains(event.target) || headerMenuButton.contains(event.target);
    if (!isClickInside) {
        closeMenu();
    }
});
menuButtonList.addEventListener('mouseover', cancelCloseTimer); // Stop the timer when hovering
menuButtonList.addEventListener('mouseout', startCloseTimer);   // Restart the timer when leaving


// Toggle dropdowns
const settingsDropdownContainer = document.querySelectorAll('.settings-dropdown-container');
const settingsDropdownHeader = document.querySelectorAll('.settings-dropdown-header');
const dropdownHeaderChevron = document.querySelectorAll('.dropdown-header-chevron');

// Loop through each header
settingsDropdownHeader.forEach(header => {
    header.addEventListener('mousedown', () => {
        const container = header.closest('.settings-dropdown-container');
        const chevron = header.querySelector('.dropdown-header-chevron');
        header.classList.toggle('open');
        chevron.classList.toggle('open');
        container.classList.toggle('open');
    });
});

// Get references to relevant elements
const upscaleContext = document.getElementById('upscale-context');
const upscaleNewGeneration = document.getElementById('upscale-new-generation');
const upscaleButtonContainer = document.getElementById('upscale-button-container');
const generateButton = document.getElementById('generate-button');
const generateUpscaleButton = document.getElementById('generate-upscale-button');

// Add event listener for clicks on the parent container
upscaleContext.addEventListener('click', (event) => {
    // Check if the clicked element is part of the toggleable items
    if (event.target.id === 'upscale-current-image' || event.target.id === 'upscale-new-generation') {
        // Remove 'selected' class from all children
        Array.from(upscaleContext.children).forEach(child => {
            child.classList.remove('selected');
        });
        // Add 'selected' class to the clicked element
        event.target.classList.add('selected');

        // Check if "upscale-new-generation" has the "selected" class
        if (upscaleNewGeneration.classList.contains('selected')) {
            upscaleButtonContainer.style.opacity = '0.35'; // Hide the button container
            upscaleButtonContainer.style.pointerEvents = 'none'; // Hide the button container
            generateButton.style.display = 'none';
            generateUpscaleButton.style.display = 'flex';
        } else {
            upscaleButtonContainer.style.opacity = '1'; // Hide the button container
            upscaleButtonContainer.style.pointerEvents = 'all'; // Hide the button container
            generateButton.style.display = 'flex';
            generateUpscaleButton.style.display = 'none';
        }
    }
});

document.getElementById('recycle-button').addEventListener('click', function() {
    // Remove the "selected" class from both buttons
    document.getElementById('recycle-button').classList.add('selected');
    document.getElementById('random-button').classList.remove('selected');
});

document.getElementById('random-button').addEventListener('click', function() {
    // Remove the "selected" class from both buttons
    document.getElementById('random-button').classList.add('selected');
    document.getElementById('recycle-button').classList.remove('selected');
});

// Get all the size-ratio-option elements
const sizeRatioOptions = document.querySelectorAll('.size-ratio-option');
sizeRatioOptions.forEach(option => {
    option.addEventListener('click', () => {
        sizeRatioOptions.forEach(opt => opt.classList.remove('selected'));
        option.classList.add('selected');
    });
});

