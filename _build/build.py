"""Generates the LuxSri static site (plain HTML) into OUT."""
import json, os, re, sys, html

OUT = sys.argv[1]
SITE = "https://www.luxsri.lk"
WA_NUM = "94775228576"
WA_TEXT = "+94 77 522 8576"
G = "https://lh7-us.googleusercontent.com/sitesv-images-rt/"

# Photos currently hosted by Google Sites. Before launch they get copied into
# assets/img/<key>.jpg and IMG_BASE switches to local files.
IMAGES = {
  "sigiriya-guests": "AMxu72um5-Y69qjBeP8dXRO-wSFTGb2DTI7NCkWZhSsGTp3Pvh9Wh4R7OJR8ZHjjnqwYEWWmmHFQA8667V81i3LP-qg3HL5f8KftwJ77bfqx7Oz8bj5r7HtUzryf2gQGzU0bZdwr77aVAhn1djOhl9drRZrvpQMJzXqjXhnumzAbHULi5_lvXF8NdSdeMuWbvLL2XD94NtSuHBBwX5aDW_9pwQF5KJWH71Izjsrqw3hP1Vs",
  "airport-welcome": "AMxu72tTT4-xlgSTGryqovHJHGhYKPthCyhlLG9nCRMW3UhCiQUtV8rRTkU_FvHv_C-2olDvZMxo9NtM8c3wIfeznYPrEHlQ6FLZyIkYmUvX-UM-qIoFFhiV9ZT6DX4Is8ONfwgO4PwSwZCQbrUpxZpV-6J_W-5z1z9qxbrBMwqbFKhZjdrcOSsULHa7bmILOLgBRfsjY1MNcor9zs5-JFbIekV6VMBDLAiLDk9jPj3ANU4",
  "lake-boat-safari": "AMxu72suT0lif-mkgXHyU2kG5jjYNJaLz9-gz8lCXf77TYgWqg07x__odIerD_VLyITjSUll_d2GXdmywxs8wAmshYLy7rYE7LL26mph0PC9f1qislPHv6anbLrexMJ--y97cB1L_zRWSmJucw3YV8Vveo8xrnVYhuktfJAcBVKeGt_cWGszfqaBnjdQxeL-2uYIrM9kJ6lKjtXEb0lTTuendjY8Vh4hN79HyR_9z_LB",
  "mahesh-with-guests": "AMxu72tAUHXEEkP_bBPtQVdpJTvO5eFVUOXRlxjYMS_qNmWMkEudgwut97Co7GmJ-Be58f1HJVuxcivki2fIpOpqI923lWHA0lCjvuJWhGPOQEkpfaZBJgSzdMA-ZV35caAwiHoNW5ftilfTXEEPsQay2rOWuiF0RYq2E2XKjE3GGXysDe-0s8Ga-eWC_qrc-7LF9049sOyaxCZJbqsap7hmwV9BXWTXRdEyYk1176vFPHY",
  "sage-pulasti": "AMxu72vgFLhRPJGC5xW9OZUdQuP-ZE1B0DagtL6zWJEJsyDXhBbAn308MkbcA0d1qEVGgESp42FTnTj0gBEYRLrniaOq3vR0EWSjuV3q-3kClonj428SyhUYvozd5hYm4Fq0RlpWdq6EuqZSqejnrSPqWm3zdytzhPAgC0Iwj3O8g1HBxhR5iVoeCabSO73glrvQnQNUWVA2xdqshDvevTKhCt17mA26o34M7tJDItxQ",
  "guardhouse": "AMxu72t-fKK1D0CMQoYxsjCPsjKoI0NKd3eO5iyxG3bgoMxlrOacHr37VGi7WNkN6FE41WL4zjBouagm3JMU8uOgiPAC-xfKuwLsfwkrOFcEPRHcpBt_DShR_70hy9160w-3P7xw0OKpij7iHDeqIR0kjU2YP8YpVvapLfqXCHvON5I7G5BtYJqr6hCsYf7ZQwbplk1MYYHkKRmQGhqZlrungiDc3Yfja8bwb7xlUMycKfk",
  "rankoth-vehera": "AMxu72tJix5k1yQwn_OfcosHEs0WCSiXBjNjzlMttXPOLNMbXnZE_vZf_hqAfCgck_fk3oqO3XZgZBd_we0d7NpEo188X3PEYoJlTygGgrokI_4OPUOv7G3GJOtKjwPMzHQ8MULK1dS5eVnSSMUl1edOX29mbf62h2hN8rSTSXoeHpnz9MhTyaABps1ThMw17l9Tj7VebgNQyexMdUCj6Dif1EUT-fWscsrJRNH73NA6qY0",
  "vejayanta-prasada": "AMxu72up92aJ4H90inmPDnU4XNdsEBVSmNc6nMN7KaaxoMZIdUICTAkFljnLOJCVrUmmrbMncr88hK3UlSBPAqHbe_-UiL3_D_9q57GuQO6hNNfOrWuLG5iCxP8_v5x3cJ8j2yU0geoGh8Oh8fpDZ__YZbQjhNZHTny7Dp2wbp61y383HGo9GboWMzTZfkbNhMOJ4iTUt_jD9gm62sYmnuTSlWMD-K91UwQSlaBaSraXAfE",
  "isurumuniya-lovers": "AMxu72v-s4AxieTo3TteTWdNsCkb3UmBvd1o08olf_WWfhBnC1JhKkT-sd-9ZCVGs8DaI3u9DUe5g7W3rurVSIg0MBvfXdiWtl1f0zZnylpeje-gJLXP2O9W9EnFv325oXg4UnVC77JSwRwP12YAf7HSb78FDuz3PHEPjoVK-xP2MBx4Umuk-TftMJkft_59dLJUux06HZ23jar3cqBv94kLjOr5aAoGggLIblVi6XDklbg",
  "isurumuni-viharaya": "AMxu72uDdf7LzvGeWbOQ9S-qTufsWGzoNegvAA8ymZf2u3pSkN0isNJu9AIyqVi9AnVQbIPCfTVnq8E-rkkaFtQR7BrlEZzGCgyfH3e6--wQMwQNUcTrk912XhWIzWJenhUx_DyPxOlXxf09yYGtuidLLPSNKDX5vOjej-3NHLmy846RZlm6Nstdul2q_D3lle-g_EBuiahVzHEHdvIHB92bwbA5hmQOENrSYVb_O70o",
  "kumana-leopard": "AMxu72usZtlOhwAM0PpPn6SNoVGRvoCV2zDsfMnQmtsE77Jd0P88JbSHXVcP7MW7E1J-UBlhuWUcepBvMYgVoukLM7SHXFnCX_UAf145mfdxLy6hcDGSx1YaXvyr06f8NWmnJLCtiC5jOC3udQAJolEkVtoUo8EdhoXb1MzVi2HSfyajcXQiLG7mdijl4rB0H1xKkmzAbZfem8GcsPdJ1R9hLXz1Ma7h_-Xp-eUtPtfw",
  "tooth-relic-temple": "AMxu72uLyQR_v-MOuYAY5cix-MrdjcyUfT1mVWc-mtvk_5cTGa90viP4DJ3zOqolhNan64LGSN9YBbgR-yqYRb9V7844CBGB7WVR5p_nk2SWk-gKQ8m0XJwHOrj34KI5ZJunTJseL7KhVYTZ0cGR7_WsVniicaX2XNfSJezWtRweDjHSKniilnUDLSauDp_jnBwfiIxtUlGcoMdt7v8XrelkLL270M4JOmGEgmdFktod",
  "pedlar-street": "AMxu72s14wa8jpiWtH3yj9CE9T_nMdWjOweJKn7qPqM5qUN4rI0rUBZVu1W5682Vy3nFrQAmTO3MvMa1ALdU3v_jSs5NMrmbCbAoJs9H4YvcUgS20vnx-UmMN14swaWdbu4dPqXw6xn2Mtptm4mwDVcceCMnM0QILuiUwiTHkS9sN558PElW6UfLSKk_Y0fm2yeJb7LWo6pTPWE64VglwXWJYWC35h-NWXptv5uy61J3",
  "church-street": "AMxu72uG9pFN9XuaESmujfidAOGVgqm2HB02utn3WfoGSGRhecQF7R7pWXEW76oxcxpy6SCwHi5n2_XOX8I8RWr-so8hmqQZyrxwI8TcGwHThK8FYMpfZkMjbYWrsveXeQTEpg0ddCrjnqR8H2ca4lNOI_0CPktmK4K7tT6EG924n-rCYEAgTiZpvuPyn5BNEK4MCBbPTbeyVCsvkUqnyFrgSs8k2-0851SIGiQWGWl-bFU",
  "ruwanweli-maha-seya": "AMxu72sRCjGP3sBLyFZGd2d7pVr6drytoDfefLN_9Ri0ujPbJNjulHak_5R9EbGSmqRw9dYZFeVkVNOG8kL7S-nqSlrKg0WqfHs4irhr23MlGemTErCU06S53deU88LekLzvHH09wuaSzWFIDhoY5ndYOGIWuf5edVfwMD0pKuXAHlJZDHVuY2EMqDnwFy2ugSCuEkrEqHJMgPuKwfdSS57R4rRBiuOmiEB5um1_zHbH",
  "rampart-street": "AMxu72tyM4lIW0r8XNgkbwTFOJu-gkIKjpxIvvSWeMF05TWkttsdaFDWa3EJUO-OewemulzlQXRfYJbOYMrzjPEHhau0QVp80FpWSbg09us0CnpxdrWJQs1otZYBnUDar8w1XEcJvgNjy49csjunvnXMkf-Kfn87HFV_iP0BgBWUCEUeyse6vdBLzn__0j0qvz9fROGnym_nxD2dchuzLHCsMQT3oeLgOPy1HGbE6OT3",
}
LOCAL = os.environ.get("LOCAL_IMAGES") == "1"

