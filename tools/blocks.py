"""Helpers: split an Elementor page body into its top-level blocks (children of the .elementor wrapper)."""
import re
VOID = {"meta","link","img","br","hr","input","source","area","base","col","embed","param","track","wbr"}
TOK = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][\w:-]*)((?:\"[^\"]*\"|'[^']*'|[^>\"'])*?)(/?)>", re.S)

def blocks(body):
    """Returns (wrapper_open_end, wrapper_close_start, [(start,end,attrs)]) for the wrapper div."""
    m = re.search(r'<div data-elementor-type="[^"]*"[^>]*>', body)
    if not m:
        return None
    pos, depth, out, start = m.end(), 0, [], None
    for t in TOK.finditer(body, m.end()):
        if t.group(0).startswith("<!--"):
            continue
        close, name, attrs, selfc = t.group(1), t.group(2).lower(), t.group(3), t.group(4)
        if name in VOID or selfc:
            continue
        if not close:
            if depth == 0:
                start, sattrs = t.start(), attrs
            depth += 1
        else:
            if depth == 0:
                return m.end(), t.start(), out, m.start()
            depth -= 1
            if depth == 0:
                out.append((start, t.end(), sattrs))
    return None
