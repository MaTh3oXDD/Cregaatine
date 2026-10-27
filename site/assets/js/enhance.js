(function () {
  var header = document.getElementById("main-header");
  var onScroll = function () {
    if (!header) return;
    header.classList.toggle("enh-scrolled", window.scrollY > 8);
  };
  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var setHeaderHeightVar = function () {
    if (!header) return;
    document.documentElement.style.setProperty("--enh-header-h", header.offsetHeight + "px");
  };
  setHeaderHeightVar();
  window.addEventListener("resize", setHeaderHeightVar);
  if ("ResizeObserver" in window && header) {
    new ResizeObserver(setHeaderHeightVar).observe(header);
  }

  var prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Smooth-scroll in-page anchors.
  //
  // The previous same-page test compared a.pathname to location.pathname.
  // The nav links are written as "/#sklad" (pathname "/") while the page
  // is actually served as "/index.html" (pathname "/index.html"), so the
  // test never matched and every nav click fell through to a hard jump.
  // The reliable test is simply: does an element with that id exist here?
  //
  // Scrolling also has to clear the sticky header, otherwise the target
  // heading lands underneath it.
  var headerEl = header;
  var scrollToTarget = function (target) {
    var headerH = headerEl ? headerEl.offsetHeight : 0;
    var top = window.pageYOffset + target.getBoundingClientRect().top - headerH - 16;
    window.scrollTo({
      top: top < 0 ? 0 : top,
      behavior: prefersReduced ? "auto" : "smooth"
    });
  };

  document.querySelectorAll('a[href*="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var hash = a.hash;
      if (!hash || hash === "#") return;

      var target;
      try {
        target = document.querySelector(hash);
      } catch (err) {
        return; // not a valid selector, let the browser deal with it
      }
      if (!target) return; // anchor lives on another page

      e.preventDefault();
      scrollToTarget(target);
      if (history.replaceState) history.replaceState(null, "", hash);
    });
  });

  // Landing on the page with a hash already in the URL (e.g. clicking
  // "Skład" from the Nagrody subpage).
  //
  // The browser jumps to the anchor as soon as it parses the element,
  // but images and the carousels above it are still resolving, so the
  // content grows underneath and the anchor slides away — which reads
  // as "it threw me to the top, then jumped to the section once
  // everything loaded".
  //
  // Fix: hold the target and re-assert its position as the layout
  // settles, instantly (never animated — animating this is the part
  // that looks like a glitch), and stop as soon as it holds still.
  if (location.hash && location.hash.length > 1) {
    var initialTarget = null;
    try {
      initialTarget = document.querySelector(location.hash);
    } catch (err) {
      initialTarget = null;
    }

    if (initialTarget) {
      var settleUntil = Date.now() + 3000;
      var lastTop = -1;

      var holdAnchor = function () {
        var headerH = headerEl ? headerEl.offsetHeight : 0;
        var top = window.pageYOffset + initialTarget.getBoundingClientRect().top - headerH - 16;
        if (top < 0) top = 0;

        // only correct when the target actually moved
        if (Math.abs(top - lastTop) > 2) {
          window.scrollTo(0, top);
          lastTop = top;
        }
        if (Date.now() < settleUntil) requestAnimationFrame(holdAnchor);
      };

      // start immediately rather than waiting for the full load event
      holdAnchor();
      document.addEventListener("DOMContentLoaded", holdAnchor);
      window.addEventListener("load", function () {
        settleUntil = Date.now() + 400;
        holdAnchor();
      });
    }
  }

  // Certificate rail: the arrows only exist when the rail overflows.
  // On a wide screen all four badges fit, and a pair of dead arrows
  // would be lying about there being more to see.
  var certRail = document.querySelector(".cert-rail");
  var certNav = document.querySelector(".cert-nav");
  if (certRail && certNav) {
    var certBtns = certNav.querySelectorAll("[data-cert-dir]");
    var certStep = function () {
      var card = certRail.querySelector(".et_pb_column");
      var gap = parseFloat(getComputedStyle(certRail).columnGap) || 0;
      return card ? card.getBoundingClientRect().width + gap : certRail.clientWidth * 0.8;
    };

    var syncCertNav = function () {
      var overflow = certRail.scrollWidth - certRail.clientWidth;
      certNav.hidden = overflow < 4;
      if (certNav.hidden) return;
      certBtns.forEach(function (btn) {
        var dir = Number(btn.getAttribute("data-cert-dir"));
        btn.disabled = dir < 0
          ? certRail.scrollLeft < 4
          : certRail.scrollLeft > overflow - 4;
      });
    };

    certBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        certRail.scrollBy({
          left: Number(btn.getAttribute("data-cert-dir")) * certStep(),
          behavior: prefersReduced ? "auto" : "smooth"
        });
      });
    });

    certRail.addEventListener("scroll", syncCertNav, { passive: true });
    window.addEventListener("resize", syncCertNav);
    window.addEventListener("load", syncCertNav);
    syncCertNav();
  }

  // The testimonial track autoplays now; reduced-motion users get it
  // parked. The plugin has no setting for that, so stop the Swiper
  // instance once it has booted.
  if (prefersReduced) {
    var parkAutoplay = function () {
      document.querySelectorAll(".dica_divi_carousel .swiper-container").forEach(function (el) {
        if (el.swiper && el.swiper.autoplay) el.swiper.autoplay.stop();
      });
    };
    window.addEventListener("load", parkAutoplay);
    setTimeout(parkAutoplay, 1200);
  }

  // Every link to carno-med.pl leaves the CreGAAtine site for the
  // Carnomed shop, a different domain with a different look. The dialog
  // says so in the shop's own visual language (bridge.css), counts down
  // three seconds and then goes. "Przejdź teraz" skips the wait, "Zostań"
  // and Esc cancel it. Modifier clicks (new tab, new window) go straight
  // through.
  var SHOP_DELAY = 3;
  var shopDialog = null;
  var shopTimer = null;

  // The script's own URL carries the GitHub Pages prefix (/Cregaatine/demo)
  // when there is one, so asset paths are built from it.
  var scriptEl = document.getElementById("enhance-js");
  var assetBase = scriptEl
    ? scriptEl.src.replace(/\/assets\/js\/enhance\.js.*$/, "/assets/")
    : "/assets/";

  var stopShopTimer = function () {
    clearInterval(shopTimer);
    shopTimer = null;
  };

  var buildShopDialog = function () {
    // Montserrat is the Carnomed typeface. Only the dialog needs it, so it
    // loads with the dialog, not with the page.
    var font = document.createElement("link");
    font.rel = "stylesheet";
    font.href = "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;800&display=swap";
    document.head.appendChild(font);

    var d = document.createElement("dialog");
    d.className = "cm-leave";
    d.setAttribute("aria-labelledby", "cm-leave-title");
    d.setAttribute("aria-describedby", "cm-leave-text");
    d.style.setProperty("--cml-delay", SHOP_DELAY + "s");
    d.innerHTML =
      '<div class="cm-leave__sheet">' +
      '<img class="cm-leave__mark" src="' + assetBase + 'img/carnomed-logo.svg" alt="Carnomed" width="210" height="43">' +
      '<span class="cm-leave__rule" aria-hidden="true"></span>' +
      '<h2 class="cm-leave__title" id="cm-leave-title">Przechodzisz do sklepu Carnomed</h2>' +
      '<p class="cm-leave__text" id="cm-leave-text">Zostaniesz przeniesiony do naszego zewnętrznego sklepu. ' +
      'Zamówienie przyjmuje Carnomed sp. z o.o., wyłączny dystrybutor CreGAAtine w Polsce.</p>' +
      '<p class="cm-leave__host"></p>' +
      '<p class="cm-leave__count" aria-live="polite"></p>' +
      '<div class="cm-leave__actions">' +
      '<a class="cm-leave__go" href="#">Przejdź teraz</a>' +
      '<button type="button" class="cm-leave__stay">Zostań na stronie CreGAAtine</button>' +
      '</div>' +
      '</div>' +
      '<div class="cm-leave__band" aria-hidden="true"><span></span></div>';
    document.body.appendChild(d);

    d.querySelector(".cm-leave__stay").addEventListener("click", function () { d.close(); });
    // a click on the backdrop lands on the dialog element itself
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
    d.addEventListener("close", function () {
      stopShopTimer();
      d.classList.remove("is-counting");
    });
    return d;
  };

  var renderCount = function (el, left) {
    el.innerHTML = left > 0
      ? "Przekierowanie za <b>" + left + "</b> s"
      : "Przekierowuję…";
  };

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0) return;
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    // carno-med.pl on the production site; the Carnomed copy on GitHub
    // Pages (math3oxdd.github.io/carnomed/) in the demo, see build_pages.py
    var a = e.target.closest && e.target.closest('a[href*="carno-med.pl"], a[href*="/carnomed/"]');
    if (!a || a.closest(".cm-leave")) return;
    var isCarnomed = /(^|\.)carno-med\.pl$/.test(a.hostname) ||
      (a.hostname === "math3oxdd.github.io" && a.pathname.indexOf("/carnomed/") === 0);
    if (!isCarnomed) return;
    if (typeof HTMLDialogElement === "undefined") return;

    e.preventDefault();
    shopDialog = shopDialog || buildShopDialog();
    var href = a.href;
    var go = shopDialog.querySelector(".cm-leave__go");
    var count = shopDialog.querySelector(".cm-leave__count");
    go.href = href;
    shopDialog.querySelector(".cm-leave__host").textContent =
      a.hostname === "math3oxdd.github.io" ? a.hostname + "/carnomed" : a.hostname;

    // restart the band from full on every opening
    shopDialog.classList.remove("is-counting");
    void shopDialog.offsetWidth;
    shopDialog.classList.add("is-counting");

    var left = SHOP_DELAY;
    renderCount(count, left);
    stopShopTimer();
    shopTimer = setInterval(function () {
      left -= 1;
      renderCount(count, left);
      if (left <= 0) {
        stopShopTimer();
        window.location.assign(href);
      }
    }, 1000);

    shopDialog.showModal();
    go.focus();
  });

  if (prefersReduced) return;

  var targets = document.querySelectorAll(
    "#main-content .et_pb_section, #main-content .et_pb_row, #main-content .et_pb_module"
  );
  var seen = new Set();
  var candidates = [];
  targets.forEach(function (el) {
    if (el.closest(".dica_divi_carousel")) return;
    if (el.closest(".et_pb_section_parallax")) return; /* transform here breaks Divi's fixed-position parallax and can trap scroll */
    if (candidates.length && candidates[candidates.length - 1].contains(el)) return;
    candidates.push(el);
  });
  candidates.slice(0, 400).forEach(function (el, i) {
    el.classList.add("enh-reveal");
    el.classList.add("enh-stagger-" + ((i % 5) + 1));
  });

  if (!("IntersectionObserver" in window)) {
    candidates.forEach(function (el) { el.classList.add("enh-visible"); });
    return;
  }
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("enh-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
  );
  candidates.forEach(function (el) { io.observe(el); });
})();