# Live Instagram section. Paste the Behold JSON feed URL here once the account is connected;
# until then the slots rotate through our own photos.
INSTAGRAM_FEED_URL = ""
INSTAGRAM_HANDLE = "luxsri_ceylon_travels"

# Email booking form. Bookings are sent through Web3Forms (free) to the inbox the key was made for.
# Until a key is set, the email button opens the visitor's mail app addressed to BOOKING_EMAIL.
WEB3FORMS_KEY = ""
BOOKING_EMAIL = ""

# Google reviews. GOOGLE_REVIEWS_URL = the business listing on Google Maps;
# REVIEWS_WIDGET = the embed snippet from Trustindex (free) once it's connected.
GOOGLE_REVIEWS_URL = ""
GOOGLE_WRITE_REVIEW_URL = ""
REVIEWS_WIDGET = ""

def img(key, w=1280):
    if LOCAL:
        return f"/assets/img/{key}.jpg"
    return f"{G}{IMAGES[key]}=w{w}"

def abs_img(key):
    return f"{SITE}/assets/img/{key}.jpg" if LOCAL else img(key)

def wa(msg="Hi Mahesh, I'd like to plan a Sri Lanka trip."):
    from urllib.parse import quote
    return f"https://wa.me/{WA_NUM}?text={quote(msg)}"

