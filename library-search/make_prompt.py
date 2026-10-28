r"""Writes AI\config\system-prompt.txt and the two plain web-UI configs from Survival Library\MANIFEST.csv."""
import os, csv, json
HERE = os.path.dirname(os.path.abspath(__file__)); AI = os.path.dirname(HERE); KIT = os.path.dirname(AI)
LIB = os.path.join(KIT, "Survival Library"); CFG = os.path.join(AI, "config")
rows = list(csv.DictReader(open(os.path.join(LIB, "MANIFEST.csv"), encoding="utf-8-sig")))
rows.sort(key=lambda r: r["file"])
lines = ["Survival Library\\" + r["file"].replace("/", "\\") for r in rows if r.get("file")]
p = ("You are a calm offline survival assistant. Be practical and concise. For medical or life-threatening issues, "
     "give first-aid steps and say when to seek help; the official guides override you. "
     "You cannot open files yourself. The user has an offline Survival Library next to you (start page: Survival Library\\INDEX.html). "
     "In every answer, name the exact guide file (full path from the list below) that the user should open to check the details. "
     "If the user wants you to read a guide, tell them to click the + button (attach) under the chat box and choose that PDF. "
     "For answers that quote the guides automatically, the user can use the Library Chat at http://127.0.0.1:8081.\n"
     "Library guide files:\n" + "\n".join(lines))
p = p.encode("ascii", "replace").decode()
os.makedirs(CFG, exist_ok=True)
open(os.path.join(CFG, "system-prompt.txt"), "w", encoding="ascii", newline="\r\n").write(p + "\n")
for name, mt in (("webui-battery.json", 512), ("webui-plugged-in.json", 1024)):
    json.dump({"systemMessage": p, "max_tokens": mt, "showSystemMessage": False},
              open(os.path.join(CFG, name), "w", encoding="utf-8"))
print("system prompt: %d chars, %d guides" % (len(p), len(lines)))
