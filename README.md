# Corporación Yanayacu – static site

Static clone of https://corporacionyanayacu.com (WordPress + Elementor + Jeg Elementor Kit). Works offline except Google Fonts files, which are stored locally under `src/assets/site/fonts/`. Requires Node >= 18, no dependencies.

## Commands

```bash
npm run dev     # build + watch + local server with live reload (http://localhost:3000)
npm run build   # generate dist/
npm run watch   # rebuild on save, no server
npm run check   # verify dist/ has no missing assets
```

## Structure

```
src/layouts/base.html     document shell: <head> slot, body, scripts
src/layouts/header.html   SHARED header (top bar, menu, social icons), same on every page
src/layouts/footer.html   SHARED footer (links, Intranet, newsletter, social icons, Libro de Reclamaciones)
src/pages/*.html          one file per page: front matter + Elementor markup + slots (head, scripts)
src/assets/site/          mirrored WordPress files (wp-content, wp-includes, fonts), copied as-is to dist/assets/site/
src/assets/css|js/        your own CSS (custom.css, loaded last) and JS (forms.js)
src/site.json             global values ({{site.*}}), form endpoints
tools/clone-site.py       one-off importer that generated src/pages and src/assets/site from the live site
tools/check-assets.mjs    asset checker used by `npm run check`
```

Page URLs: `src/pages/nosotros.html` -> `dist/nosotros/index.html`. `{{root}}` is the relative path to the site root, so the site works from any sub-folder (GitHub Pages included).

## Editing

- Text, links, images: edit the page in `src/pages/`. The markup is Elementor's rendered HTML.
- Header and footer are shared: edit `src/layouts/header.html` / `footer.html` once. They keep the home page's Elementor IDs, so every page also loads `post-48.css` (the home CSS) to style them. The active menu item is marked automatically by the build.
- Phone, WhatsApp number, e-mail and Intranet URL live in `src/site.json` (`phone`, `phone_wa`, `email`, `intranet`). Use `{{site.phone}}`, `{{site.phone_wa}}`, `{{site.email}}` in pages.
- TikTok: the header/footer link is `https://www.tiktok.com/@somoscorporacionyanayacu` (taken from the original site).
- Your own styles: `src/assets/css/custom.css`.

## Forms (pending)

Contact, newsletter and Libro de Reclamaciones were WordPress/PHP forms. There is no backend here. `assets/js/forms.js` intercepts every `<form>` and POSTs it to the URL configured in `src/site.json` (`forms.contact`, `forms.newsletter`, `forms.libro`).
- TODO: create a Formspree (or similar) endpoint per form and paste its URL in `site.json`. While empty, users see a notice with the contact email.
- The Provincia/Distrito selects of the Libro de Reclamaciones used `admin-ajax.php` and do not work without PHP. `assets/js/libro.js` swaps them for text inputs (same id/name).
- Libro de Reclamaciones: page in `src/pages/libro-de-reclamaciones.html`, styles in `src/assets/css/pages/libro.css`, behaviour in `src/assets/js/libro.js`.

## Not cloned

- WordPress admin, REST API, search, comments (`wp-json`, `admin-ajax`, `xmlrpc` URLs are replaced by `#`).
- The Intranet link (footer) points to the live external site `https://rrhh.corporacionyanayacu.com/login`.

## Deploy (cPanel Git Version Control)

`dist/` is committed on purpose: cPanel only copies files, it does not run npm. `.cpanel.yml` copies `dist/` to `/home/corpor46/public_html/`.

1. Once: cPanel > Git Version Control > Create > clone this repo (SSH with a deploy key, since it is private).
2. Every change: edit `src/` > `npm run build` > commit (`src/` + `dist/`) > `git push`.
3. cPanel > Git Version Control > Manage > Pull or Deploy > *Update from Remote*, then *Deploy HEAD Commit*.

`.htaccess` and `robots.txt` live in `src/public/` and end up in the root of `dist/`. Enable the HTTPS redirect in `.htaccess` once SSL is active, and fill `url` in `src/site.json` for canonical links.

Warning: if `public_html` still holds the old WordPress install, back it up first. Deploying copies over it and does not delete the old files.

## Re-importing from the live site

`python -I tools/clone-site.py` overwrites `src/pages/*` and `src/assets/site/*` (your manual edits there are lost).