ICON = {
  "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2zm5.8 14.08c-.24.68-1.43 1.32-1.97 1.37-.5.05-1.13.07-1.83-.11-.42-.13-.96-.31-1.65-.61-2.9-1.25-4.8-4.18-4.94-4.37-.14-.19-1.18-1.57-1.18-3s.75-2.13 1.02-2.42c.26-.29.58-.36.77-.36h.55c.18 0 .42-.07.65.5.24.58.82 2 .89 2.15.07.14.12.31.02.5-.1.19-.14.31-.29.48-.14.17-.3.37-.43.5-.14.14-.29.3-.13.59.17.29.74 1.22 1.58 1.97 1.09.97 2 1.27 2.29 1.41.29.14.46.12.62-.07.17-.19.72-.84.91-1.13.19-.29.38-.24.65-.14.26.1 1.68.79 1.97.94.29.14.48.22.55.34.07.12.07.7-.17 1.38z"/></svg>',
  "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
  "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M3 13l2-6h14l2 6v4H3z"/><circle cx="7.5" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/></svg>',
  "plane": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 16l20-8-4 12-6-4-4 4v-6"/></svg>',
  "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h16v11H8l-4 4z"/><path d="M8 10h8M8 13h5"/></svg>',
  "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4 3 6v14l6-2 6 2 6-2V4l-6 2z"/><path d="M9 4v14M15 6v14"/></svg>',
  "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8V6.5c0-.7.2-1.2 1.2-1.2H17V2.1A22 22 0 0 0 14.6 2C12.2 2 10.6 3.4 10.6 6.1V8H8v3.4h2.6V22H14V11.4h2.7L17.1 8z"/></svg>',
  "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
  "tt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 2h-3.3v13.4a2.9 2.9 0 1 1-2-2.8V9.2a6.2 6.2 0 1 0 5.3 6.2V8.6a7.9 7.9 0 0 0 4.4 1.4V6.7a4.5 4.5 0 0 1-4.4-4.7z"/></svg>',
}
# Monogram until the real logo file is dropped in.
MARK = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="none" stroke="#b98a3e" stroke-width="1.5"/><path d="M20 7c-3 5-3 9 0 13 3-4 3-8 0-13z" fill="#b98a3e"/><path d="M11 30h18M14 30V19M26 30V19M20 30v-7" stroke="#e9d7b4" stroke-width="1.6" fill="none" stroke-linecap="round"/></svg>'

SOCIAL = {
  "facebook": "https://www.facebook.com/profile.php?id=61587585470639",
  "instagram": "https://www.instagram.com/luxsri_ceylon_travels/",
  "tiktok": "https://www.tiktok.com/@maheshthilakasiri",
}
NAV = [
  ("/", "Home"),
  ("/private-driver-sri-lanka/", "Private Driver"),
  ("/sri-lanka-tour-packages/", "Tour Packages"),
  ("/luxsri-journey/", "Journey Gallery"),
  ("/contact/", "Contact"),
]

ORG = {
  "@context": "https://schema.org",
  "@type": "TravelAgency",
  "@id": f"{SITE}/#business",
  "name": "LuxSri Ceylon Travels",
  "url": f"{SITE}/",
  "image": abs_img("sigiriya-guests"),
  "telephone": "+94775228576",
  **({"email": BOOKING_EMAIL} if BOOKING_EMAIL else {}),
  "slogan": "Journey Beyond Expectations",
  "description": "Private English-speaking chauffeur guide and tailor-made Sri Lanka tours with Mahesh Thilakasiri.",
  "areaServed": {"@type": "Country", "name": "Sri Lanka"},
  "address": {"@type": "PostalAddress", "addressCountry": "LK"},
  "founder": {"@type": "Person", "name": "Mahesh Thilakasiri"},
  "sameAs": list(SOCIAL.values()),
}

def page(path, title, desc, body, active, og_img="sigiriya-guests", extra_ld=(), over_hero=False):
    canon = SITE + path
    nav = "\n".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    lds = [ORG, *extra_ld]
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#12352c">
<meta property="og:type" content="website">
<meta property="og:site_name" content="LuxSri Ceylon Travels">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{abs_img(og_img)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marcellus&family=Manrope:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/site.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header{' over-hero' if over_hero else ''}">
  <div class="wrap">
    <a class="brand" href="/" aria-label="LuxSri Ceylon Travels home">{MARK}<span class="brand-name">LuxSri<small>Ceylon Travels</small></span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">
      {nav}
      <a class="btn btn-gold btn-sm" href="/contact/">Book your journey</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div class="stack">
        <a class="brand" href="/">{MARK}<span class="brand-name">LuxSri<small>Ceylon Travels</small></span></a>
        <p>Private chauffeur guide and tailor-made tours across Sri Lanka with Mahesh Thilakasiri. Journey Beyond Expectations.</p>
        <div class="socials">
          <a href="{SOCIAL['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ICON['fb']}</a>
          <a href="{SOCIAL['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ICON['ig']}</a>
          <a href="{SOCIAL['tiktok']}" target="_blank" rel="noopener" aria-label="TikTok">{ICON['tt']}</a>
        </div>
      </div>
      <div>
        <h3>Explore</h3>
        <ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)}</ul>
      </div>
      <div>
        <h3>Contact</h3>
        <ul>
          <li><a href="{wa()}" target="_blank" rel="noopener">WhatsApp {WA_TEXT}</a></li>
          <li><a href="tel:+94775228576">Call {WA_TEXT}</a></li>
          {f'<li><a href="mailto:{BOOKING_EMAIL}">{BOOKING_EMAIL}</a></li>' if BOOKING_EMAIL else ''}
          <li><a href="/contact/">Booking form</a></li>
          <li>Airport pickup at Colombo (CMB)</li>
        </ul>
      </div>
    </div>
    <div class="legal"><span>© <span data-year>2026</span> LuxSri Ceylon Travels. All rights reserved.</span><span>Sri Lanka</span></div>
  </div>
</footer>
<a class="wa-float" href="{wa()}" target="_blank" rel="noopener" aria-label="Chat with Mahesh on WhatsApp">{ICON["wa"]}<span class="wa-label">Chat with Mahesh</span></a>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""

def facts():
    items = [
      ("chat", "English-speaking chauffeur", "Mahesh drives and guides you himself"),
      ("car", "Private A/C vehicle", "No shared buses or fixed schedules"),
      ("plane", "Airport pickup", "Met at Colombo airport (CMB)"),
      ("map", "Free tailor-made plan", "Itinerary and quote on WhatsApp"),
    ]
    lis = "".join(f'<li>{ICON[i]}<span><strong>{a}</strong>{b}</span></li>' for i, a, b in items)
    return f'<div class="facts"><div class="wrap"><ul>{lis}</ul></div></div>'

STEPS = """
<ol class="steps">
  <li><h3>Message Mahesh</h3><p class="muted">Send your travel dates, group size and the places you'd like to see on WhatsApp.</p></li>
  <li><h3>Get your plan</h3><p class="muted">Receive a free personalised itinerary and quote, then adjust it until it feels right.</p></li>
  <li><h3>Arrive and relax</h3><p class="muted">Confirm, and Mahesh meets you at the airport with a name sign. The rest is your journey.</p></li>
</ol>"""

