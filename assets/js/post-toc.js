(function () {
  function initScrollspy() {
    var toc = document.querySelector(".post-toc");
    if (!toc) return;

    var tocLinks = Array.from(toc.querySelectorAll(".post-toc-link"));
    if (!tocLinks.length) return;

    var linkMap = new Map();
    tocLinks.forEach(function (link) {
      var href = link.getAttribute("href");
      if (href && href.startsWith("#")) {
        try {
          var id = decodeURIComponent(href.slice(1));
          var target = document.getElementById(id);
          if (target) {
            linkMap.set(target, link);
          }
        } catch (e) {
          // ignore malformed URI components
        }
      }
    });

    var headings = Array.from(linkMap.keys());
    if (!headings.length) return;

    var activeLink = null;
    var stickyContainer = document.querySelector(".post-sidebar-sticky");

    function setActive(link) {
      if (activeLink === link) return;
      if (activeLink) {
        activeLink.classList.remove("is-active");
      }
      activeLink = link;
      if (activeLink) {
        activeLink.classList.add("is-active");
        if (stickyContainer && stickyContainer.scrollHeight > stickyContainer.clientHeight) {
          var activeRect = activeLink.getBoundingClientRect();
          var containerRect = stickyContainer.getBoundingClientRect();
          if (activeRect.top < containerRect.top || activeRect.bottom > containerRect.bottom) {
            activeLink.scrollIntoView({ block: "nearest", behavior: "smooth" });
          }
        }
      }
    }

    var ticking = false;
    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(function () {
          updateActive();
          ticking = false;
        });
        ticking = true;
      }
    }

    function updateActive() {
      // Offset from top of viewport to consider a section "active"
      var headerOffset = 120;
      var scrollY = window.scrollY || window.pageYOffset;
      var docHeight = document.documentElement.scrollHeight;
      var winHeight = window.innerHeight;

      // If scrolled near the bottom of the page, activate the last heading
      if (scrollY + winHeight >= docHeight - 50) {
        var lastHeading = headings[headings.length - 1];
        setActive(linkMap.get(lastHeading));
        return;
      }

      var current = headings[0];
      for (var i = 0; i < headings.length; i++) {
        var heading = headings[i];
        var top = heading.getBoundingClientRect().top;
        if (top <= headerOffset) {
          current = heading;
        } else {
          break;
        }
      }

      if (current) {
        setActive(linkMap.get(current));
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll, { passive: true });
    updateActive();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initScrollspy);
  } else {
    initScrollspy();
  }
})();
