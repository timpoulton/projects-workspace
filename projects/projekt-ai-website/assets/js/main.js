document.addEventListener('DOMContentLoaded', function() {
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

    // Modal functionality
    const modalOverlay = document.getElementById('caseStudyModal');
    const modalBody = document.getElementById('modalBody');
    const modalClose = document.getElementById('closeModal');
    const portfolioCards = document.querySelectorAll('.modal-trigger');

    // Function to open modal
    function openModal(card) {
        const caseStudyTitle = card.querySelector('.case-study-title').textContent;
        const modalData = card.querySelector('.modal-data');
        
        if (modalData && modalBody) {
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
        if (modalOverlay) {
            modalOverlay.classList.remove('active');
            document.body.style.overflow = '';
            setTimeout(() => {
                if (modalBody) {
                    modalBody.innerHTML = '';
                }
            }, 300);
        }
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
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }

    // Close modal when clicking overlay
    if (modalOverlay) {
        modalOverlay.addEventListener('click', (e) => {
            if (e.target === modalOverlay) {
                closeModal();
            }
        });
    }

    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modalOverlay && modalOverlay.classList.contains('active')) {
            closeModal();
        }
    });

    // Contact form handling (if exists)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const message = document.getElementById('message').value;
            
            alert(`Thank you for your message, ${name}! We'll get back to you at ${email} soon.`);
            contactForm.reset();
        });
    }

    // Mobile menu functionality (if exists)
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking on links
        document.querySelectorAll('.mobile-menu a').forEach(link => {
            link.addEventListener('click', function() {
                if (mobileMenu) {
                    mobileMenu.classList.remove('active');
                }
            });
        });
    }

    // Button hover effects
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // FAQ functionality
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', function() {
            const answer = question.nextElementSibling;
            if (answer.style.display === 'none') {
                answer.style.display = 'block';
            } else {
                answer.style.display = 'none';
            }
        });
    });
});
