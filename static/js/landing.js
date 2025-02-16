let lenis;
gsap.registerPlugin(ScrollTrigger);

// Initialize Lenis
addEventListener("DOMContentLoaded", function () {
  // Initialize a new Lenis instance for smooth scrolling
  const lenis = new Lenis();

  // Synchronize Lenis scrolling with GSAP's ScrollTrigger plugin
  lenis.on("scroll", ScrollTrigger.update);

  // Add Lenis's requestAnimationFrame (raf) method to GSAP's ticker
  // This ensures Lenis's smooth scroll animation updates on each GSAP tick
  gsap.ticker.add((time) => {
    lenis.raf(time * 1000); // Convert time from seconds to milliseconds
  });

  // Disable lag smoothing in GSAP to prevent any delay in scroll animations
  gsap.ticker.lagSmoothing(0);

  gsapAnimation();
});



function gsapAnimation() {
  const tl = gsap.timeline();

  tl.from(
    ".hero-anim",
    {
      duration: 1,
      x: -100,
      opacity: 0,
      stagger: 0.2,
      ease: "power2.out",
    },
    "same"
  );

  tl.from(
    ".hero-anim2",
    {
      duration: 1,
      x: 100,
      opacity: 0,
      stagger: 0.2,
      ease: "power2.out",
    },
    "same"
  );

  gsap.from(".ticker-anim", {
    scrollTrigger: {
      trigger: ".ticker-anim",
      start: "top 90%",
      end: "bottom 50%",
      toggleActions: "play none none none",
    },
    x: 500,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out",
  })

  gsap.from(".test-anim-img", {
    scrollTrigger: {
      trigger: ".test-anim",
      start: "top 90%",
      end: "bottom 50%",
      marks: true,
      scrub: 2,
    },
    x: -500,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out",
    
  })

  gsap.from(".test-anim", {
    scrollTrigger: {
      trigger: ".test-anim",
      start: "top 90%",
      end: "bottom 50%",
      scrub: 2,
    },
    x: 500,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out",
  })

  gsap.from(".why-anim", {
    scrollTrigger: {
      trigger: ".why-anim",
      start: "top 90%",
      end: "bottom 50%",
     
    },
    x: 500,
    duration:1,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out",
  })

  gsap.from(".why-anim2", {
    scrollTrigger: {
      trigger: ".why-anim2",
      start: "top 90%",
      end: "bottom 50%",
    },
    x: 700,
    duration: 1,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out",
  });

}
