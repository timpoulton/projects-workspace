document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    const modalClose = document.querySelector('.modal-close');
    const portfolioCards = document.querySelectorAll('.modal-trigger');

    // Function to open modal
    function openModal(card) {
        const caseStudyTitle = card.querySelector('.case-study-title').textContent;
        const modalData = card.querySelector('.modal-data');
        
        if (modalData) {
            // Set modal title
            modalTitle.textContent = caseStudyTitle;
            
            // Clone and insert the modal data content
            const content = modalData.cloneNode(true);
            content.style.display = 'block';
            modalBody.innerHTML = '';
            modalBody.appendChild(content);
            
            // Show modal
            modalOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }

    // Function to close modal
    function closeModal() {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => {
            modalBody.innerHTML = '';
        }, 300);
    }

    // Add click listeners to portfolio cards
    portfolioCards.forEach(card => {
        card.addEventListener('click', (e) => {
            e.preventDefault();
            openModal(card);
        });
        
        // Add keyboard support
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openModal(card);
            }
        });
        
        // Make cards focusable
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `View details for ${card.querySelector('.case-study-title').textContent}`);
    });

    // Close modal when clicking close button
    modalClose.addEventListener('click', closeModal);

    // Close modal when clicking overlay
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });
}); 