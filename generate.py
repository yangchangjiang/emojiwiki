#!/usr/bin/env python3
"""Generate emoji pages for emojiwiki.world"""
import json, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "emojiwiki.world"
LANGS = ["en","zh-CN","ja","ko","es","pt","fr","de","ar","hi","th","vi","id","ru"]

print("Loading emojis...")
with open(os.path.join(BASE, "emojis.json"), "r", encoding="utf-8") as f:
    emojis = json.load(f)
print(f"  {len(emojis)} emojis loaded")

# Read base template
with open(os.path.join(BASE, "base.html"), "r", encoding="utf-8") as f:
    base_template = f.read()

# Generate emoji page html
def gen_emoji_page(e):
    """Generate HTML for a single emoji page"""
    emoji = e["emoji"]
    name = e["name"]
    emoji_id = e["id"]
    codepoint = e["codepoint"]
    html_entity = e["html_entity"]
    
    title = f"{emoji} {name} — Emoji Copy & Paste | EmojiWiki"
    desc = f"Copy and paste the {emoji} {name} emoji. Unicode: U+{codepoint.upper().replace(' ', ' U+')}. HTML Entity: {html_entity}. Get {emoji} emoji meaning and usage."
    
    content = f'''<div class="breadcrumb"><a href="/{{lang_path}}/">Home</a> / {emoji} {name}</div>
<div class="emoji-display">{emoji}</div>
<h1>{emoji} {name}</h1>
<div class="emoji-info">
<p>Click the emoji to copy it to your clipboard.</p>
<p><strong>Name:</strong> {name}</p>
<p><strong>Unicode:</strong> <span class="code-block">U+{codepoint.upper().replace(' ', ' U+')}</span></p>
<p><strong>HTML Entity:</strong> <span class="code-block">{html_entity}</span></p>
<p><strong>CSS:</strong> <span class="code-block">\\{codepoint.upper().replace(' ', '\\')}</span></p>
</div>'''
    
    return title, desc, content

# Create all emoji pages (only EN for now — lang dirs handled by build_final)
print("Generating emoji pages...")
emoji_dir = os.path.join(BASE, "en", "emoji")
os.makedirs(emoji_dir, exist_ok=True)

for i, e in enumerate(emojis):
    title, desc, content = gen_emoji_page(e)
    emoji_id = e["id"]
    
    html = base_template.replace("{meta_section}", f'''<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{e['emoji']},{e['name']},emoji,copy emoji,{e['name']} emoji copy">
<link rel="canonical" href="https://{DOMAIN}/en/emoji/{emoji_id}.html">''')
    
    html = html.replace("{content}", content)
    html = html.replace("{scripts}", f'''<script>
document.querySelector('.emoji-display').addEventListener('click',function(){{
navigator.clipboard.writeText('{e["emoji"]}');
var t=this;t.style.background='#d1fae5';
setTimeout(function(){{t.style.background='';}},800);
}});
</script>''')
    html = html.replace("{lang_path}", "en")
    
    with open(os.path.join(emoji_dir, f"{emoji_id}.html"), "w", encoding="utf-8") as f:
        f.write(html)
    
    if (i+1) % 500 == 0:
        print(f"  {i+1}/{len(emojis)}")

print(f"  ✓ {len(emojis)} emoji pages generated")

# Generate index page
print("Generating index page...")
grid_items = []
for e in emojis[:500]:  # First 500 emojis
    grid_items.append(f'''<a class="emoji-card" href="/en/emoji/{e['id']}.html"><span class="em">{e['emoji']}</span><span class="label">{e['name'][:20]}</span></a>''')

index_title = "Emoji Copy & Paste — Free Emoji Encyclopedia | EmojiWiki"
index_desc = "Copy and paste emoji. Browse 3,759 emojis with search, categories, unicode, and HTML entities. 100% free."
index_html = base_template.replace("{meta_section}", f'''<title>{index_title}</title>
<meta name="description" content="{index_desc}">
<meta name="keywords" content="emoji,copy emoji,emoji list,emoji copy paste,emoji meaning">
<link rel="canonical" href="https://{DOMAIN}/">''')
index_html = index_html.replace("{lang_path}", "en")
index_html = index_html.replace("{scripts}", '''<script>
document.getElementById('emojiSearch').addEventListener('input',function(){
var q=this.value.toLowerCase();
document.querySelectorAll('.emoji-card').forEach(function(c){
c.style.display=c.querySelector('.label').textContent.toLowerCase().includes(q)?'':'none';
});
});
</script>''')
index_html = index_html.replace("{content}", f'''<h1>😊 Emoji Copy & Paste</h1>
<p>Browse and copy 3,759 emojis. Click any emoji to copy it, or search by name.</p>
<input class="search-box" id="emojiSearch" placeholder="Search emoji..." type="text">
<div class="grid">{''.join(grid_items)}</div>
<p style="text-align:center;margin-top:20px"><a href="/en/emoji/">View all 3,759 emojis →</a></p>''')

os.makedirs(os.path.join(BASE, "en"), exist_ok=True)
with open(os.path.join(BASE, "en", "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)
print("  ✓ index page generated")

# Copy about, privacy, terms from unitconvert
for fname in ["about.html", "privacy.html", "terms.html", "cookie-consent.js"]:
    src = f"E:/hermesworkspace/unitconvert/{fname}"
    dst = os.path.join(BASE, fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)

print("  ✓ Static pages copied")
print("\n✅ Generation complete")
