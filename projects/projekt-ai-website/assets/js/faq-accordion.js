/**
 * FAQ Accordion JavaScript - Simplified & Reliable
 * Handles the accordion functionality for FAQ sections
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('FAQ Accordion: DOM loaded, initializing...');
    
    // Find all FAQ items
    const faqItems = document.querySelectorAll('.faq-item');
    console.log('FAQ Accordion: Found', faqItems.length, 'FAQ items');
    
    if (faqItems.length === 0) {
        console.warn('FAQ Accordion: No FAQ items found!');
        return;
    }
    
    // Add click event listeners to each FAQ item
    faqItems.forEach((item, index) => {
        const header = item.querySelector('.faq-header');
        const content = item.querySelector('.faq-content');
        const answer = item.querySelector('.faq-answer');
        
        if (!header || !content || !answer) {
            console.warn('FAQ Accordion: Missing elements in FAQ item', index);
            return;
        }
        
        // Make header focusable and add accessibility attributes
        header.setAttribute('tabindex', '0');
        header.setAttribute('role', 'button');
        header.setAttribute('aria-expanded', 'false');
        
        // Add click event listener
        header.addEventListener('click', function() {
            console.log('FAQ Accordion: Clicked item', index);
            toggleFAQ(item, content, answer, header);
        });
        
        // Add keyboard event listener
        header.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                console.log('FAQ Accordion: Keyboard activated item', index);
                toggleFAQ(item, content, answer, header);
            }
        });
        
        console.log('FAQ Accordion: Initialized item', index);
    });
    
    function toggleFAQ(item, content, answer, header) {
        const isActive = item.classList.contains('active');
        
        // Close all other FAQ items (accordion behavior)
        faqItems.forEach(otherItem => {
            if (otherItem !== item && otherItem.classList.contains('active')) {
                closeFAQ(otherItem);
            }
        });
        
        // Toggle the clicked item
        if (isActive) {
            closeFAQ(item);
        } else {
            openFAQ(item, content, answer, header);
        }
    }
    
    function openFAQ(item, content, answer, header) {
        console.log('FAQ Accordion: Opening FAQ');
        
        // Add active class
        item.classList.add('active');
        
        // Set proper max-height for smooth animation
        const contentHeight = answer.scrollHeight + 64; // Add padding
        content.style.maxHeight = contentHeight + 'px';
        
        // Update ARIA attributes
        header.setAttribute('aria-expanded', 'true');
    }
    
    function closeFAQ(item) {
        console.log('FAQ Accordion: Closing FAQ');
        
        const content = item.querySelector('.faq-content');
        const header = item.querySelector('.faq-header');
        
        // Remove active class
        item.classList.remove('active');
        
        // Reset max-height for smooth animation
        if (content) {
            content.style.maxHeight = '0px';
        }
        
        // Update ARIA attributes
        if (header) {
            header.setAttribute('aria-expanded', 'false');
        }
    }
    
    console.log('FAQ Accordion: Initialization complete!');
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