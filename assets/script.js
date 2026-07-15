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
    var parallaxData = Array.prototype.map.call(document.querySelectorAll('[data-parallax]'), function(el){
      return { el: el, speed: parseFloat(el.getAttribute('data-parallax')) || 0.1, lastOffset: 0 };
    });
    var ticking = false;
    function updateParallax(){
      parallaxData.forEach(function(d){
        // rect.top already includes last frame's transform, so subtract it back
        // out first — otherwise each tick compounds on the previous offset and
        // the element drifts far past its intended position over a long scroll.
        var rect = d.el.getBoundingClientRect();
        var staticTop = rect.top - d.lastOffset;
        var offset = (staticTop - window.innerHeight/2) * d.speed;
        d.el.style.transform = 'translateY(' + offset + 'px)';
        d.lastOffset = offset;
      });
      ticking = false;
    }
    window.addEventListener('scroll', function(){
      if(!ticking){ requestAnimationFrame(updateParallax); ticking = true; }
    }, {passive:true});
    updateParallax();
  }

  // stat band card alignment — while .statband-pin is stuck, each card rises
  // from data-align-offset px below its resting spot, finishing at its own
  // data-align-arrive fraction of the pinned scroll. Different distances and
  // arrival points = visibly different speeds; once every card has settled
  // the aligned row holds until the section releases. Mobile CSS forces
  // transform:none, so this is desktop-only.
  var statband = document.querySelector('.statband');
  if(statband && !reduced){
    var alignCards = statband.querySelectorAll('.statcard[data-align-offset]');
    var stackTicking = false;
    function updateStatband(){
      var scrollable = statband.offsetHeight - window.innerHeight;
      if(scrollable > 0){
        var p = Math.min(1, Math.max(0, -statband.getBoundingClientRect().top / scrollable));
        alignCards.forEach(function(c){
          var start = parseFloat(c.getAttribute('data-align-offset')) || 0;
          var arrive = parseFloat(c.getAttribute('data-align-arrive')) || 0.55;
          var t = Math.min(1, p / arrive);
          t = 1 - Math.pow(1 - t, 3);
          c.style.transform = 'translateY(' + (start * (1 - t)) + 'px)';
        });
      }
      stackTicking = false;
    }
    window.addEventListener('scroll', function(){
      if(!stackTicking){ requestAnimationFrame(updateStatband); stackTicking = true; }
    }, {passive:true});
    updateStatband();
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
