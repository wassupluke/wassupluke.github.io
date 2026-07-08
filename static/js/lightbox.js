// Dependency-free lightbox for the photography gallery.
(function () {
    const thumbs = Array.from(document.querySelectorAll('.gallery-item img'));
    if (!thumbs.length) return;

    const overlay = document.createElement('div');
    overlay.className = 'lightbox';
    overlay.innerHTML =
        '<button class="lightbox-close" aria-label="Close">&times;</button>' +
        '<button class="lightbox-prev" aria-label="Previous photo">&#8249;</button>' +
        '<img alt="">' +
        '<button class="lightbox-next" aria-label="Next photo">&#8250;</button>';
    document.body.appendChild(overlay);

    const fullImg = overlay.querySelector('img');
    let index = 0;

    function show(i) {
        index = (i + thumbs.length) % thumbs.length;
        fullImg.src = thumbs[index].src;
        fullImg.alt = thumbs[index].alt;
        overlay.classList.add('open');
        document.body.style.overflow = 'hidden';
    }

    function close() {
        overlay.classList.remove('open');
        fullImg.removeAttribute('src');
        document.body.style.overflow = '';
    }

    thumbs.forEach((img, i) => {
        img.style.cursor = 'zoom-in';
        img.addEventListener('click', () => show(i));
    });

    overlay.addEventListener('click', (e) => {
        if (e.target === overlay || e.target.classList.contains('lightbox-close')) close();
    });
    overlay.querySelector('.lightbox-prev').addEventListener('click', () => show(index - 1));
    overlay.querySelector('.lightbox-next').addEventListener('click', () => show(index + 1));

    document.addEventListener('keydown', (e) => {
        if (!overlay.classList.contains('open')) return;
        if (e.key === 'Escape') close();
        if (e.key === 'ArrowLeft') show(index - 1);
        if (e.key === 'ArrowRight') show(index + 1);
    });
})();
