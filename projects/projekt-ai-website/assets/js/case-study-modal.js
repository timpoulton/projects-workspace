// Case Study Modal System - Robust Implementation
(function() {
    'use strict';
    
    let isModalOpen = false;
    let currentModal = null;
    
    function initializeModal() {
        try {
            createModalHTML();
            
            const modal = document.getElementById('case-study-modal');
            const modalTitle = document.getElementById('modal-title');
            const modalContent = document.getElementById('modal-content');
            const closeButton = document.querySelector('.modal-close');
            const portfolioCards = document.querySelectorAll('.portfolio-card');
            
            if (!modal || !modalTitle || !modalContent || !closeButton) {
                console.error('Modal elements not found');
                return;
            }
            
            currentModal = modal;
            modal.classList.add('hidden');
            document.body.style.overflow = '';
            
            portfolioCards.forEach((card, index) => {
                card.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    const caseStudyIds = [
                        'club77-content-pipeline',
                        'upwork-proposal-automation', 
                        'dj-recording-manager',
                        'manychat-guestlist-automation'
                    ];
                    
                    const caseStudyId = caseStudyIds[index];
                    if (caseStudyId) {
                        openModal(caseStudyId);
                    }
                });
                
                card.style.cursor = 'pointer';
            });
            
            closeButton.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                closeModal();
            });
            
            modal.addEventListener('click', function(e) {
                if (e.target === modal || e.target.classList.contains('modal-overlay')) {
                    closeModal();
                }
            });
            
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && isModalOpen) {
                    closeModal();
                }
            });
            
            console.log('Modal system initialized successfully');
            
        } catch (error) {
            console.error('Error initializing modal:', error);
        }
    }
    
    function createModalHTML() {
        const modalHTML = `
            <div id="case-study-modal" class="modal-overlay hidden">
                <div class="modal-container">
                    <div class="modal-header">
                        <h2 id="modal-title">Case Study Title</h2>
                        <button class="modal-close" aria-label="Close modal">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="18" y1="6" x2="6" y2="18"></line>
                                <line x1="6" y1="6" x2="18" y2="18"></line>
                            </svg>
                        </button>
                    </div>
                    <div class="modal-content" id="modal-content">
                        <!-- Content will be dynamically inserted here -->
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }
    
    const caseStudyData = {
        'club77-content-pipeline': {
            title: 'Club77 Content Pipeline',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Automated content creation pipeline for Club77, a premier nightclub venue. This comprehensive system streamlines the entire content workflow from concept to publication, reducing manual effort while maintaining high-quality output.</p>
                </div>

                <div class="modal-stats">
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">75%</div>
                        <div class="modal-stat-label">Time Savings</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">3x</div>
                        <div class="modal-stat-label">Content Output</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">24/7</div>
                        <div class="modal-stat-label">Automation</div>
                    </div>
                </div>

                <div class="modal-section">
                    <h3>Challenge</h3>
                    <p>Club77 faced significant challenges in maintaining consistent, high-quality content across multiple social media platforms while managing a busy event schedule.</p>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Implemented a comprehensive AI-powered content pipeline that automates the entire workflow from ideation to publication.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>The automated content pipeline transformed Club77's digital presence, enabling consistent high-quality content production.</p>
                </div>
            `
        },
        'upwork-proposal-automation': {
            title: 'Proposal Generator',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Advanced AI-powered proposal generation system designed for freelance professionals.</p>
                </div>

                <div class="modal-stats">
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">85%</div>
                        <div class="modal-stat-label">Efficiency Gain</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">5x</div>
                        <div class="modal-stat-label">Faster Proposals</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">95%</div>
                        <div class="modal-stat-label">Accuracy Rate</div>
                    </div>
                </div>

                <div class="modal-section">
                    <h3>Challenge</h3>
                    <p>Freelance professionals struggle with the time-intensive process of crafting unique, compelling proposals.</p>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Developed an intelligent proposal generation system that analyzes job descriptions and creates tailored proposals.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>Users experienced dramatic improvements in both efficiency and success rates.</p>
                </div>
            `
        },
        'dj-recording-manager': {
            title: 'DJ Recording Suite',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Comprehensive recording workflow optimization system for professional DJ studios.</p>
                </div>

                <div class="modal-stats">
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">68%</div>
                        <div class="modal-stat-label">Workflow Speed</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">4x</div>
                        <div class="modal-stat-label">Recording Capacity</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">100%</div>
                        <div class="modal-stat-label">Quality Maintained</div>
                    </div>
                </div>

                <div class="modal-section">
                    <h3>Challenge</h3>
                    <p>Professional DJ studios faced significant bottlenecks in their recording workflows.</p>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Implemented an intelligent recording management system that automates session configuration.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>The studio achieved significant improvements in operational efficiency.</p>
                </div>
            `
        },
        'manychat-guestlist-automation': {
            title: 'Guest List Automation',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Intelligent chatbot system designed for venue customer service and guest list management.</p>
                </div>

                <div class="modal-stats">
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">92%</div>
                        <div class="modal-stat-label">Process Automation</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">10x</div>
                        <div class="modal-stat-label">Response Speed</div>
                    </div>
                    <div class="modal-stat-card">
                        <div class="modal-stat-number">99%</div>
                        <div class="modal-stat-label">Uptime</div>
                    </div>
                </div>

                <div class="modal-section">
                    <h3>Challenge</h3>
                    <p>Venues struggled with managing high volumes of guest inquiries and reservations.</p>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Developed an intelligent chatbot system that handles guest interactions across multiple platforms.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>Venues experienced dramatic improvements in customer service efficiency and guest satisfaction.</p>
                </div>
            `
        }
    };
    
    function openModal(caseStudyId) {
        try {
            const modal = currentModal;
            const modalTitle = document.getElementById('modal-title');
            const modalContent = document.getElementById('modal-content');
            const caseStudy = caseStudyData[caseStudyId];
            
            if (!modal || !modalTitle || !modalContent || !caseStudy) {
                console.error('Cannot open modal - missing elements or data');
                return;
            }
            
            modalTitle.textContent = caseStudy.title;
            modalContent.innerHTML = caseStudy.content;
            
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
            isModalOpen = true;
            
            console.log('Modal opened:', caseStudyId);
            
        } catch (error) {
            console.error('Error opening modal:', error);
        }
    }
    
    function closeModal() {
        try {
            if (!currentModal) return;
            
            currentModal.classList.add('hidden');
            document.body.style.overflow = '';
            isModalOpen = false;
            
            console.log('Modal closed');
            
        } catch (error) {
            console.error('Error closing modal:', error);
        }
    }
    
    window.forceCloseModal = closeModal;
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initializeModal);
    } else {
        initializeModal();
    }
    
})();
