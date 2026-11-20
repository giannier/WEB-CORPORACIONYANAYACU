#!/usr/bin/env python3
"""
One-off importer: mirrors the rendered WordPress/Elementor pages of corporacionyanayacu.com
into src/ (pages + assets) so the site can be edited as code.

Usage (from the project root):  python -I tools/clone-site.py

- Assets are taken from the local WordPress copy (wp-content/, wp-includes/) when the file exists,
  otherwise downloaded from the live site.
- Every absolute URL of the live site is rewritten to {{root}}assets/site/... (or {{root}}<page>/).
- WordPress-only endpoints (wp-json, admin-ajax, xmlrpc) are replaced by "#".
Re-running it overwrites src/pages/* and src/assets/site/*.
"""
import os, re, sys, shutil, hashlib, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "corporacionyanayacu.com"
LIVE = "https://" + HOST
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
SRC = os.path.join(ROOT, "src")
ASSETS = os.path.join(SRC, "assets", "site")
PAGES = {  # slug -> (output file, title fallback)
    "": "index", "nosotros": "nosotros", "agro": "agro", "construccion": "construccion",
    "servicios-generales": "servicios-generales", "marcas": "marcas", "contacto": "contacto",
    "libro-de-reclamaciones": "libro-de-reclamaciones",
}
missing, fetched = [], set()


def http(url, binary=True):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else data.decode("utf8", "replace")


def local_target(path):
    return os.path.join(ASSETS, *path.strip("/").split("/"))


def ensure(path):
    """Make sure /wp-content/... exists under src/assets/site. Returns local file path or None."""
    path = urllib.parse.unquote(path)
    dst = local_target(path)
    if path in fetched:
        return dst if os.path.exists(dst) else None
    fetched.add(path)
    if path.endswith("/") or not os.path.splitext(path)[1]:
        return None
    if os.path.exists(dst):
        return dst
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    srcfile = os.path.join(ROOT, *path.strip("/").split("/"))
    try:
        if os.path.isfile(srcfile):
            shutil.copy2(srcfile, dst)
        else:
            with open(dst, "wb") as f:
                f.write(http(LIVE + urllib.parse.quote(path)))
    except Exception as e:  # noqa
        missing.append(f"{path} ({e})")
        return None
    if dst.endswith(".css"):
        process_css(path, dst)
    return dst


def google_font_css(url):
    """Download a Google Fonts stylesheet + its woff2 files; return the site-root-relative path of the local CSS."""
    url = url.replace("&#038;", "&").replace("&amp;", "&")
    name = hashlib.md5(url.encode()).hexdigest()[:10]
    rel = f"fonts/{name}.css"
    dst = os.path.join(ASSETS, "fonts", f"{name}.css")
    if os.path.exists(dst):
        return rel
    os.makedirs(os.path.join(ASSETS, "fonts", "files"), exist_ok=True)
    try:
        css = http(url, binary=False)
    except Exception as e:  # noqa
        missing.append(f"{url} ({e})")
        return None

    def sub(m):
        u = m.group(1).strip("'\"")
        fn = hashlib.md5(u.encode()).hexdigest()[:12] + os.path.splitext(urllib.parse.urlparse(u).path)[1]
        fp = os.path.join(ASSETS, "fonts", "files", fn)
        if not os.path.exists(fp):
            try:
                open(fp, "wb").write(http(u))
            except Exception as e:  # noqa
                missing.append(f"{u} ({e})")
        return f"url(files/{fn})"

    css = re.sub(r"url\(([^)]+)\)", sub, css)
    open(dst, "w", encoding="utf8").write(css)
    return rel


def process_css(url_path, dst):
    """Rewrite absolute live URLs in a CSS file to relative ones and fetch everything it references."""
    css = open(dst, encoding="utf8", errors="replace").read()
    base = LIVE + url_path

    def fix(m):
        raw = m.group(1).strip().strip("'\"")
        if raw.startswith("data:") or raw.startswith("#"):
            return m.group(0)
        absu = urllib.parse.urljoin(base, raw)
        p = urllib.parse.urlparse(absu)
        if p.netloc.replace("www.", "") == HOST:
            ensure(p.path)
            rel = os.path.relpath(local_target(urllib.parse.unquote(p.path)), os.path.dirname(dst)).replace(os.sep, "/")
            return f"url({rel}{('?' + p.query) if False else ''})"
        if p.netloc in ("fonts.gstatic.com",):
            fn = hashlib.md5(absu.encode()).hexdigest()[:12] + os.path.splitext(p.path)[1]
            fp = os.path.join(ASSETS, "fonts", "files", fn)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            if not os.path.exists(fp):
                try:
                    open(fp, "wb").write(http(absu))
                except Exception as e:  # noqa
                    missing.append(f"{absu} ({e})")
            rel = os.path.relpath(fp, os.path.dirname(dst)).replace(os.sep, "/")
            return f"url({rel})"
        return m.group(0)

    new = re.sub(r"url\(\s*([^)]+?)\s*\)", fix, css)

    def fiximport(m):
        u = m.group(1)
        if "fonts.googleapis.com" in u:
            rel = google_font_css(u)
            if rel:
                return '@import url("%s");' % os.path.relpath(os.path.join(ASSETS, rel), os.path.dirname(dst)).replace(os.sep, "/")
        return m.group(0)

    new = re.sub(r"@import\s+url\(['\"]?([^)'\"]+)['\"]?\)\s*;", fiximport, new)
    if new != css:
        open(dst, "w", encoding="utf8").write(new)