TRIP_OPTIONS = ["A tailor-made tour", "7-Day Cultural Triangle & Kandy", "10-Day Sri Lanka Highlights",
                "14-Day Complete Round Trip", "Day trip", "Airport transfer"]

def booking_form(full=False):
    """One form, two ways to send: email (Web3Forms) or WhatsApp with the details filled in."""
    opts = "".join(f"<option>{html.escape(o)}</option>" for o in TRIP_OPTIONS)
    extra = """
      <fieldset><legend>About you</legend>""" if full else ""
    about = f"""
      <div class="row">
        <label for="f-name">Full name<input id="f-name" name="name" autocomplete="name" required></label>
        <label for="f-email">Email<input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@example.com"></label>
      </div>""" + ("""
      <div class="row">
        <label for="f-phone">WhatsApp or phone <em>(optional)</em><input id="f-phone" name="phone" type="tel" autocomplete="tel"></label>
        <label for="f-country">Country <em>(optional)</em><input id="f-country" name="country" autocomplete="country-name"></label>
      </div>""" if full else "")
    return f"""
    <form class="form" id="enquiry" data-wa="{WA_NUM}" data-key="{WEB3FORMS_KEY}" data-email="{BOOKING_EMAIL}" novalidate>
      {'<fieldset><legend>Trip details</legend>' if full else ''}
      <div class="row">
        <label for="f-trip">Tour<select id="f-trip" name="trip">{opts}</select></label>
        <label for="f-arrive">Start date<input id="f-arrive" name="arrive" type="date"></label>
      </div>
      <div class="row">
        <label for="f-days">Number of days<input id="f-days" name="days" type="number" min="1" max="60" placeholder="e.g. 10"></label>
        <label for="f-group">Number of guests<input id="f-group" name="group" type="number" min="1" max="20" placeholder="e.g. 2"></label>
      </div>
      {'</fieldset>' if full else ''}{extra}{about}
      <label for="f-msg">Places, wishes or questions<textarea id="f-msg" name="msg" placeholder="Sigiriya, the Ella train, a leopard safari, beach time…"></textarea></label>
      {'</fieldset>' if full else ''}
      <label class="hp" aria-hidden="true">Leave this empty<input name="botcheck" tabindex="-1" autocomplete="off"></label>
      <div class="send">
        <button class="btn btn-gold" type="submit" value="email">Send booking request</button>
        <button class="btn btn-wa" type="submit" value="whatsapp">{ICON['wa']}Send on WhatsApp</button>
      </div>
      <p class="form-status" role="status" aria-live="polite" hidden></p>
      <p class="note">Email goes straight to the LuxSri inbox; WhatsApp opens a chat with Mahesh. Nothing is stored on this website.</p>
    </form>"""

STEPS_BAND = f"""
<section class="band band-sand">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">How it works</span><h2>From first message to airport welcome</h2></div>
    {STEPS}
  </div>
</section>"""

def enquiry(heading="Plan your journey with Mahesh"):
    return f"""
<section class="band band-forest" id="plan">
  <div class="wrap enquire">
    <div class="stack-lg" data-reveal>
      <div class="stack">
        <span class="eyebrow">Free itinerary and quote</span>
        <h2>{heading}</h2>
        <p class="muted">Tell us a little about your trip and send it by email or WhatsApp. Mahesh replies personally with a free plan and quote.</p>
      </div>
      <ul class="contact-list">
        <li><span>WhatsApp or call</span><a href="{wa()}" target="_blank" rel="noopener">{WA_TEXT}</a></li>
        {f'<li><span>Email</span><a href="mailto:{BOOKING_EMAIL}">{BOOKING_EMAIL}</a></li>' if BOOKING_EMAIL else ''}
        <li><span>Instagram</span><a href="{SOCIAL['instagram']}" target="_blank" rel="noopener">@luxsri_ceylon_travels</a></li>
        <li><span>TikTok</span><a href="{SOCIAL['tiktok']}" target="_blank" rel="noopener">@maheshthilakasiri</a></li>
      </ul>
    </div>
    {booking_form()}
  </div>
</section>"""

TOURS = [
  ("7-day-cultural-triangle-kandy", "7 days", "Cultural Triangle & Kandy", "sigiriya-guests",
   "Sigiriya, Dambulla, Polonnaruwa and Anuradhapura, an elephant safari, then Kandy's Temple of the Tooth.",
   [("Day 1", "Airport pickup and transfer to Negombo or Sigiriya"),
    ("Day 2", "Sigiriya Rock Fortress climb and Dambulla Cave Temple"),
    ("Day 3", "Polonnaruwa ancient city, evening elephant safari in Minneriya or Kaudulla"),
    ("Day 4", "Anuradhapura sacred city: Ruwanweli Maha Seya and Isurumuniya"),
    ("Day 5", "Spice garden on the way to Kandy, Temple of the Sacred Tooth Relic"),
    ("Day 6", "Peradeniya Botanical Gardens and Kandy city"),
    ("Day 7", "Transfer to Colombo airport")]),
  ("10-day-sri-lanka-highlights", "10 days", "Sri Lanka Highlights", "kumana-leopard",
   "Ancient cities, tea country, the famous train to Ella, a Yala leopard safari and the south coast.",
   [("Days 1–3", "Sigiriya, Dambulla and Polonnaruwa"),
    ("Days 4–5", "Kandy and the Nuwara Eliya tea country"),
    ("Day 6", "Scenic train ride to Ella"),
    ("Day 7", "Ella Rock, Nine Arch Bridge and Little Adam's Peak"),
    ("Day 8", "Leopard and elephant safari in Yala National Park"),
    ("Day 9", "South coast beaches and Galle Fort"),
    ("Day 10", "Transfer to Colombo airport")]),
  ("14-day-complete-round-trip", "14 days", "Complete Sri Lanka Round Trip", "pedlar-street",
   "The whole island at an easy pace, from the sacred cities to an east coast safari and Galle Fort.",
   None),
]
ROUND_TRIP = ["Anuradhapura", "Polonnaruwa", "Sigiriya", "Kandy", "Hill country", "Ella",
              "Yala or Kumana safari", "South coast beaches", "Galle Fort"]

