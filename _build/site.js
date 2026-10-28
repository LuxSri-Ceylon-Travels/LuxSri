// Mobile menu
const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("nav");
if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.textContent = open ? "Close" : "Menu";
  });
}

// Footer year
document.querySelectorAll("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });

// Booking form: "Send booking request" emails it (Web3Forms), "Send on WhatsApp" opens a filled-in chat
const form = document.getElementById("enquiry");
if (form) {
  const status = form.querySelector(".form-status");
  const say = (msg, ok) => { status.hidden = false; status.textContent = msg; status.className = "form-status " + (ok ? "ok" : "err"); };
  const summary = (f) => {
    const lines = [];
    const add = (label, v) => { if (v && String(v).trim()) lines.push(`${label}: ${String(v).trim()}`); };
    add("Name", f.get("name")); add("Email", f.get("email")); add("Phone", f.get("phone")); add("Country", f.get("country"));
    add("Tour", f.get("trip")); add("Start date", f.get("arrive")); add("Days", f.get("days")); add("Guests", f.get("group"));
    add("Wishes", f.get("msg"));
    return lines;
  };
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const via = (e.submitter && e.submitter.value) || "email";
    const f = new FormData(form);
    if (f.get("botcheck")) return;
    const name = form.querySelector("[name=name]");
    if (!String(f.get("name") || "").trim()) { name.classList.add("bad"); name.focus(); say("Please add your name.", false); return; }
    name.classList.remove("bad");

    if (via === "whatsapp") {
      const text = ["Hi Mahesh, I'd like to plan a Sri Lanka trip.", ...summary(f)].join("\n");
      const url = `https://wa.me/${form.dataset.wa}?text=${encodeURIComponent(text)}`;
      const w = window.open(url, "_blank");
      if (w) w.opener = null; else window.location.href = url;
      return;
    }

    const email = form.querySelector("[name=email]");
    if (!email.value || !email.checkValidity()) { email.classList.add("bad"); email.focus(); say("Please add a valid email so we can reply.", false); return; }
    email.classList.remove("bad");

    if (!form.dataset.key) {
      if (form.dataset.email) {
        const body = encodeURIComponent(summary(f).join("\n"));
        window.location.href = `mailto:${form.dataset.email}?subject=${encodeURIComponent("Booking request from " + f.get("name"))}&body=${body}`;
      } else {
        say("Email booking isn't switched on yet. Please use the WhatsApp button for now.", false);
      }
      return;
    }

    const btn = e.submitter; if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "Sending…"; }
    try {
      const payload = Object.fromEntries(f.entries());
      payload.access_key = form.dataset.key;
      payload.subject = `New LuxSri booking request from ${f.get("name")}`;
      payload.from_name = "LuxSri website";
      payload.replyto = f.get("email");
      const r = await fetch("https://api.web3forms.com/submit", { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) });
      const res = await r.json();
      if (!res.success) throw new Error(res.message || "Send failed");
      form.reset();
      say("Thank you! Your request is on its way. Mahesh will reply by email, usually within a day.", true);
    } catch (err) {
      say("Sorry, that didn't send. Please try again, or use the WhatsApp button.", false);
    } finally {
      if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
    }
  });
}

// Opened straight from disk (double-clicked index.html): point folder links at their index.html
if (location.protocol === "file:") {
  document.querySelectorAll('a[href]').forEach((a) => {
    const h = a.getAttribute("href");
    if (/^\.{1,2}\//.test(h)) a.setAttribute("href", h.replace(/\/(#.*)?$/, "/index.html$1"));
  });
}

// Instagram strip: load the latest posts from the feed (falls back to our own photos),
// then every few seconds swap one slot to the next photo so the section keeps moving.
const ig = document.querySelector(".ig-grid");
if (ig) {
  const slots = [...ig.querySelectorAll(".ig-slot")];
  let items = [];
  try { items = JSON.parse(ig.dataset.fallback || "[]"); } catch (e) { items = []; }
  const toItem = (p) => {
    const sizes = p.sizes || {};
    const src = (sizes.medium && sizes.medium.mediaUrl) || (p.mediaType === "VIDEO" ? p.thumbnailUrl : p.mediaUrl) || p.thumbnailUrl;
    return src ? { src, href: p.permalink, alt: (p.prunedCaption || p.caption || "LuxSri on Instagram").slice(0, 120) } : null;
  };
  const show = (slot, item) => {
    const im = slot.querySelector("img");
    im.classList.add("fading");
    setTimeout(() => {
      im.src = item.src;
      if (item.alt) im.alt = item.alt;
      slot.href = item.href || slot.href;
      im.onload = () => im.classList.remove("fading");
    }, 350);
  };
  const start = () => {
    if (items.length <= slots.length) return;
    let next = slots.length, which = 0;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;
    setInterval(() => {
      if (document.hidden) return;
      show(slots[which], items[next]);
      which = (which + 1) % slots.length;
      next = (next + 1) % items.length;
    }, 4000);
  };
  if (ig.dataset.feed) {
    fetch(ig.dataset.feed)
      .then((r) => r.json())
      .then((data) => {
        const posts = (Array.isArray(data) ? data : data.posts || []).map(toItem).filter(Boolean).slice(0, 9);
        if (posts.length) {
          items = posts;
          slots.forEach((s, i) => items[i] && show(s, items[i]));
        }
      })
      .catch(() => {})
      .finally(start);
  } else {
    start();
  }
}

// Header: solid once the page scrolls past the hero
const header = document.querySelector(".site-header.over-hero");
if (header) {
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 40);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
}

// Scroll reveal
if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.documentElement.classList.add("js-reveal");
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll("[data-reveal]").forEach((el) => io.observe(el));
}

// Copy buttons
document.querySelectorAll("[data-copy]").forEach((b) => {
  b.addEventListener("click", () => {
    navigator.clipboard?.writeText(b.dataset.copy).then(() => {
      const t = b.textContent; b.textContent = "Copied"; setTimeout(() => (b.textContent = t), 1600);
    }).catch(() => {});
  });
});