# ---------------------------------------------------------------- HTML rewriting
URL_RE = re.compile(
    r"https?:(?:\\?/){2}(?:www\.)?" + re.escape(HOST) + r"((?:\\?/[^\s\"'<>()\\,?#&;/]*)*)(\?[^\s\"'<>()\\,]*)?")
SLUGS = {k for k in PAGES if k}


def rewrite(text):
    def sub(m):
        escaped = "\\/" in m.group(0)
        path = (m.group(1) or "").replace("\\/", "/")
        out = None
        if re.match(r"^/(wp-json|xmlrpc|wp-admin|wp-comments|feed|comments)", path) or "admin-ajax" in path:
            out = "#"
        elif path.startswith("/wp-content/") or path.startswith("/wp-includes/"):
            ensure(path)
            out = "{{root}}assets/site" + path
        elif path in ("", "/"):
            out = "{{root}}"
        elif path.strip("/") in SLUGS:
            out = "{{root}}" + path.strip("/") + "/"
        if out is None:
            return m.group(0)
        return out.replace("/", "\\/") if escaped else out

    return URL_RE.sub(sub, text)


def split_head_body(html):
    h = re.search(r"<head[^>]*>(.*?)</head>", html, re.S)
    b = re.search(r"<body([^>]*)>(.*)</body>", html, re.S)
    return h.group(1), b.group(1), b.group(2)


DROP_LINK = re.compile(r"rel=[\"'](?:shortlink|canonical|EditURI|wlwmanifest|alternate|profile|https://api\.w\.org/|dns-prefetch|preconnect)[\"']", re.I)
DROP_META = re.compile(r"name=[\"'](?:generator|robots)[\"']", re.I)


def clean_head(head):
    head = re.sub(r"<title>.*?</title>", "", head, flags=re.S)
    head = re.sub(r"<link\b[^>]*>", lambda m: "" if DROP_LINK.search(m.group(0)) else m.group(0), head)
    head = re.sub(r"<meta\b[^>]*>", lambda m: "" if DROP_META.search(m.group(0)) or "charset" in m.group(0) or "viewport" in m.group(0) else m.group(0), head)
    head = re.sub(r"<script\b[^>]*>(?:(?!</script>).)*?(?:_wpemojiSettings|wp-emoji)(?:(?!</script>).)*?</script>", "", head, flags=re.S)
    head = re.sub(r"<script\b[^>]*wp-embed[^>]*></script>", "", head)
    head = re.sub(r"<style[^>]*id=[\"']wp-emoji-styles[^>]*>.*?</style>", "", head, flags=re.S)

    # Google Fonts stylesheets -> local copies
    def gf(m):
        tag = m.group(0)
        href = re.search(r"href=[\"']([^\"']+)[\"']", tag)
        if href and "fonts.googleapis.com" in href.group(1):
            rel = google_font_css(href.group(1))
            if rel:
                return f'<link rel="stylesheet" href="{{{{root}}}}assets/site/{rel}">'
        return tag

    head = re.sub(r"<link\b[^>]*>", gf, head)
    return re.sub(r"\n\s*\n+", "\n", head).strip()


def split_scripts(body):
    scripts = []

    def grab(m):
        s = m.group(0)
        if "wp-emoji" in s or "_wpemojiSettings" in s or "wp-embed" in s:
            return ""
        scripts.append(s)
        return ""

    body = re.sub(r"<script\b[^>]*>.*?</script>", grab, body, flags=re.S)
    return body, "\n".join(scripts)


def copy_runtime_dirs():
    """Elementor lazy-loads chunks at runtime, so ship whole js/ and lib/ trees of the plugins."""
    n = 0
    for plugin in ("elementor", "pro-elements", "jeg-elementor-kit"):
        for sub in ("js", "lib", "css/modules" if plugin == "elementor" else "js"):
            s = os.path.join(ROOT, "wp-content", "plugins", plugin, "assets", sub)
            if not os.path.isdir(s):
                continue
            for r, _, fs_ in os.walk(s):
                for f in fs_:
                    if f.endswith(".map"):
                        continue
                    rel = os.path.relpath(os.path.join(r, f), ROOT)
                    d = os.path.join(ASSETS, rel)
                    if not os.path.exists(d):
                        os.makedirs(os.path.dirname(d), exist_ok=True)
                        shutil.copy2(os.path.join(r, f), d)
                        n += 1
    return n


def main():
    os.makedirs(os.path.join(SRC, "pages"), exist_ok=True)
    for slug, name in PAGES.items():
        html = http(f"{LIVE}/{slug + '/' if slug else ''}", binary=False)
        title = re.search(r"<title>(.*?)</title>", html, re.S).group(1).strip()
        head, battrs, body = split_head_body(html)
        bclass = re.search(r'class="([^"]*)"', battrs)
        bclass = bclass.group(1) if bclass else ""
        head = rewrite(clean_head(head))
        body, scripts = split_scripts(body)
        body = rewrite(body)
        scripts = rewrite(scripts)
        # Scripts that were in <head> (jQuery etc.) stay in head; ones in body go to the "scripts" slot.
        fm = f"---\ntitle: {title.replace('&#8211;', '–')}\nbody_class: {bclass}\n---\n"
        page = f"{fm}{body.strip()}\n\n<!-- @slot head -->\n{head}\n\n<!-- @slot scripts -->\n{scripts}\n"
        open(os.path.join(SRC, "pages", name + ".html"), "w", encoding="utf8").write(page)
        print("page", slug or "/", len(page))
    # Pull in every asset referenced by the generated pages (images inside CSS were fetched by process_css)
    n = copy_runtime_dirs()
    print("runtime files copied:", n)
    if missing:
        print("\nMISSING:")
        for m in sorted(set(missing)):
            print("  ", m)


if __name__ == "__main__":
    main()
