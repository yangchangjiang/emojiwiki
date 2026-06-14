#!/usr/bin/env python3
"""i18n-aware emoji page generator"""
import json, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
PREFIX = "/emojiwiki"

with open(os.path.join(BASE, "emojis.json"), "r", encoding="utf-8") as f:
    emojis = json.load(f)

CSS = '<style>:root{--bg:#fff;--surface:#fff;--surface2:#f8fafc;--border:#e2e8f0;--text:#0f172a;--text2:#64748b;--accent:#f59e0b;--accent2:#fbbf24;--accent-bg:#fffbeb;--radius:12px;--shadow:0 1px 3px rgba(0,0,0,.08)}body{font-family:system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;margin:0;padding:0}header{background:rgba(255,255,255,0.95);backdrop-filter:blur(12px);border-bottom:1px solid var(--border);padding:14px 0;position:sticky;top:0;z-index:100}.container{max-width:1100px;margin:0 auto;padding:0 20px}a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}nav{display:flex;align-items:center;flex-wrap:wrap;gap:16px}nav a{color:var(--text2);font-size:.9rem;font-weight:500}.logo{font-size:1.2rem;font-weight:700;color:var(--text)}.emoji-display{font-size:6rem;text-align:center;padding:40px;background:var(--accent-bg);border-radius:var(--radius);margin:20px 0;cursor:pointer;user-select:none}.emoji-info p{margin:8px 0;font-size:1.05rem}.code-block{background:var(--surface2);padding:8px 14px;border-radius:8px;font-family:monospace;font-size:.9rem;display:inline-block;margin:4px}footer{background:var(--surface2);border-top:1px solid var(--border);padding:30px 0;text-align:center;color:var(--text2);font-size:.85rem;margin-top:60px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px}.emoji-card{text-align:center;padding:15px 10px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);transition:all .2s;box-shadow:var(--shadow)}.emoji-card:hover{transform:translateY(-2px);box-shadow:0 4px 6px rgba(0,0,0,.07);border-color:var(--accent)}.emoji-card .em{font-size:2.5rem;display:block}.emoji-card .label{font-size:.75rem;color:var(--text2);margin-top:6px}.search-box{width:100%;padding:14px 20px;border:2px solid var(--border);border-radius:var(--radius);font-size:1.1rem;outline:none;box-sizing:border-box}.search-box:focus{border-color:var(--accent)}.breadcrumb{font-size:.85rem;color:var(--text2);margin:15px 0}.language-select{position:relative;display:inline-block}.lang-btn{background:none;border:1px solid var(--border);padding:6px 12px;border-radius:8px;cursor:pointer;font-size:.9rem;color:var(--text)}.lang-dropdown{display:none;position:absolute;top:100%;right:0;background:var(--surface);border:1px solid var(--border);border-radius:8px;box-shadow:0 4px 6px rgba(0,0,0,.07);z-index:101;min-width:150px;padding:4px 0}.lang-dropdown.show{display:block}.lang-dropdown button{display:block;width:100%;text-align:left;padding:8px 16px;border:none;background:none;font-size:.9rem;cursor:pointer;color:var(--text)}.lang-dropdown button:hover{background:var(--accent-bg);color:var(--accent)}</style>'

NAV = '<header><div class="container"><nav><a class="logo" href="' + PREFIX + '/en/">&#x1F60A; <span data-i18n="siteName">EmojiWiki</span></a><a href="' + PREFIX + '/en/" data-i18n="navHome">Home</a><a href="' + PREFIX + '/en/about.html" data-i18n="navAbout">About</a><a href="' + PREFIX + '/en/privacy.html" data-i18n="navPrivacy">Privacy</a></nav></div></header>'

FOOTER = '<footer><div class="container"><span data-i18n="footer">&#xa9; 2026 EmojiWiki</span></div></footer>'

def make_head(title, desc, kw, canonical):
    return '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1.0">\n<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n<meta name="keywords" content="' + kw + '">\n<link rel="canonical" href="' + canonical + '">\n' + CSS

