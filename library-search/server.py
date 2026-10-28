"""Survival Library chat: tiny offline RAG web app.
Serves http://127.0.0.1:8081 . For each question it searches the pre-extracted
library text (BM25), sends the best passages + their file paths to the local
llama-server (http://127.0.0.1:8080) and streams back a cited answer.
No internet, no installs; Python standard library only."""
import os, sys, re, json, math, time, traceback, argparse, urllib.request, urllib.parse, threading
from collections import Counter, defaultdict
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
AI = os.path.dirname(HERE)
KIT = os.path.dirname(AI)
LIB = os.path.join(KIT, "Survival Library")

ap = argparse.ArgumentParser()
ap.add_argument("--port", type=int, default=8081)
ap.add_argument("--llama", default="http://127.0.0.1:8080")
ap.add_argument("--k", type=int, default=4, help="passages per question")
ap.add_argument("--max-tokens", type=int, default=512)
ap.add_argument("--mode", default="battery")
ap.add_argument("--pidfile", default="")
ARGS = ap.parse_args()

STOP = set("""a an the and or of to in on for with without is are was were be been being it its this that these those
as at by from into than then there their they them you your yours we our us i me my he she his her not no do does did
can could should would will shall may might must have has had how what when where which who whom why if so such about
over under up down out off very more most any all some each other also just only own same too s t don now get got use
using used make made one two per via etc""".split())

def stem(w):
    for suf in ("ations", "ation", "ings", "ing", "edly", "ies", "ied", "es", "ed", "ly", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf in ("ies", "ied") else "")
    return w

def toks(text):
    return [stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP and len(w) > 1]

# ---------- load index ----------
with open(os.path.join(HERE, "index", "chunks.json"), encoding="utf-8") as f:
    IDX = json.load(f)
CH = IDX["chunks"]
DOCS, DF, TITLES = [], Counter(), []
for c in CH:
    tf = Counter(toks(c["title"] + " " + c["text"]))
    DOCS.append((tf, sum(tf.values())))
    TITLES.append(set(toks(c["title"] + " " + c["folder"])))
    DF.update(tf.keys())
N = len(DOCS)
AVG = sum(l for _, l in DOCS) / max(N, 1)
POST = defaultdict(list)
for i, (tf, _) in enumerate(DOCS):
    for t, n in tf.items():
        POST[t].append((i, n))
IDF = {t: math.log(1 + (N - df + 0.5) / (df + 0.5)) for t, df in DF.items()}

def search(q, k=4, per_file=2):
    qt = Counter(toks(q))
    sc = defaultdict(float)
    k1, b = 1.4, 0.75
    for t, qn in qt.items():
        idf = IDF.get(t)
        if not idf: continue
        for i, n in POST[t]:
            dl = DOCS[i][1]
            sc[i] += idf * n * (k1 + 1) / (n + k1 * (1 - b + b * dl / AVG))
    # boost passages whose guide title / topic folder matches the question (e.g. "water", "hypothermia")
    for i in list(sc):
        sc[i] += 1.2 * sum(IDF.get(t, 0) for t in qt if t in TITLES[i])
    out, per = [], Counter()
    for i, s in sorted(sc.items(), key=lambda x: -x[1]):
        c = CH[i]
        if per[c["file"]] >= per_file: continue
        per[c["file"]] += 1
        out.append(dict(c, score=round(s, 2)))
        if len(out) >= k: break
    return out

BASE = ("You are a calm offline survival assistant. Be practical and concise. For medical or life-threatening "
        "issues, give first-aid steps and say when to seek help; official guides override you. "
        "Below are numbered EXCERPTS found in the user's offline Survival Library for this question. "
        "Base your answer on them and cite them inline like [1] or [2]. Do not invent facts that are not in the "
        "excerpts; if they do not cover something important, say so briefly and give only widely accepted safety "
        "advice, marked as general advice. Finish with a line 'Check:' naming the most useful guide file path and page.")

def build_messages(history, hits):
    ex = []
    for n, h in enumerate(hits, 1):
        ex.append(f"[{n}] Survival Library\\{h['file']} (page {h['page']})\n{h['text']}")
    sys_msg = BASE + "\n\nEXCERPTS:\n" + ("\n\n".join(ex) if ex else "(no matching excerpts found)")
    msgs = [{"role": "system", "content": sys_msg}]
    # keep only the last few turns to fit the small context
    msgs += [m for m in history if m.get("role") in ("user", "assistant")][-(3 if ARGS.k <= 4 else 5):]
    return msgs

