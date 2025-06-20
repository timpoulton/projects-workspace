// Case Study Modal Functionality
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('case-study-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    const closeButton = document.querySelector('.modal-close');
    const portfolioCards = document.querySelectorAll('.portfolio-card');
    
    // Force close any open modals and ensure modal starts hidden
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = ''; // Restore scrolling immediately
    }
    
    // Emergency close function - can be called from console if needed
    window.forceCloseModal = function() {
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = '';
        }
    };

    // Case study data with Lorem ipsum placeholder content
    const caseStudyData = {
        'club77-content-pipeline': {
            title: 'Club77 Content Pipeline',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
                    <p>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
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
                    <p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</p>
                    <ul>
                        <li>Lorem ipsum dolor sit amet consectetur</li>
                        <li>Adipiscing elit sed do eiusmod tempor</li>
                        <li>Incididunt ut labore et dolore magna</li>
                        <li>Aliqua ut enim ad minim veniam</li>
                    </ul>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet.</p>
                    <p>Consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident.</p>
                    <p>Similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio nam libero tempore.</p>
                </div>
            `
        },
        'upwork-proposal-automation': {
            title: 'Proposal Generator',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae.</p>
                    <p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin eget tortor risus. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus.</p>
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
                    <p>Donec rutrum congue leo eget malesuada. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus. Cras ultricies ligula sed magna dictum porta.</p>
                    <ul>
                        <li>Vestibulum ac diam sit amet quam vehicula</li>
                        <li>Elementum sed sit amet dui proin eget</li>
                        <li>Tortor risus dapibus augue vel accumsan</li>
                        <li>Tellus mauris a diam maecenas sed enim</li>
                    </ul>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Mauris blandit aliquet elit, eget tincidunt nibh pulvinar a.</p>
                    <p>Sed porttitor lectus nibh. Donec sollicitudin molestie malesuada. Nulla quis lorem ut libero malesuada feugiat. Curabitur aliquet quam id dui posuere blandit.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>Quisque velit nisi, pretium ut lacinia in, elementum id enim. Donec rutrum congue leo eget malesuada. Vivamus suscipit tortor eget felis porttitor volutpat.</p>
                    <p>Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet ligula.</p>
                </div>
            `
        },
        'dj-recording-manager': {
            title: 'DJ Recording Suite',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.</p>
                    <p>Nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident.</p>
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
                    <p>Sunt in culpa qui officia deserunt mollit anim id est laborum. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.</p>
                    <ul>
                        <li>Totam rem aperiam eaque ipsa quae</li>
                        <li>Ab illo inventore veritatis et quasi</li>
                        <li>Architecto beatae vitae dicta sunt</li>
                        <li>Explicabo nemo enim ipsam voluptatem</li>
                    </ul>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est.</p>
                    <p>Qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur.</p>
                    <p>Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur.</p>
                </div>
            `
        },
        'manychat-guestlist-automation': {
            title: 'Guest List Automation',
            content: `
                <div class="modal-section">
                    <h3>Project Overview</h3>
                    <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus lacinia odio vitae vestibulum. Donec auctor blandit quam. Vestibulum ante ipsum primis in faucibus orci luctus.</p>
                    <p>Et ultrices posuere cubilia curae; Mauris viverra venenenatis lorem, at elementum diam luctus vel. Maecenas tristique lacus sed nisi varius vehicula et in nisl.</p>
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
                    <p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Vestibulum tortor quam, feugiat vitae, ultricies eget, tempor sit amet.</p>
                    <ul>
                        <li>Ante donec eu libero sit amet quam</li>
                        <li>Egestas semper aenean ultricies mi</li>
                        <li>Vitae congue mauris rhoncus aenean</li>
                        <li>Vel elit scelerisque mauris pellentesque</li>
                    </ul>
                </div>

                <div class="modal-section">
                    <h3>Solution</h3>
                    <p>Pulvinar elementum integer enim neque volutpat ac tincidunt vitae semper. Quis viverra nibh cras pulvinar mattis nunc sed blandit libero volutpat.</p>
                    <p>Sed vulputate mi sit amet mauris commodo quis imperdiet massa tincidunt. Nunc congue nisi vitae suscipit tellus mauris a diam maecenas sed enim ut sem.</p>
                </div>

                <div class="modal-section">
                    <h3>Results</h3>
                    <p>Viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue.</p>
                    <p>Eget arcu dictum varius duis at consectetur lorem donec massa sapien faucibus et molestie ac feugiat sed lectus vestibulum mattis ullamcorper velit sed.</p>
                </div>
            `
        }
    };

    // Add click event listeners to portfolio cards
    portfolioCards.forEach(card => {
        card.addEventListener('click', function() {
            const caseStudyId = this.getAttribute('data-case-study');
            const caseStudy = caseStudyData[caseStudyId];
            
            if (caseStudy && modal && modalTitle && modalContent) {
                modalTitle.textContent = caseStudy.title;
                modalContent.innerHTML = caseStudy.content;
                modal.classList.remove('hidden');
                document.body.style.overflow = 'hidden'; // Prevent background scrolling
            }
        });
    });

    // Close modal functionality
    function closeModal() {
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = ''; // Restore scrolling
        }
    }

    // Close button click
    if (closeButton) {
        closeButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            closeModal();
        });
    }

    // Close on overlay click (clicking outside the modal content)
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal || e.target.classList.contains('modal-overlay')) {
                closeModal();
            }
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });
}); 