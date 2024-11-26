const textareas = document.querySelectorAll('.prompt-textarea');
textareas.forEach(textarea => {
    textarea.addEventListener('input', () => {
        textarea.style.height = textarea.scrollHeight + 'px';
    });
    textarea.dispatchEvent(new Event('input'));
});