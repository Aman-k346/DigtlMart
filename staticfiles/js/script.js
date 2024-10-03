let Sidebar = document.querySelector("#Sidebar");
let Hamburger = document.querySelector(".Hamburger");
let TopMenu = document.querySelector(".TopMenu");

function ChangeHamburgerIcon(x) {
  x.classList.toggle("change");
}

// Handle Hamburger click
Hamburger.addEventListener("click", function () {
  ChangeHamburgerIcon(this);
  if (Hamburger.classList.contains("change")) {
    Sidebar.classList.add("SlideToggle");
    scrollLock.disablePageScroll();
  } else {
    Sidebar.classList.remove("SlideToggle");
    scrollLock.enablePageScroll();
  }
});

// Click detection for outside clicks
document.addEventListener("click", function (e) {
  if (!Hamburger.contains(e.target) && !TopMenu.contains(e.target)) {
    if (Hamburger.classList.contains("change")) {
      Hamburger.classList.remove("change");
      Sidebar.classList.remove("SlideToggle");
      scrollLock.enablePageScroll();
    }
  }
});

// slider initialization
document.addEventListener("DOMContentLoaded", function () {
  let splide = new Splide("#AnnouncementsBar", {
    type: "fade",
    perPage: 1,
    perMove: 1,
    pagination: false,
    autoplay: true,
    interval: 2000,
    snap: true,
    rewind: true,
  });
  splide.mount();

  let TestimonialBar = new Splide("#TestimonialBar", {
    type: "loop",
    perPage: 3,
    perMove: 1,
    pagination: false,
    autoplay: true,
    interval: 2000,
    snap: true,
    rewind: true,

    breakpoints: {
      1300: {
        perPage: 2,
      },
      600: {
        perPage: 1,
      },
    },
  });

  TestimonialBar.mount();
});

window.addEventListener("load", function () {
  let headerHeight = document.querySelector("header").offsetHeight + 25;
  console.log(headerHeight);
  TopMenu.style.paddingTop = headerHeight + "px";
});
