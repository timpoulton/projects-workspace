/**
 * FAQ Accordion JavaScript
 * Handles the accordion functionality for FAQ sections
 */

class FAQAccordion {
    constructor() {
        this.init();
    }

    init() {
        // Find all FAQ items
        this.faqItems = document.querySelectorAll('.faq-item');
        
        // Add click event listeners
        this.faqItems.forEach(item => {
            const header = item.querySelector('.faq-header');
            if (header) {
                header.addEventListener('click', () => this.toggleFAQ(item));
            }
        });

        // Add keyboard navigation
        this.setupKeyboardNavigation();
    }

    toggleFAQ(item) {
        const isActive = item.classList.contains('active');
        
        // Close all other FAQ items (optional - remove if you want multiple open)
        this.faqItems.forEach(otherItem => {
            if (otherItem !== item && otherItem.classList.contains('active')) {
                this.closeFAQ(otherItem);
            }
        });

        // Toggle the clicked item
        if (isActive) {
            this.closeFAQ(item);
        } else {
            this.openFAQ(item);
        }
    }

    openFAQ(item) {
        const content = item.querySelector('.faq-content');
        const answer = item.querySelector('.faq-answer');
        
        // Add active class
        item.classList.add('active');
        
        // Set proper max-height for smooth animation
        if (content && answer) {
            const contentHeight = answer.scrollHeight;
            content.style.maxHeight = contentHeight + 'px';
        }

        // Update ARIA attributes for accessibility
        const header = item.querySelector('.faq-header');
        if (header) {
            header.setAttribute('aria-expanded', 'true');
        }
    }

    closeFAQ(item) {
        const content = item.querySelector('.faq-content');
        
        // Remove active class
        item.classList.remove('active');
        
        // Reset max-height for smooth animation
        if (content) {
            content.style.maxHeight = '0px';
        }

        // Update ARIA attributes for accessibility
        const header = item.querySelector('.faq-header');
        if (header) {
            header.setAttribute('aria-expanded', 'false');
        }
    }

    setupKeyboardNavigation() {
        this.faqItems.forEach(item => {
            const header = item.querySelector('.faq-header');
            if (header) {
                // Make header focusable
                header.setAttribute('tabindex', '0');
                header.setAttribute('role', 'button');
                header.setAttribute('aria-expanded', 'false');
                
                // Add keyboard event listener
                header.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.toggleFAQ(item);
                    }
                });
            }
        });
    }

    // Method to open specific FAQ by ID
    openFAQById(id) {
        const item = document.querySelector(`[data-accordion="${id}"]`);
        if (item) {
            this.openFAQ(item);
            // Scroll to the FAQ item
            item.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }

    // Method to close all FAQs
    closeAllFAQs() {
        this.faqItems.forEach(item => {
            this.closeFAQ(item);
        });
    }
}

// Initialize FAQ accordion when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const faqAccordion = new FAQAccordion();
    
    // Make it globally accessible for external use
    window.faqAccordion = faqAccordion;
});

// Add smooth scroll behavior for FAQ links
document.addEventListener('DOMContentLoaded', () => {
    const faqLinks = document.querySelectorAll('a[href*="#faq"]');
    
    faqLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            if (href.includes('#faq-')) {
                e.preventDefault();
                const faqId = href.split('#')[1];
                const faqItem = document.querySelector(`[data-accordion="${faqId}"]`);
                
                if (faqItem) {
                    // Scroll to FAQ section first
                    faqItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    // Open the specific FAQ after a short delay
                    setTimeout(() => {
                        window.faqAccordion.openFAQById(faqId);
                    }, 500);
                }
            }
        });
    });
}); 