def make_emoji_page(e):
    head = make_head(
        e["emoji"] + " " + e["name"] + " \u2014 Emoji Copy &amp; Paste | EmojiWiki",
        "Copy and paste the " + e["emoji"] + " " + e["name"] + " emoji. Unicode: U+" + e["codepoint"].upper().replace(" ", " U+") + ". Free emoji encyclopedia.",
        e["emoji"] + "," + e["name"] + ",emoji,copy emoji," + e["name"] + " emoji",
        "https://emojiwiki.world/en/emoji/" + e["id"] + ".html"
    )
    cp = e["codepoint"]
    css_cp = "\\" + cp.upper().replace(" ", "\\")
    body = '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + head + '</head>\n<body>\n' + NAV + '\n<main class="container">\n'
    body += '<div class="breadcrumb"><a href="' + PREFIX + '/en/">Home</a> / ' + e["emoji"] + ' ' + e["name"] + '</div>\n'
    body += '<div class="emoji-display" onclick="var t=this;navigator.clipboard.writeText(this.textContent);t.style.background=\'#d1fae5\';setTimeout(function(){t.style.background=\'\'},800)">' + e["emoji"] + '</div>\n'
    body += '<h1>' + e["emoji"] + ' ' + e["name"] + '</h1>\n'
    body += '<div class="emoji-info">\n'
    body += '<p data-i18n="click_to_copy">Click the emoji to copy it. &#x1F447;</p>\n'
    body += '<p><strong data-i18n="name_label">Name</strong>: ' + e["name"] + '</p>\n'
    body += '<p><strong data-i18n="unicode_label">Unicode</strong>: <span class="code-block">U+' + cp.upper().replace(" ", " U+") + '</span></p>\n'
    body += '<p><strong data-i18n="html_entity_label">HTML Entity</strong>: <span class="code-block">' + e["html_entity"].replace("&","&amp;") + '</span></p>\n'
    body += '<p><strong data-i18n="css_label">CSS</strong>: <span class="code-block">' + css_cp + '</span></p>\n'
    body += '</div>\n</main>\n' + FOOTER + '\n<script src="' + PREFIX + '/i18n.js"></script>\n</body>\n</html>'
    return body

print("Generating " + str(len(emojis)) + " emoji pages...")
emoji_dir = os.path.join(BASE, "en", "emoji")
os.makedirs(emoji_dir, exist_ok=True)

for i, e in enumerate(emojis):
    html = make_emoji_page(e)
    with open(os.path.join(emoji_dir, e["id"] + ".html"), "w", encoding="utf-8") as f:
        f.write(html)
    if (i + 1) % 500 == 0:
        print("  " + str(i + 1) + "/" + str(len(emojis)))

print("  Done: " + str(len(emojis)) + " pages")

# Generate i18n index
print("Generating index...")
grid = []
for e in emojis[:500]:
    grid.append('<a class="emoji-card" href="' + PREFIX + '/en/emoji/' + e["id"] + '.html"><span class="em">' + e["emoji"] + '</span><span class="label">' + e["name"][:20] + '</span></a>')

idx = '<!DOCTYPE html>\n<html lang="en">\n<head>\n' + make_head(
    "Emoji Copy &amp; Paste \u2014 Free Emoji Encyclopedia | EmojiWiki",
    "Copy and paste emoji. Browse " + str(len(emojis)) + " emojis with search, unicode, and HTML entities. 100% free.",
    "emoji,copy emoji,emoji list,emoji copy paste,emoji meaning",
    "https://emojiwiki.world/"
) + '</head>\n<body>\n' + NAV + '\n<main class="container">\n'
idx += '<h1 data-i18n="heading">&#x1F60A; Emoji Copy &amp; Paste</h1>\n'
idx += '<p data-i18n="browse_copy">Browse and copy ' + str(len(emojis)) + ' emojis. Click any emoji to copy, or search by name.</p>\n'
idx += '<input class="search-box" id="search" data-i18n-search="search_placeholder" placeholder="Search emoji..." type="text">\n'
idx += '<p><a href="' + PREFIX + '/en/emoji/" data-i18n-v="view_all">View all ' + str(len(emojis)) + ' emojis \u2192</a></p>\n'
idx += '<div class="grid">\n' + "\n".join(grid) + '\n</div>\n'
idx += '</main>\n' + FOOTER + '\n<script src="' + PREFIX + '/i18n.js"></script>\n'
idx += '<script>document.getElementById("search").addEventListener("input",function(){var q=this.value.toLowerCase();document.querySelectorAll(".emoji-card").forEach(function(c){c.style.display=c.querySelector(".label").textContent.toLowerCase().includes(q)?"":"none"})});</script>\n'
idx += '</body>\n</html>'

with open(os.path.join(BASE, "en", "index.html"), "w", encoding="utf-8") as f:
    f.write(idx)
print("  Index done")

# Copy support files
for fname in ["i18n.js"]:
    src = os.path.join(BASE, fname)
    dst = os.path.join(BASE, "en", fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)

print("\nAll done!")
