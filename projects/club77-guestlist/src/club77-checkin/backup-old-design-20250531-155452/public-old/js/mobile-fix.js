// Mobile optimization script for Club77 Check-in System
(function() {
    'use strict';
    
    // Force mobile viewport settings
    function setMobileViewport() {
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
        }
    }
    
    // Force mobile CSS classes
    function applyMobileClasses() {
        const isMobile = window.innerWidth <= 1199; // Treat everything under 1200px as mobile/tablet
        const isTablet = window.innerWidth <= 768;
        const isSmallMobile = window.innerWidth <= 480;
        
        // Always enforce single column for mobile and tablet
        const eventsGrid = document.querySelector('.club77-events-grid');
        if (eventsGrid && isMobile) {
            eventsGrid.style.display = 'grid';
            eventsGrid.style.gridTemplateColumns = '1fr !important';
            eventsGrid.style.gap = isTablet ? '1rem' : '1.5rem';
            eventsGrid.style.width = '100%';
            eventsGrid.style.maxWidth = '100%';
            eventsGrid.style.padding = isTablet ? '1rem 0' : '1.5rem 0';
        }
        
        if (isMobile) {
            document.body.classList.add('mobile-device');
            
            // Force artwork container sizes for mobile/tablet
            const artworkContainers = document.querySelectorAll('.club77-artwork-container');
            artworkContainers.forEach(container => {
                if (isSmallMobile) {
                    container.style.height = '180px';
                    container.style.maxHeight = '180px';
                } else if (isTablet) {
                    container.style.height = '220px';
                    container.style.maxHeight = '220px';
                } else {
                    container.style.height = '250px';
                    container.style.maxHeight = '250px';
                }
                container.style.width = '100%';
            });
            
            // Force text sizes
            const eventTitles = document.querySelectorAll('.club77-event-title');
            eventTitles.forEach(title => {
                title.style.fontSize = isSmallMobile ? '0.95rem' : '1rem';
                title.style.lineHeight = '1.2';
                title.style.marginBottom = '0.75rem';
            });
            
            const metaItems = document.querySelectorAll('.club77-meta-item');
            metaItems.forEach(item => {
                item.style.fontSize = isSmallMobile ? '0.8rem' : '0.875rem';
                item.style.marginBottom = '0.5rem';
            });
            
            const descriptions = document.querySelectorAll('.club77-event-description');
            descriptions.forEach(desc => {
                desc.style.fontSize = isSmallMobile ? '0.8rem' : '0.875rem';
                desc.style.lineHeight = '1.4';
            });
            
            const actionBtns = document.querySelectorAll('.club77-action-btn');
            actionBtns.forEach(btn => {
                btn.style.fontSize = '0.8rem';
                btn.style.padding = '0.625rem 1rem';
            });
            
            // Force padding
            const paddingGlobals = document.querySelectorAll('.padding-global');
            paddingGlobals.forEach(element => {
                element.style.paddingLeft = isSmallMobile ? '0.75rem' : '1rem';
                element.style.paddingRight = isSmallMobile ? '0.75rem' : '1rem';
            });
        }
    }
    
    // Prevent zoom on input focus (mobile Safari)
    function preventZoom() {
        const inputs = document.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                if (window.innerWidth <= 768) {
                    this.style.fontSize = '16px';
                }
            });
        });
    }
    
    // Force repaint to ensure CSS changes take effect
    function forceRepaint() {
        document.body.style.display = 'none';
        document.body.offsetHeight; // Trigger reflow
        document.body.style.display = '';
    }
    
    // Initialize mobile fixes
    function init() {
        setMobileViewport();
        applyMobileClasses();
        preventZoom();
        
        // Apply fixes on resize
        let resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function() {
                applyMobileClasses();
            }, 250);
        });
        
        // Force repaint after a short delay
        setTimeout(forceRepaint, 100);
    }
    
    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Also run on window load as backup
    window.addEventListener('load', init);
    
})(); 