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
- Header and footer: Elementor styles each page's header/footer by its own element IDs (`post-XX.css`), so they live inside each page file and are NOT shared. When changing the menu, phone or footer, apply the change in every page.
- Your own styles: `src/assets/css/custom.css`.

## Forms (pending)

Contact, newsletter and Libro de Reclamaciones were WordPress/PHP forms. There is no backend here. `assets/js/forms.js` intercepts every `<form>` and POSTs it to the URL configured in `src/site.json` (`forms.contact`, `forms.newsletter`, `forms.libro`).
- TODO: create a Formspree (or similar) endpoint per form and paste its URL in `site.json`. While empty, users see a notice with the contact email.
- The Provincia/Distrito selects of the Libro de Reclamaciones used `admin-ajax.php` and do not work without PHP.

## Not cloned

- WordPress admin, REST API, search, comments (`wp-json`, `admin-ajax`, `xmlrpc` URLs are replaced by `#`).
- The Intranet button points to the live external site `https://rrhh.corporacionyanayacu.com/login`.

## Deploy (GitHub Pages)

Publish the contents of `dist/` (for example with a GitHub Actions workflow that runs `npm run build` and deploys `dist/`). `.gitignore` excludes the old WordPress files so only the clone is versioned.

## Re-importing from the live site

`python -I tools/clone-site.py` overwrites `src/pages/*` and `src/assets/site/*` (your manual edits there are lost).
