(function(){
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, {threshold:0.15, rootMargin:'0px 0px -60px 0px'});
  document.querySelectorAll('.reveal, .reveal-stagger').forEach(function(el){ io.observe(el); });

  if(!reduced){
    var parallaxEls = document.querySelectorAll('[data-parallax]');
    var ticking = false;
    function updateParallax(){
      parallaxEls.forEach(function(el){
        var speed = parseFloat(el.getAttribute('data-parallax')) || 0.1;
        var rect = el.getBoundingClientRect();
        var offset = (rect.top - window.innerHeight/2) * speed;
        el.style.transform = 'translateY(' + offset + 'px)';
      });
      ticking = false;
    }
    window.addEventListener('scroll', function(){
      if(!ticking){ requestAnimationFrame(updateParallax); ticking = true; }
    }, {passive:true});
    updateParallax();
  }

  var contactForm = document.getElementById('contact-form');
  if(contactForm){
    contactForm.addEventListener('submit', function(e){
      e.preventDefault();
      var success = document.getElementById('form-success');
      if(success){ success.classList.add('visible'); }
      contactForm.reset();
    });
  }
})();
