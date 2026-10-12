/* JMC Fitness — progressive enhancement only.
   No cookies, no localStorage, no analytics, no third-party requests. */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  /* ---------- Kinetic headline: split into characters ----------
     The readable text stays in a visually-hidden span for screen readers;
     the animated copy is aria-hidden. */
  document.querySelectorAll(".kinetic").forEach(function (el) {
    var i = 0;
    el.querySelectorAll(".line").forEach(function (line, lineIndex) {
      var text = line.textContent;
      var sr = document.createElement("span");
      sr.className = "visually-hidden";
      sr.textContent = text + " ";
      var visual = document.createElement("span");
      visual.setAttribute("aria-hidden", "true");
      line.style.setProperty("--line-delay", lineIndex * 300 + "ms");
      Array.prototype.forEach.call(text, function (ch) {
        var s = document.createElement("span");
        s.className = "char";
        s.style.setProperty("--i", i++);
        s.textContent = ch === " " ? " " : ch;
        visual.appendChild(s);
      });
      line.textContent = "";
      line.appendChild(sr);
      line.appendChild(visual);
    });
  });

  /* ---------- Rotating word ---------- */
  document.querySelectorAll(".rotator").forEach(function (rot) {
    var words = rot.querySelectorAll("span");
    if (!words.length) return;
    var idx = 0;
    words[0].classList.add("is-active");
    if (reduceMotion || words.length < 2) return;
    setInterval(function () {
      var current = words[idx];
      current.classList.remove("is-active");
      current.classList.add("is-leaving");
      setTimeout(function () { current.classList.remove("is-leaving"); }, 900);
      idx = (idx + 1) % words.length;
      words[idx].classList.add("is-active");
    }, 4000);
  });

  /* ---------- Scroll reveal ---------- */
  var revealEls = document.querySelectorAll(".reveal, .reveal-stagger");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-visible"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Marquee pause / play (WCAG 2.2.2) ---------- */
  var marquee = document.querySelector(".marquee");
  var mToggle = document.querySelector(".marquee-toggle");
  if (marquee && mToggle) {
    mToggle.addEventListener("click", function () {
      var paused = marquee.classList.toggle("is-paused");
      mToggle.setAttribute("aria-pressed", String(paused));
      mToggle.textContent = paused ? "Play animation" : "Pause animation";
    });
  }

  /* ---------- Enquiry form ----------
     Nothing is sent to a server. On submit the visitor's own email app opens
     with a pre-filled message to JMC Fitness, so no data is stored by this site. */
  var form = document.getElementById("enquiry-form");
  if (form) {
    var status = document.getElementById("form-status");
    form.noValidate = true; // use the accessible error messages below instead of browser bubbles

    // "Enquire about ..." buttons pre-select the matching plan
    document.querySelectorAll("[data-plan]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var radio = form.querySelector('input[name="plan"][value="' + btn.getAttribute("data-plan") + '"]');
        if (radio) radio.checked = true;
      });
    });

    function setError(input, msgId, message) {
      var msg = document.getElementById(msgId);
      if (message) {
        input.setAttribute("aria-invalid", "true");
        msg.textContent = message;
      } else {
        input.removeAttribute("aria-invalid");
        msg.textContent = "";
      }
      return !message;
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.elements["name"];
      var email = form.elements["email"];
      var plan = form.querySelector('input[name="plan"]:checked');
      var planFirst = form.querySelector('input[name="plan"]');
      var planSet = document.getElementById("plan-fieldset");
      var age = form.elements["age"];
      var consent = form.elements["consent"];
      var firstInvalid = null;

      var checks = [
        [name, "name-error", name.value.trim() ? "" : "Enter your name."],
        [email, "email-error", !email.value.trim() ? "Enter your email address." :
          (email.validity.valid ? "" : "Enter an email address in the format name@example.com.")],
        [planSet, "plan-error", plan ? "" : "Choose which plan you are interested in."],
        [age, "age-error", age.checked ? "" : "You must be 18 or over to use JMC Fitness plans."],
        [consent, "consent-error", consent.checked ? "" : "Confirm you have read the Privacy Policy so we can reply to your enquiry."]
      ];
      checks.forEach(function (c) {
        if (!setError(c[0], c[1], c[2]) && !firstInvalid) firstInvalid = c[0] === planSet ? planFirst : c[0];
      });

      if (firstInvalid) {
        status.textContent = "There is a problem with your enquiry. Please check the highlighted fields.";
        firstInvalid.focus();
        return;
      }

      var to = form.getAttribute("data-email");
      var subject = "COACH enquiry: " + plan.value;
      var body =
        "Name: " + name.value.trim() + "\n" +
        "Email: " + email.value.trim() + "\n" +
        "Plan: " + plan.value + "\n" +
        "Goal: " + (form.elements["goal"].value.trim() || "(not given)") + "\n\n" +
        "I confirm I am 18 or over and have read the Privacy Policy.";
      window.location.href = "mailto:" + to +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
      status.textContent = "Your email app should now open with your enquiry ready to send. " +
        "If it does not, email us directly at " + to + " or send \"COACH\" on Instagram.";
    });
  }

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
