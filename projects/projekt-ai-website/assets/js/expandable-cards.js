(function() {
    'use strict';
    
    console.log('Expandable Cards: Script loaded');
    
    function initializeExpandableCards() {
        console.log('Expandable Cards: Initializing...');
        const expandableCards = document.querySelectorAll('.expandable-card');
        console.log('Expandable Cards: Found', expandableCards.length, 'cards');
        
        expandableCards.forEach((card, index) => {
            const expandButton = card.querySelector('.expand-button');
            const expandableContent = card.querySelector('.expandable-content');
            const expandText = card.querySelector('.expand-text');
            const expandIcon = card.querySelector('.expand-icon');
            
            console.log(`Card ${index}:`, {
                button: !!expandButton,
                content: !!expandableContent,
                text: !!expandText,
                icon: !!expandIcon
            });
            
            if (!expandButton || !expandableContent || !expandText || !expandIcon) {
                console.warn('Expandable card missing required elements:', {
                    button: !!expandButton,
                    content: !!expandableContent,
                    text: !!expandText,
                    icon: !!expandIcon
                });
                return;
            }
            
            // Initially hide the expandable content
            expandableContent.style.display = 'none';
            console.log(`Card ${index}: Content hidden initially`);
            
            expandButton.addEventListener('click', function(e) {
                console.log(`Card ${index}: Button clicked!`);
                e.preventDefault();
                e.stopPropagation();
                
                const isExpanded = card.getAttribute('data-expanded') === 'true';
                console.log(`Card ${index}: Current state - expanded:`, isExpanded);
                
                if (isExpanded) {
                    // Collapse the card
                    console.log(`Card ${index}: Collapsing`);
                    expandableContent.style.display = 'none';
                    card.setAttribute('data-expanded', 'false');
                    expandText.textContent = 'View Details';
                    expandIcon.style.transform = 'rotate(0deg)';
                    card.classList.remove('expanded');
                } else {
                    // Expand the card
                    console.log(`Card ${index}: Expanding`);
                    expandableContent.style.display = 'block';
                    card.setAttribute('data-expanded', 'true');
                    expandText.textContent = 'Hide Details';
                    expandIcon.style.transform = 'rotate(180deg)';
                    card.classList.add('expanded');
                    
                    // Smooth scroll to show the expanded content
                    setTimeout(() => {
                        expandableContent.scrollIntoView({
                            behavior: 'smooth',
                            block: 'nearest'
                        });
                    }, 100);
                }
            });
            
            console.log(`Card ${index}: Event listener attached`);
        });
        
        console.log('Expandable Cards: Initialization complete');
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        console.log('Expandable Cards: DOM still loading, waiting...');
        document.addEventListener('DOMContentLoaded', initializeExpandableCards);
    } else {
        console.log('Expandable Cards: DOM already loaded, initializing immediately');
        initializeExpandableCards();
    }
})(); 