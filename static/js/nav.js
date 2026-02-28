// Highlight current page in nav
document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.hostname === location.hostname && link.pathname === location.pathname) {
        link.classList.add('active');
    }
});

const navLinks = document.querySelector('.nav-links');
const hamburger = document.querySelector('.hamburger');

if (navLinks && hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Close mobile nav when a link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });

    // Close mobile nav when clicking outside
    document.addEventListener('click', (e) => {
        if (navLinks.classList.contains('active') && !e.target.closest('nav')) {
            navLinks.classList.remove('active');
        }
    });
}