def safe_lib_path(rel):
    rel = urllib.parse.unquote(rel).replace("/", os.sep)
    full = os.path.realpath(os.path.join(LIB, rel))
    if not full.startswith(os.path.realpath(LIB) + os.sep) or not full.lower().endswith(".pdf"):
        return None
    return full if os.path.isfile(full) else None

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def log_message(self, *a): pass

    def send(self, code, body, ctype="application/json"):
        if isinstance(body, (dict, list)): body = json.dumps(body).encode()
        elif isinstance(body, str): body = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(body)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self.send(200, f.read(), "text/html; charset=utf-8")
        if u.path == "/api/info":
            return self.send(200, {"mode": ARGS.mode, "files": len(IDX["files"]), "chunks": N, "built": IDX.get("built")})
        if u.path == "/api/search":
            q = urllib.parse.parse_qs(u.query).get("q", [""])[0]
            return self.send(200, search(q, 8))
        if u.path.startswith("/pdf/"):
            full = safe_lib_path(u.path[5:])
            if not full: return self.send(404, {"error": "not found"})
            with open(full, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Content-Disposition", "inline; filename*=UTF-8''" + urllib.parse.quote(os.path.basename(full)))
            self.end_headers()
            try: self.wfile.write(data)
            except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError): pass
            return
        return self.send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/chat": return self.send(404, {"error": "not found"})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except Exception:
            return self.send(400, {"error": "bad json"})
        hist = req.get("messages", [])
        users = [m["content"] for m in hist if m.get("role") == "user"]
        if not users: return self.send(400, {"error": "no question"})
        q = users[-1] + (" " + users[-2] if len(users) > 1 and len(users[-1].split()) < 8 else "")
        hits = search(q, ARGS.k)
        body = {"messages": build_messages(hist, hits), "stream": bool(req.get("stream", True)),
                "max_tokens": ARGS.max_tokens, "timings_per_token": False}
        sources = [{"n": i + 1, "file": h["file"], "title": h["title"], "page": h["page"],
                    "path": "Survival Library\\" + h["file"]} for i, h in enumerate(hits)]
        try:
            r = urllib.request.urlopen(urllib.request.Request(ARGS.llama + "/v1/chat/completions",
                    data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=600)
        except Exception as e:
            return self.send(502, {"error": "The AI engine is not running or still loading (%s). Start it with a Start Survival AI launcher." % e,
                                   "sources": sources})
        if not body["stream"]:
            data = json.loads(r.read())
            data["sources"] = sources
            return self.send(200, data)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(("data: " + json.dumps({"sources": sources}) + "\n\n").encode()); self.wfile.flush()
        try:
            for line in r:
                self.wfile.write(line); 
                if line.strip() == b"": self.wfile.flush()
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            r.close()

def log(msg):
    try:
        with open(os.path.join(AI, "logs", "library-chat.log"), "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + msg + "\n")
    except Exception:
        pass

class Srv(ThreadingHTTPServer):
    daemon_threads = True
    def handle_error(self, request, client_address):
        log("request error: " + traceback.format_exc().strip().splitlines()[-1])

if __name__ == "__main__":
    # Runs until "Stop Survival AI.bat" ends it. If the server loop ever fails it restarts itself.
    if ARGS.pidfile:
        with open(ARGS.pidfile, "w") as f: f.write(str(os.getpid()))
    log(f"start on 127.0.0.1:{ARGS.port} mode={ARGS.mode} guides={len(IDX['files'])} passages={N}")
    while True:
        try:
            srv = Srv(("127.0.0.1", ARGS.port), H)
            if sys.stdout: print(f"Survival Library chat on http://127.0.0.1:{ARGS.port}  ({len(IDX['files'])} guides, {N} passages)")
            srv.serve_forever()
        except KeyboardInterrupt:
            break
        except Exception:
            log("server loop error, restarting: " + traceback.format_exc().strip().splitlines()[-1])
            time.sleep(2)