PLACES = [
  ("Sigiriya & Dambulla", "Lion Rock fortress and the cave temple"),
  ("Anuradhapura & Polonnaruwa", "Ancient royal and sacred cities"),
  ("Kandy", "Temple of the Sacred Tooth Relic"),
  ("Nuwara Eliya", "Tea estates and cool hill country"),
  ("Kandy to Ella train", "One of the world's most scenic rail rides"),
  ("Yala & Kumana", "Leopard, elephant and bird safaris"),
  ("Ella", "Nine Arch Bridge and Little Adam's Peak"),
  ("Galle Fort", "Dutch colonial streets by the sea"),
  ("South coast", "Beaches from Unawatuna to Mirissa"),
]

GALLERY = [
  ("sage-pulasti", "Sage Pulasti", "Polonnaruwa", "Ancient rock-cut statue of Sage Pulasti at Polonnaruwa, Sri Lanka"),
  ("guardhouse", "Guardhouse ruins", "Polonnaruwa", "Brick ruins of the guardhouse in the ancient city of Polonnaruwa, Sri Lanka"),
  ("rankoth-vehera", "Rankoth Vehera", "Polonnaruwa", "Rankoth Vehera, the largest stupa in Polonnaruwa, Sri Lanka"),
  ("vejayanta-prasada", "Vejayanta Prasada", "Polonnaruwa", "Ruins of Vejayanta Prasada royal palace of King Parakramabahu, Polonnaruwa, Sri Lanka"),
  ("isurumuniya-lovers", "Isurumuniya Lovers", "Anuradhapura", "Isurumuniya Lovers ancient stone carving at Isurumuni temple, Anuradhapura, Sri Lanka"),
  ("isurumuni-viharaya", "Isurumuni Viharaya", "Anuradhapura", "Isurumuni Viharaya rock temple and pond in Anuradhapura, Sri Lanka"),
  ("ruwanweli-maha-seya", "Ruwanweli Maha Seya", "Anuradhapura", "Ruwanweli Maha Seya white stupa at sunset in the sacred city of Anuradhapura, Sri Lanka"),
  ("kumana-leopard", "Kotiya, the leopard", "Kumana National Park", "Leopard (kotiya) resting on the entrance sign at Kumana National Park safari, Sri Lanka"),
  ("tooth-relic-temple", "Temple of the Tooth", "Kandy", "Temple of the Sacred Tooth Relic in Kandy lit up during the Esala Perahera with elephants, Sri Lanka"),
  ("pedlar-street", "Pedlar Street", "Galle Fort", "Colonial buildings and shops on Pedlar Street inside Galle Fort, Sri Lanka"),
  ("church-street", "Church Street", "Galle Fort", "Colonial-era Church Street and Dutch architecture inside Galle Fort, Sri Lanka"),
  ("rampart-street", "Rampart Street", "Galle Fort", "Colonial house with veranda on Rampart Street in Galle Fort, Sri Lanka"),
]

def figure(k, t, loc, alt):
    return (f'<figure><div class="frame"><img src="{img(k, 900)}" alt="{html.escape(alt)}" loading="lazy" width="900" height="675"></div>'
            f'<figcaption><strong>{t}</strong><span>{loc}</span></figcaption></figure>')

FAQ = [
  ("Who will be driving us?", "Mahesh Thilakasiri, the founder of LuxSri Ceylon Travels, is your English-speaking private chauffeur guide for the whole trip."),
  ("Do you pick up from the airport?", "Yes. Airport pickup and drop-off at Colombo Bandaranaike International Airport (CMB) is included, and private transfers can go anywhere in Sri Lanka."),
  ("Can we change the sample itineraries?", "Yes. Every tour is planned around you. The sample routes can be shortened, extended or combined, and plans can change along the way."),
  ("How much does a tour cost?", "It depends on your dates, route and group size. Send your details on WhatsApp and Mahesh will reply with a free personalised itinerary and quote."),
  ("Who are your tours for?", "Couples, families and small groups of friends who want to travel at their own pace in a private air-conditioned vehicle."),
]

def faq_block():
    items = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    return f"""
<section class="band">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">Good to know</span><h2>Questions travellers ask</h2></div>
    <div class="faq">{items}</div>
  </div>
</section>"""

FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

def tour_cards():
    out = []
    for slug, days, name, im, blurb, _ in TOURS:
        out.append(f'''<article class="tour" data-reveal><div class="img"><img src="{img(im, 900)}" alt="" loading="lazy" width="900" height="600"></div>
<div class="body"><span class="days">{days}</span><h3>{html.escape(name)}</h3><p>{blurb}</p>
<a class="more" href="/sri-lanka-tour-packages/#{slug}">See the itinerary →</a></div></article>''')
    return "".join(out)

INSTA_FALLBACK = ["ruwanweli-maha-seya", "kumana-leopard", "tooth-relic-temple", "lake-boat-safari",
                  "pedlar-street", "airport-welcome", "isurumuni-viharaya", "sigiriya-guests", "rampart-street"]

def insta_block():
    ig = f"https://www.instagram.com/{INSTAGRAM_HANDLE}/"
    fallback = json.dumps([{"src": img(k, 900), "href": ig} for k in INSTA_FALLBACK])
    slots = "".join(
        f'<a class="ig-slot" href="{ig}" target="_blank" rel="noopener"><img src="{img(k, 900)}" alt="Recent LuxSri journey photo" loading="lazy" width="900" height="900"></a>'
        for k in INSTA_FALLBACK[:3])
    return f"""
<section class="band band-sand" id="instagram">
  <div class="wrap">
    <div class="ig-head">
      <div class="section-head" data-reveal><span class="eyebrow">Latest on Instagram</span><h2>On the road right now</h2></div>
      <a class="btn btn-ig" href="{ig}" target="_blank" rel="noopener">{ICON['ig']}@{INSTAGRAM_HANDLE}</a>
    </div>
    <div class="ig-grid" data-feed="{INSTAGRAM_FEED_URL}" data-fallback='{html.escape(fallback, quote=True)}'>{slots}</div>
  </div>
</section>"""

