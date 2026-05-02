document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    
    form.addEventListener('submit', () => {
        const button = document.querySelector('.btn-predict');
        button.innerHTML = "Processing Analysis...";
        button.style.opacity = "0.7";
        button.disabled = true;
    });

    // Add subtle animation to input fields
    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = "scale(1.02)";
            input.parentElement.style.transition = "0.3s";
        });
        input.addEventListener('blur', () => {
            input.parentElement.style.transform = "scale(1)";
        });
    });
});