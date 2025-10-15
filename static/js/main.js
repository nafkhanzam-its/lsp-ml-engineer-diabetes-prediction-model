// Main JavaScript for Diabetes Prediction System

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Add smooth scrolling to anchor links
    initSmoothScrolling();

    // Initialize form validation
    initFormValidation();

    // Add loading states to buttons
    initButtonStates();

    // Initialize tooltips
    initTooltips();

    // Add animation on scroll
    initScrollAnimations();

    console.log('🚀 Diabetes Prediction System initialized');
}

function initSmoothScrolling() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

function initFormValidation() {
    const form = document.getElementById('predictionForm');
    if (!form) return;

    // Add real-time validation
    const inputs = form.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateInput(this);
        });

        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });

    // Add form submission validation
    form.addEventListener('submit', function(e) {
        if (!validateForm()) {
            e.preventDefault();
            showValidationErrors();
        }
    });
}

function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);

    // Remove existing validation classes
    input.classList.remove('is-valid', 'is-invalid');

    // Get or create feedback element
    let feedback = input.parentNode.querySelector('.invalid-feedback');
    if (!feedback) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        input.parentNode.appendChild(feedback);
    }

    if (input.value === '') {
        input.classList.add('is-invalid');
        feedback.textContent = 'This field is required.';
        return false;
    }

    if (isNaN(value) || value < min || value > max) {
        input.classList.add('is-invalid');
        feedback.textContent = `Value must be between ${min} and ${max}.`;
        return false;
    }

    // Additional specific validations
    const fieldName = input.name;
    if (fieldName === 'glucose' && (value < 70 || value > 200)) {
        input.classList.add('is-invalid');
        feedback.textContent = 'Unusual glucose level. Please verify the value.';
        return false;
    }

    if (fieldName === 'bmi' && (value < 15 || value > 50)) {
        input.classList.add('is-invalid');
        feedback.textContent = 'Unusual BMI value. Please verify the calculation.';
        return false;
    }

    input.classList.add('is-valid');
    feedback.textContent = '';
    return true;
}

function validateForm() {
    const form = document.getElementById('predictionForm');
    const inputs = form.querySelectorAll('input[type="number"]');
    let isValid = true;

    inputs.forEach(input => {
        if (!validateInput(input)) {
            isValid = false;
        }
    });

    return isValid;
}

function showValidationErrors() {
    // Show toast notification for validation errors
    showToast('Please correct the highlighted fields before submitting.', 'error');
}

function initButtonStates() {
    // Add loading state functionality to buttons
    const submitBtn = document.getElementById('predictBtn');
    if (!submitBtn) return;

    const originalText = submitBtn.innerHTML;

    // Store original button state
    submitBtn.setAttribute('data-original-text', originalText);
}

function setButtonLoading(button, loading = true) {
    const originalText = button.getAttribute('data-original-text');

    if (loading) {
        button.disabled = true;
        button.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Processing...
        `;
    } else {
        button.disabled = false;
        button.innerHTML = originalText;
    }
}

function initTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initScrollAnimations() {
    // Add fade-in animation to elements as they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements that should animate
    const animateElements = document.querySelectorAll('.feature-card, .card, .alert');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

function showToast(message, type = 'info') {
    // Create toast notification
    const toastContainer = getOrCreateToastContainer();

    const toastId = 'toast-' + Date.now();
    const iconClass = getToastIcon(type);
    const bgClass = getToastBackground(type);

    const toastHTML = `
        <div class="toast ${bgClass}" id="${toastId}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="${iconClass} me-2"></i>
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);

    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 5000
    });

    toast.show();

    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

function getOrCreateToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1060';
        document.body.appendChild(container);
    }
    return container;
}

function getToastIcon(type) {
    const icons = {
        'success': 'fas fa-check-circle text-success',
        'error': 'fas fa-exclamation-circle text-danger',
        'warning': 'fas fa-exclamation-triangle text-warning',
        'info': 'fas fa-info-circle text-info'
    };
    return icons[type] || icons.info;
}

function getToastBackground(type) {
    const backgrounds = {
        'success': 'bg-light border-success',
        'error': 'bg-light border-danger',
        'warning': 'bg-light border-warning',
        'info': 'bg-light border-info'
    };
    return backgrounds[type] || backgrounds.info;
}

// Utility function to format numbers
function formatNumber(number, decimals = 1) {
    return Number(number).toFixed(decimals);
}

// Utility function to calculate BMI
function calculateBMI(weight, height) {
    if (!weight || !height) return null;
    return weight / (height * height);
}

// Function to provide health tips based on risk category
function getHealthTips(riskCategory) {
    const tips = {
        'Low Risk': [
            'Maintain a balanced diet rich in fruits and vegetables',
            'Engage in regular physical activity (150 minutes/week)',
            'Monitor your weight and blood pressure regularly',
            'Stay hydrated and limit sugary drinks',
            'Get adequate sleep (7-9 hours per night)'
        ],
        'Medium Risk': [
            'Consider consulting a nutritionist for diet planning',
            'Increase physical activity to 300 minutes/week',
            'Monitor blood glucose levels monthly',
            'Reduce refined sugar and processed food intake',
            'Manage stress through relaxation techniques'
        ],
        'High Risk': [
            'Schedule immediate consultation with a healthcare provider',
            'Consider glucose tolerance testing',
            'Implement strict dietary modifications',
            'Begin structured exercise program under supervision',
            'Monitor blood glucose levels weekly'
        ]
    };

    return tips[riskCategory] || tips['Medium Risk'];
}

// Function to export results to PDF (placeholder for future implementation)
function exportToPDF(results) {
    showToast('PDF export feature coming soon!', 'info');
}

// Function to save results locally
function saveResults(results) {
    try {
        const timestamp = new Date().toISOString();
        const savedResults = {
            ...results,
            savedAt: timestamp
        };

        localStorage.setItem('diabetes_prediction_' + timestamp, JSON.stringify(savedResults));
        showToast('Results saved successfully!', 'success');
    } catch (error) {
        showToast('Failed to save results.', 'error');
        console.error('Save error:', error);
    }
}

// Function to clear form
function clearForm() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.reset();

        // Remove validation classes
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.classList.remove('is-valid', 'is-invalid');
        });

        // Hide results section
        const resultsSection = document.getElementById('resultsSection');
        if (resultsSection) {
            resultsSection.style.display = 'none';
        }

        showToast('Form cleared successfully!', 'info');
    }
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('predictionForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }

    // Escape to clear form
    if (e.key === 'Escape') {
        clearForm();
    }
});

// Performance monitoring
window.addEventListener('load', function() {
    if ('performance' in window) {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`🚀 Page loaded in ${loadTime}ms`);
    }
});

// Export functions for global use
window.DiabetesApp = {
    showToast,
    saveResults,
    clearForm,
    exportToPDF,
    getHealthTips,
    calculateBMI,
    formatNumber
};