EXPERIENCES = [
  ("ruwanweli-maha-seya", "Ancient cities", "Anuradhapura, Polonnaruwa and Sigiriya"),
  ("kumana-leopard", "Wildlife safaris", "Leopards and elephants in Yala and Kumana"),
  ("tooth-relic-temple", "Temples & culture", "Kandy and the Temple of the Tooth"),
  ("lake-boat-safari", "Lakes & rivers", "Boat safaris with a local guide"),
  ("pedlar-street", "Colonial Galle", "Walk the Dutch fort by the sea"),
  ("airport-welcome", "Seamless arrival", "Met at Colombo airport with your name"),
]

def experiences():
    tiles = "".join(f'''<a class="exp" href="/sri-lanka-tour-packages/" data-reveal>
<img src="{img(k, 900)}" alt="" loading="lazy" width="900" height="1200">
<span class="exp-text"><strong>{t}</strong><span>{d}</span></span></a>''' for k, t, d in EXPERIENCES)
    return f"""
<section class="band">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">Signature experiences</span><h2>The Sri Lanka you came for</h2><p class="muted">Mix and match these on one private, unhurried route planned around you.</p></div>
    <div class="exps">{tiles}</div>
  </div>
</section>"""

def quote_band():
    return f"""
<section class="quote-band">
  <img src="{img('ruwanweli-maha-seya', 1920)}" alt="" loading="lazy" width="1920" height="1280">
  <div class="wrap" data-reveal>
    <p class="quote-mark" aria-hidden="true">“</p>
    <p class="quote">Journey Beyond Expectations.</p>
    <p class="quote-by">Mahesh Thilakasiri, founder</p>
    <div class="btn-row"><a class="btn btn-gold" href="/contact/">Start planning</a><a class="btn btn-ghost" href="{wa()}" target="_blank" rel="noopener">{ICON['wa']}Ask on WhatsApp</a></div>
  </div>
</section>"""

def reviews_block():
    widget = REVIEWS_WIDGET or '''<div class="reviews-empty">
      <p class="stars" aria-hidden="true">★★★★★</p>
      <p>Guest reviews from Google will appear here.</p>
    </div>'''
    btns = ""
    if GOOGLE_REVIEWS_URL:
        btns += f'<a class="btn btn-ig" href="{GOOGLE_REVIEWS_URL}" target="_blank" rel="noopener">See all reviews on Google</a>'
    if GOOGLE_WRITE_REVIEW_URL:
        btns += f'<a class="btn btn-gold" href="{GOOGLE_WRITE_REVIEW_URL}" target="_blank" rel="noopener">Write a review</a>'
    return f"""
<section class="band" id="reviews">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">Guest reviews</span><h2>What travellers say</h2></div>
    <div class="reviews">{widget}</div>
    {f'<div class="btn-row" style="margin-top:1.5rem">{btns}</div>' if btns else ''}
  </div>
</section>"""

# ---------- Home ----------
home = f"""
<section class="hero hero-home">
  <img class="kenburns" src="{img('sigiriya-guests', 1920)}" alt="Happy guests at Sigiriya Rock on a private LuxSri Ceylon Travels tour in Sri Lanka" width="1920" height="1280" fetchpriority="high">
  <div class="wrap">
    <div class="hero-copy">
      <span class="eyebrow">Private driver &amp; tailor-made tours</span>
      <h1>Discover Sri Lanka with Mahesh</h1>
      <p class="lead">Temples, tea hills, leopards and quiet beaches, at your own pace, with your own English-speaking chauffeur guide from the moment you land.</p>
      <div class="btn-row">
        <a class="btn btn-gold" href="/contact/">Book your journey</a>
        <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{ICON['wa']}WhatsApp Mahesh</a>
        <a class="btn btn-ghost" href="/sri-lanka-tour-packages/">See tour ideas</a>
      </div>
    </div>
  </div>
</section>
{facts()}
<section class="band band-sand">
  <div class="wrap split">
    <div class="photo"><img src="{img('mahesh-with-guests')}" alt="Mahesh Thilakasiri, founder of LuxSri Ceylon Travels, with guests on a private tour in Sri Lanka" loading="lazy" width="1024" height="1280"></div>
    <div class="stack-lg">
      <div class="stack">
        <span class="eyebrow">A personal journey</span>
        <h2>Hello, I'm Mahesh Thilakasiri</h2>
      </div>
      <div class="stack narrow">
        <p>I founded LuxSri Ceylon Travels to share the Sri Lanka I love with travellers who want more than a bus tour. I drive and guide every trip myself, so you always have someone local beside you who knows the roads, the history and the best place for lunch.</p>
        <p>From the ancient cities and hill-country temples to wildlife safaris, train journeys and the beaches of the south, I plan each itinerary around you, in a comfortable air-conditioned vehicle, from airport pickup to departure.</p>
        <p>My goal is simple: help you enjoy an authentic Sri Lankan experience and take home memories that last.</p>
      </div>
      <p class="signature">Journey Beyond Expectations.</p>
    </div>
  </div>
</section>
{experiences()}
<section class="band band-sand">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">How it works</span><h2>From first message to airport welcome</h2></div>
    {STEPS}
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">Sample itineraries</span><h2>Tour ideas to start from</h2><p class="muted">Each route can be shortened, extended or combined. Every trip includes your private chauffeur guide, an air-conditioned vehicle and airport transfers.</p></div>
    <div class="tours">{tour_cards()}</div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">Journey gallery</span><h2>Moments from the road</h2></div>
    <div class="gallery teaser">{"".join(figure(*g) for g in [GALLERY[2], GALLERY[7], GALLERY[8], GALLERY[9]])}</div>
    <p style="margin-top:1.5rem"><a href="/luxsri-journey/"><strong>See the full gallery →</strong></a></p>
  </div>
</section>
{quote_band()}
{reviews_block()}
{insta_block()}
{faq_block()}
{enquiry()}
"""

