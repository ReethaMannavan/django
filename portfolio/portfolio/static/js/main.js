// Animate skill bars
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.progress-bar').forEach(function(bar) {
    let width = bar.dataset.width;
    setTimeout(() => {
      bar.style.width = width + '%';
    }, 200);
  });
});
