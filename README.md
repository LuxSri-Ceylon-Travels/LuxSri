# LuxSri Ceylon Travels website

Hand-coded static site for https://www.luxsri.lk, replacing the Google Sites version.
Same page addresses as before, so existing Google results and shared links keep working:
`/`, `/private-driver-sri-lanka/`, `/sri-lanka-tour-packages/`, `/luxsri-journey/` (old `/home` redirects to `/`).

## What's in it
- 5 pages (Home, Private Driver, Tour Packages, Journey Gallery, Contact/Booking) + 404, mobile-first, no frameworks, one CSS and one small JS file
- Floating "Chat with Mahesh" WhatsApp button on every page
- Enquiry form that opens WhatsApp with the traveller's dates, group size and wishes filled in
- SEO: unique titles and descriptions, canonical URLs, Open Graph share images, TravelAgency / FAQ / TouristTrip structured data, sitemap.xml, robots.txt

## Settings (top of _build/build.py)
- `WEB3FORMS_KEY` + `BOOKING_EMAIL`: email booking form (free key from web3forms.com, made with the booking email)
- `INSTAGRAM_FEED_URL`: Behold JSON feed for the live Instagram strip
- `GOOGLE_REVIEWS_URL`, `GOOGLE_WRITE_REVIEW_URL`, `REVIEWS_WIDGET`: Google reviews section (Trustindex free widget)
Rebuild: `python3 _build/build.py .` from the site folder (copy site.css/site.js from _build into assets/ first).

## Before launch
1. Photos: right now images load from the old Google Site. Run `get-images.ps1` (or add photos from Downloads\LuxSri into `assets/img/`), then rebuild with `LOCAL_IMAGES=1`.
2. Logo: replace the placeholder monogram with the real logo.
3. Optional: add an email address, guest reviews and "from" prices.

## Going live (GitHub Pages)
1. Push these files to the repo, enable Pages (Settings > Pages > Deploy from branch `main`, root).
2. Custom domain `www.luxsri.lk` (the CNAME file is included), tick Enforce HTTPS.
3. At the domain registrar: `www` CNAME -> `<github-user>.github.io`; apex `luxsri.lk` A records -> 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153. This also fixes bare luxsri.lk, which does not resolve today.
4. Submit the sitemap in Google Search Console.