# ---------- Private driver ----------
INCLUDED = [
  "A personalised itinerary built around your dates, interests and pace",
  "An English-speaking private chauffeur guide for the whole trip",
  "A comfortable air-conditioned vehicle",
  "Airport pickup and drop-off at Colombo Bandaranaike International Airport (CMB)",
  "Local tips on food, culture and lesser-known places",
  "Freedom to stop for photos, roadside stalls and village temples",
]
driver = f"""
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">Private Driver Sri Lanka</span>
  <h1>Your private chauffeur guide in Sri Lanka</h1>
  <p>Travel Sri Lanka at your own pace with Mahesh Thilakasiri, founder of LuxSri Ceylon Travels and a professional English-speaking driver. No shared buses, no fixed group schedules. Just you, a comfortable air-conditioned vehicle and a local guide.</p>
  <div class="btn-row"><a class="btn btn-wa" href="{wa('Hi Mahesh, I need a private driver in Sri Lanka.')}" target="_blank" rel="noopener">{ICON['wa']}Check your dates on WhatsApp</a></div>
</div></section>
{facts()}
<section class="band">
  <div class="wrap split">
    <div class="stack-lg">
      <div class="stack"><span class="eyebrow">What's included</span><h2>Everything you need for an easy trip</h2></div>
      <ul class="included">{"".join(f'<li>{ICON["check"]}<span>{i}</span></li>' for i in INCLUDED)}</ul>
    </div>
    <div class="photo"><img src="{img('airport-welcome')}" alt="Guest welcomed with a name sign at Colombo airport pickup by LuxSri Ceylon Travels, Sri Lanka" loading="lazy" width="1024" height="1280"></div>
  </div>
</section>
<section class="band band-forest">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">Where we drive</span><h2>Anywhere on the island</h2><p class="muted">These are the places guests ask for most. Mahesh will happily take you beyond them.</p></div>
    <div class="places">{"".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in PLACES)}</div>
  </div>
</section>
<section class="band">
  <div class="wrap split">
    <div class="photo"><img src="{img('lake-boat-safari')}" alt="Guests on a lake boat safari with their LuxSri Ceylon Travels guide in Sri Lanka" loading="lazy" width="1024" height="1280"></div>
    <div class="stack-lg">
      <div class="stack"><span class="eyebrow">Why a private driver</span><h2>See more, wait less</h2></div>
      <div class="stack narrow">
        <p>Many of Sri Lanka's best places are hard to reach by public transport. With your own driver you can stop for photos, roadside fruit stalls and village temples, start early at Sigiriya to beat the crowds, and change plans on the way when something catches your eye.</p>
        <p>It's the relaxed way to travel for couples, families and small groups of friends.</p>
      </div>
    </div>
  </div>
</section>
<section class="band band-sand">
  <div class="wrap">
    <div class="section-head" data-reveal><span class="eyebrow">How to book</span><h2>Three simple steps</h2></div>
    {STEPS}
  </div>
</section>
{faq_block()}
{enquiry("Book your Sri Lanka driver")}
"""

# ---------- Tour packages ----------
def itin_block(t):
    slug, days, name, im, blurb, plan = t
    if plan:
        detail = '<ol class="days-list">' + "".join(f"<li><b>{d}</b><span>{x}</span></li>" for d, x in plan) + "</ol>"
    else:
        detail = ('<p class="muted" style="margin-bottom:1rem">A two-week loop of the whole island, planned day by day with you. A typical route:</p>'
                  '<ul class="route">' + "".join(f"<li>{p}</li>" for p in ROUND_TRIP) + "</ul>")
    return f"""
<article class="itin" id="{slug}" data-reveal>
  <div class="meta">
    <div class="img"><img src="{img(im, 900)}" alt="" loading="lazy" width="900" height="600"></div>
    <span class="eyebrow">{days}</span>
    <h2>{html.escape(name)}</h2>
    <p class="muted">{blurb}</p>
    <div><a class="btn btn-wa btn-sm" href="{wa(f"Hi Mahesh, I'm interested in the {days} {name} tour.")}" target="_blank" rel="noopener">{ICON['wa']}Ask about this tour</a></div>
  </div>
  <div>{detail}</div>
</article>"""

TRIP_LD = [{"@context": "https://schema.org", "@type": "TouristTrip", "name": f"{t[1]} {t[2]} tour",
            "description": t[4], "touristType": ["Couples", "Families", "Small groups"],
            "provider": {"@id": f"{SITE}/#business"}} for t in TOURS]

tours = f"""
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">Sri Lanka Tour Packages</span>
  <h1>Tailor-made Sri Lanka tours with a private driver</h1>
  <p>Every tour is planned around you. These sample itineraries show the most popular routes, and each one can be shortened, extended or combined. All trips include a private English-speaking chauffeur guide, an air-conditioned vehicle and airport pickup and drop-off.</p>
</div></section>
<section class="band">
  <div class="wrap itins">{"".join(itin_block(t) for t in TOURS)}</div>
</section>
<section class="band band-sand">
  <div class="wrap split">
    <div class="stack-lg">
      <div class="stack"><span class="eyebrow">Shorter trips</span><h2>Day trips and airport transfers</h2></div>
      <p class="narrow">Day tours from Colombo, Negombo, Kandy and Galle, plus private transfers from Colombo Bandaranaike International Airport (CMB) to anywhere in Sri Lanka.</p>
      <div><a class="btn btn-wa" href="{wa('Hi Mahesh, I would like a day trip / airport transfer.')}" target="_blank" rel="noopener">{ICON['wa']}Ask for a day trip or transfer</a></div>
    </div>
    <div class="photo"><img src="{img('airport-welcome')}" alt="Traveller arriving in Sri Lanka met with a welcome sign for her private chauffeur tour" loading="lazy" width="1024" height="1280"></div>
  </div>
</section>
{enquiry("Plan your Sri Lanka tour")}
"""

