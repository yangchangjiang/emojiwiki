#!/usr/bin/env python3
"""Generate emoji pages for emojiwiki.world"""
import json, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "emojiwiki.world"

with open(os.path.join(BASE, "emojis.json"), "r", encoding="utf-8") as f:
    emojis = json.load(f)
print(f"Loaded {len(emojis)} emojis")

def page_head(title, desc, kw):
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n<meta name="keywords" content="' + kw + '">\n<link rel="canonical" href="https://emojiwiki.world/emoji/{emoji_id}.html">\n'

css = '''<style>:root{--bg:#fff;--surface:#fff;--surface2:#f8fafc;--border:#e2e8f0;--text:#0f172a;--text2:#64748b;--accent:#f59e0b;--accent2:#fbbf24;--accent-bg:#fffbeb;--radius:12px;--shadow:0 1px 3px rgba(0,0,0,.08)}body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;margin:0;padding:0;-webkit-font-smoothing:antialiased}header{background:rgba(255,255,255,0.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:14px 0;position:sticky;top:0;z-index:100}.container{max-width:1100px;margin:0 auto;padding:0 20px}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}nav{display:flex;align-items:center;flex-wrap:wrap;gap:16px}nav a{color:var(--text2);font-size:.9rem;font-weight:500}.logo{font-size:1.2rem;font-weight:700;color:var(--text)}.emoji-display{font-size:6rem;text-align:center;padding:40px;background:var(--accent-bg);border-radius:var(--radius);margin:20px 0;cursor:pointer;user-select:none;transition:background .3s}.emoji-info p{margin:8px 0;font-size:1.05rem}.code-block{background:var(--surface2);padding:8px 14px;border-radius:8px;font-family:monospace;font-size:.9rem;display:inline-block;margin:4px}footer{background:var(--surface2);border-top:1px solid var(--border);padding:30px 0;text-align:center;color:var(--text2);font-size:.85rem;margin-top:60px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px}.emoji-card{text-align:center;padding:15px 10px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);transition:all .2s;box-shadow:var(--shadow)}.emoji-card:hover{transform:translateY(-2px);box-shadow:0 4px 6px rgba(0,0,0,.07);border-color:var(--accent)}.emoji-card .em{font-size:2.5rem;display:block}.emoji-card .label{font-size:.75rem;color:var(--text2);margin-top:6px}.search-box{width:100%;padding:14px 20px;border:2px solid var(--border);border-radius:var(--radius);font-size:1.1rem;outline:none}.search-box:focus{border-color:var(--accent)}</style>'''

header = '<header><div class="container"><nav><a class="logo" href="/">&#x1F60A; EmojiWiki</a><a href="/">Home</a><a href="/about.html">About</a><a href="/privacy.html">Privacy</a></nav></div></header>'
footer = '<footer><div class="container">(c) 2026 EmojiWiki. <a href="/privacy.html">Privacy</a> | <a href="/terms.html">Terms</a></div></footer>'

# Generate emoji pages
emoji_dir = os.path.join(BASE, "en", "emoji")
os.makedirs(emoji_dir, exist_ok=True)

for i, e in enumerate(emojis):
    emoji_id = e["id"]
    emoji_char = e["emoji"]
    name = e["name"]
    cp = e["codepoint"]
    he = e["html_entity"]
    
    title = emoji_char + " " + name + " \u2014 Emoji Copy & Paste | EmojiWiki"
    desc = "Copy and paste the " + emoji_char + " " + name + " emoji. Unicode U+" + cp.upper().replace(" ", " U+").encode("ascii","ignore").decode() + ". Free emoji encyclopedia."
    kw = emoji_char + "," + name + ",emoji,copy emoji," + name + " emoji copy"
    
    html = page_head(title, desc, kw) + ' + css + '</head>\n<body>\n' + header + '\n<main class="container">\n'
    html += '<div style="font-size:.85rem;color:var(--text2);margin:15px 0"><a href="/">Home</a> / ' + emoji_char + ' ' + name + '</div>\n'
    html += '<div class="emoji-display" onclick="var t=this;navigator.clipboard.writeText(this.textContent);t.style.background=\'#d1fae5\';setTimeout(function(){t.style.background=\'\'},800)">' + emoji_char + '</div>\n'
    html += '<h1>' + emoji_char + ' ' + name + '</h1>\n'
    html += '<div class="emoji-info">\n'
    html += '<p>Click the emoji to copy it. &#x1F447;</p>\n'
    html += '<p><strong>Name:</strong> ' + name + '</p>\n'
    html += '<p><strong>Unicode:</strong> <span class="code-block">U+' + cp.upper().replace(" ", " U+") + '</span></p>\n'
    html += '<p><strong>HTML Entity:</strong> <span class="code-block">' + he.replace("&","&amp;") + '</span></p>\n'
    html += '<p><strong>CSS:</strong> <span class="code-block">\\' + cp.upper().replace(" ", "\\") + '</span></p>\n'
    html += '</div>\n'
    html += '</main>\n' + footer + '\n</body>\n</html>'
    
    with open(os.path.join(emoji_dir, emoji_id + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    
    if (i+1) % 500 == 0:
        print(f"  {i+1}/{len(emojis)}")

print(f"  Generated {len(emojis)} emoji pages")

# Generate index
grid = []
for e in emojis[:500]:
    grid.append('<a class="emoji-card" href="/emoji/' + e["id"] + '.html"><span class="em">' + e["emoji"] + '</span><span class="label">' + e["name"][:20] + '</span></a>')

idx_html = page_head("Emoji Copy & Paste \u2014 Free Emoji Encyclopedia | EmojiWiki", 
    "Copy and paste emoji. Browse 3759 emojis with search, unicode, and HTML entities. 100% free online emoji encyclopedia.",
    "emoji,copy emoji,emoji list,emoji copy paste,emoji meaning") + css + '</head>\n<body>\n' + header + '\n'

idx_html += '<main class="container">\n'
idx_html += '<h1>&#x1F60A; Emoji Copy & Paste</h1>\n'
idx_html += '<p>Browse and copy 3,759 emojis. Click any emoji to copy, or search by name.</p>\n'
idx_html += '<input class="search-box" id="search" placeholder="Search emoji..." type="text">\n'
idx_html += '<p style="margin:10px 0"><a href="/emoji/">View all ' + str(len(emojis)) + ' emojis &rarr;</a></p>\n'
idx_html += '<div class="grid">\n' + "\n".join(grid) + '\n</div>\n'
idx_html += '<script>document.getElementById("search").addEventListener("input",function(){var q=this.value.toLowerCase();document.querySelectorAll(".emoji-card").forEach(function(c){c.style.display=c.querySelector(".label").textContent.toLowerCase().includes(q)?"":"none"})})</script>\n'
idx_html += '</main>\n' + footer + '\n</body>\n</html>'

with open(os.path.join(BASE, "en", "index.html"), "w", encoding="utf-8") as f:
    f.write(idx_html)
print("  Generated index page")

# Copy static pages
for fname in ["about.html", "privacy.html", "terms.html", "cookie-consent.js"]:
    src = "E:/hermesworkspace/unitconvert/" + fname
    dst = os.path.join(BASE, fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print("  Copied " + fname)

print("\nDone!")
