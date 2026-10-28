r"""Build the offline search index for the Survival Library.
Reads every PDF under "Survival Library", extracts text page by page (pypdf),
splits it into overlapping chunks and saves index\chunks.json.
Run with: Rebuild library index.bat   (fully offline)."""
import os, sys, re, json, csv, time
HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(HERE)
KIT = os.path.dirname(AI)
LIB = os.path.join(KIT, "Survival Library")
sys.path.insert(0, os.path.join(AI, "app", "pylib"))
import logging
logging.disable(logging.WARNING)
from pypdf import PdfReader

CHUNK_WORDS, OVERLAP = 170, 40

def clean(t):
    t = t.replace("\u00ad", "").replace("\ufb01", "fi").replace("\ufb02", "fl")
    t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)          # re-join hyphenated line breaks
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()

def titles():
    m = {}
    p = os.path.join(LIB, "MANIFEST.csv")
    if os.path.exists(p):
        with open(p, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                fp = (r.get("file") or "").replace("/", os.sep).replace("\\", os.sep)
                if fp: m[os.path.normcase(fp)] = r.get("title") or ""
    return m

def main():
    t0 = time.time()
    tmap = titles()
    chunks, files = [], []
    for root, _, names in os.walk(LIB):
        for n in sorted(names):
            if not n.lower().endswith(".pdf"): continue
            full = os.path.join(root, n)
            rel = os.path.relpath(full, LIB)
            title = tmap.get(os.path.normcase(rel)) or os.path.splitext(n)[0]
            folder = os.path.dirname(rel)
            try:
                rd = PdfReader(full)
                pages = len(rd.pages)
            except Exception as e:
                print("SKIP (cannot open):", rel, e); continue
            words_total = 0
            buf = []  # list of (word, page)
            for pi in range(pages):
                try:
                    txt = clean(rd.pages[pi].extract_text() or "")
                except Exception:
                    txt = ""
                for w in txt.split():
                    buf.append((w, pi + 1))
            words_total = len(buf)
            i = 0
            while i < len(buf):
                seg = buf[i:i + CHUNK_WORDS]
                if len(seg) < 25 and i > 0: break
                chunks.append({"file": rel, "title": title, "folder": folder,
                               "page": seg[0][1], "text": " ".join(w for w, _ in seg)})
                i += CHUNK_WORDS - OVERLAP
            files.append({"file": rel, "title": title, "pages": pages, "words": words_total})
            print(f"{pages:4d} pages {words_total:7d} words  {rel}")
    os.makedirs(os.path.join(HERE, "index"), exist_ok=True)
    out = os.path.join(HERE, "index", "chunks.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"built": time.strftime("%Y-%m-%d %H:%M"), "files": files, "chunks": chunks}, f, ensure_ascii=False)
    empty = [x["file"] for x in files if x["words"] < 50]
    print(f"\n{len(files)} PDFs, {len(chunks)} chunks, {time.time()-t0:.0f}s -> {out}")
    if empty: print("WARNING: little or no text (scanned?) in:", *empty, sep="\n  ")

if __name__ == "__main__":
    main()
