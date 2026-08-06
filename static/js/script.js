/**
 * Global JavaScript - Humanaid
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log('Global JavaScript loaded successfully.');

    // Initialize accordion single-open behavior
    initAccordionBehavior();

    // Ensure all external links open securely in a new tab
    const externalLinks = document.querySelectorAll('a[target="_blank"]');
    externalLinks.forEach(link => {
        if (!link.getAttribute('rel')) {
            link.setAttribute('rel', 'noopener noreferrer');
        }
    });

    // Smooth scroll behavior for internal anchor links (#sudan, etc.)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

/**
 * Single-Accordion Mode:
 * Listens for clicks on <summary> elements and closes all other open <details> tags.
 */
function initAccordionBehavior() {
    const categoriesContainer = document.getElementById('categories');
    if (!categoriesContainer) return;

    const summaries = categoriesContainer.querySelectorAll('.accordion-item > summary');

    summaries.forEach(summary => {
        summary.addEventListener('click', (e) => {
            // Prevent accordions from closing if the user clicks the "Learn More" button inside summary
            if (e.target.closest('.learn-more-btn')) {
                return;
            }

            const currentDetails = summary.parentElement;
            const allAccordions = categoriesContainer.querySelectorAll('.accordion-item');

            allAccordions.forEach(details => {
                // Close any details element that is NOT the one currently being clicked
                if (details !== currentDetails) {
                    details.removeAttribute('open');
                }
            });
        });
    });
}

/**
 * Trigger Email Client via Contact Button
 */
function handleContactClick() {
    const email = "adityakumarmishra162006@gmail.com";
    const subject = encodeURIComponent("Regarding Humanaid");
    const body = encodeURIComponent("Your Name: <INPUT YOUR NAME HERE>\n\nMessage:\n");

    window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
}