# ---------- Gallery ----------
gallery = f"""
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">LuxSri Journey</span>
  <h1>Moments from our journeys</h1>
  <p>Ancient cities, sacred temples, wildlife and colonial streets, photographed on the road with LuxSri guests across Sri Lanka.</p>
</div></section>
<section class="band">
  <div class="wrap"><div class="gallery">{"".join(figure(*g) for g in GALLERY)}</div></div>
</section>
{enquiry("Want to see these places yourself?")}
"""

# ---------- Contact / booking ----------
contact = f"""
<section class="page-hero"><div class="wrap">
  <span class="eyebrow">Book your journey</span>
  <h1>Plan your Sri Lanka trip with Mahesh</h1>
  <p>Share your dates and wishes and you'll get a free personalised itinerary and quote. Send it by email, or straight to Mahesh on WhatsApp.</p>
</div></section>
<section class="band">
  <div class="wrap contact-grid">
    <div class="form-wrap">{booking_form(full=True)}</div>
    <aside class="contact-cards">
      <div class="card">
        <span class="eyebrow">Fastest reply</span>
        <h2>WhatsApp Mahesh</h2>
        <p class="muted">Most guests plan their trip over WhatsApp. Send a hello any time.</p>
        <a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{ICON['wa']}Open WhatsApp</a>
      </div>
      <div class="card">
        <span class="eyebrow">Call or message</span>
        <p class="copy-row"><strong>{WA_TEXT}</strong><button class="copy" type="button" data-copy="+94775228576">Copy</button></p>
        {f'<span class="eyebrow">Email</span><p class="copy-row"><strong>{BOOKING_EMAIL}</strong><button class="copy" type="button" data-copy="{BOOKING_EMAIL}">Copy</button></p>' if BOOKING_EMAIL else ''}
      </div>
      <div class="card">
        <span class="eyebrow">Follow the journey</span>
        <div class="socials socials-dark">
          <a href="{SOCIAL['facebook']}" target="_blank" rel="noopener" aria-label="Facebook">{ICON['fb']}</a>
          <a href="{SOCIAL['instagram']}" target="_blank" rel="noopener" aria-label="Instagram">{ICON['ig']}</a>
          <a href="{SOCIAL['tiktok']}" target="_blank" rel="noopener" aria-label="TikTok">{ICON['tt']}</a>
        </div>
      </div>
    </aside>
  </div>
</section>
{STEPS_BAND}
"""

redirect = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>LuxSri Ceylon Travels</title>
<link rel="canonical" href="{SITE}/"><meta http-equiv="refresh" content="0; url=/"><meta name="robots" content="noindex"></head>
<body><p><a href="/">Continue to LuxSri Ceylon Travels</a></p></body></html>"""

notfound = page("/404.html", "Page not found | LuxSri Ceylon Travels", "This page could not be found.",
  f"""<section class="page-hero"><div class="wrap"><span class="eyebrow">404</span><h1>We couldn't find that page</h1>
<p>The link may be old. Try the home page or message Mahesh directly.</p>
<div class="btn-row"><a class="btn btn-gold" href="/">Go to the home page</a><a class="btn btn-wa" href="{wa()}" target="_blank" rel="noopener">{ICON['wa']}WhatsApp Mahesh</a></div></div></section>""", None)

PAGES = {
  "index.html": page("/", "Private Driver & Tailor-Made Sri Lanka Tours | LuxSri Ceylon Travels",
     "Explore Sri Lanka with Mahesh Thilakasiri, your English-speaking private chauffeur guide. Tailor-made tours, A/C vehicle and Colombo airport pickup. Free itinerary on WhatsApp.",
     home, "/", extra_ld=[FAQ_LD], over_hero=True),
  "private-driver-sri-lanka/index.html": page("/private-driver-sri-lanka/", "Private Driver in Sri Lanka with English-Speaking Chauffeur | LuxSri",
     "Hire Mahesh as your private driver in Sri Lanka: English-speaking chauffeur guide, air-conditioned vehicle, airport pickup and a free personalised itinerary.",
     driver, "/private-driver-sri-lanka/", og_img="airport-welcome", extra_ld=[FAQ_LD]),
  "sri-lanka-tour-packages/index.html": page("/sri-lanka-tour-packages/", "Sri Lanka Tour Packages: 7, 10 & 14 Day Itineraries | LuxSri",
     "Tailor-made Sri Lanka tour packages with a private driver: 7-day Cultural Triangle & Kandy, 10-day Highlights, 14-day round trip, day trips and airport transfers.",
     tours, "/sri-lanka-tour-packages/", og_img="kumana-leopard", extra_ld=TRIP_LD),
  "luxsri-journey/index.html": page("/luxsri-journey/", "Sri Lanka Travel Photo Gallery | LuxSri Journey",
     "Photos from LuxSri journeys across Sri Lanka: Polonnaruwa, Anuradhapura, Kandy's Temple of the Tooth, Kumana leopards and Galle Fort.",
     gallery, "/luxsri-journey/", og_img="ruwanweli-maha-seya"),
  "contact/index.html": page("/contact/", "Book a Private Sri Lanka Tour | Contact LuxSri Ceylon Travels",
     "Request a free personalised Sri Lanka itinerary and quote from Mahesh Thilakasiri by email or WhatsApp. Private driver, airport pickup, tailor-made tours.",
     contact, "/contact/"),
  "home/index.html": redirect,
  "404.html": notfound,
}

for rel, content in PAGES.items():
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if rel != "404.html":
        # Relative links so the site also works under username.github.io/LuxSri/ before the domain moves.
        pre = "../" * rel.count("/") or "./"
        content = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{pre}', content)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    urls = ["/", "/private-driver-sri-lanka/", "/sri-lanka-tour-packages/", "/luxsri-journey/", "/contact/"]
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "".join(f"  <url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(OUT, "CNAME"), "w") as f:
    f.write("www.luxsri.lk\n")
with open(os.path.join(OUT, "assets", "images.json"), "w") as f:
    json.dump({k: f"{G}{v}=w1920" for k, v in IMAGES.items()}, f, indent=2)
with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="8" fill="#12352c"/>'
            + MARK.replace('<svg viewBox="0 0 40 40" aria-hidden="true">', '').replace('</svg>', '') + '</svg>')
print("built", len(PAGES), "pages")
