const jcb = document.querySelector(".jcb");
const text = document.querySelector(".text");

const word = "MAINTAINENCE";
text.textContent = "";
word.split("").forEach((letter, id) => {
    const span = document.createElement("span");
    span.textContent = letter;
    span.style.display = "inline-block";
    span.id = `anim-${id}`;
    text.appendChild(span);
});

gsap.from("span", {
    duration: .5,
    y: 100,
    opacity: 0,
    stagger: 0.2,
    ease: "power2.out"
})


gsap.from(jcb, {
    duration: 3,
    opacity: 0,
    x: 400,
    repeat: -1,
    yoyo: true,
    ease: "power2.out"
});