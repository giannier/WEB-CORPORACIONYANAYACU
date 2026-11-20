/* Home hero: slideshow crossfade (replaces Elementor's slideshow JS) + accessible video modal. */
(function () {
  var slides = document.querySelectorAll('.yy-hero__slide');
  if (slides.length > 1) {
    var current = 0;
    setInterval(function () {
      slides[current].classList.remove('is-active');
      current = (current + 1) % slides.length;
      var next = slides[current];
      next.classList.remove('is-active');
      void next.offsetWidth; // restart the Ken Burns animation
      next.classList.add('is-active');
    }, 5000);
  }

  var modal = document.getElementById('yy-video');
  if (!modal) return;
  var video = modal.querySelector('video');
  var lastFocus = null;

  function open(e) {
    e.preventDefault();
    lastFocus = document.activeElement;
    modal.hidden = false;
    video.play().catch(function () {});
    modal.querySelector('.yy-modal__close').focus();
  }
  function close() {
    modal.hidden = true;
    video.pause();
    if (lastFocus) lastFocus.focus();
  }
  document.querySelectorAll('[data-yy-video-open]').forEach(function (el) { el.addEventListener('click', open); });
  modal.querySelectorAll('[data-yy-video-close]').forEach(function (el) { el.addEventListener('click', close); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) close(); });
})();
