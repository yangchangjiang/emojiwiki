#!/usr/bin/env python3
"""SEO boost for emojiwiki — long-tail keywords, FAQPage, BreadcrumbList"""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "emojiwiki.world"
LANGS = ["en","zh-CN","ja","ko"]

with open(os.path.join(BASE, "emojis.json"), "r", encoding="utf-8") as f:
    emojis = json.load(f)

emoji_map = {e["id"]: e for e in emojis}

# SEO titles and keywords per language
SEO = {
    "en": {
        "title_tpl": "{emoji} {name} Emoji — Copy & Paste | EmojiWiki",
        "desc_tpl": "Copy and paste {emoji} {name} emoji. Unicode U+{cp}. HTML entity {he}. Free emoji encyclopedia with 3,759 emojis.",
        "kw_tpl": "{name} emoji,{emoji} emoji copy,copy {name} emoji,{name} emoji meaning,emoji {name} copy paste,{name}",
        "faq_q1": "How to copy the {name} emoji?",
        "faq_a1": "Click the {emoji} emoji on this page to copy it to your clipboard instantly.",
        "faq_q2": "What is the Unicode for {name} emoji?",
        "faq_a2": "The Unicode codepoint for {name} emoji is U+{cp}. HTML entity: {he}.",
    },
    "zh-CN": {
        "title_tpl": "{emoji} {name} Emoji — 复制粘贴 | EmojiWiki",
        "desc_tpl": "复制粘贴{emoji} {name} emoji。Unicode: U+{cp}。HTML实体: {he}。免费emoji百科，收录3,759个emoji。",
        "kw_tpl": "{name} emoji,{name} 复制,{name} emoji 复制,emoji {name},表情符号{name}",
        "faq_q1": "如何复制{name} emoji？",
        "faq_a1": "点击页面上的{emoji} emoji 即可复制到剪贴板。",
        "faq_q2": "{name} emoji 的 Unicode 是什么？",
        "faq_a2": "{name} emoji 的 Unicode 码点是 U+{cp}。HTML 实体: {he}。",
    },
    "ja": {
        "title_tpl": "{emoji} {name} 絵文字 — コピー＆ペースト | EmojiWiki",
        "desc_tpl": "{emoji} {name} 絵文字をコピー＆ペースト。Unicode: U+{cp}。HTMLエンティティ: {he}。3,759個の絵文字を収録。",
        "kw_tpl": "{name} 絵文字,{name} コピー,{name} emoji,絵文字 {name},{name} 意味",
        "faq_q1": "{name} 絵文字のコピー方法は？",
        "faq_a1": "ページ上の{emoji} 絵文字をクリックするとクリップボードにコピーされます。",
        "faq_q2": "{name} 絵文字のUnicodeは？",
        "faq_a2": "{name} 絵文字のUnicodeコードポイントは U+{cp} です。HTMLエンティティ: {he}。",
    },
    "ko": {
        "title_tpl": "{emoji} {name} 이모지 — 복사 붙여넣기 | EmojiWiki",
        "desc_tpl": "{emoji} {name} 이모지를 복사 붙여넣기. 유니코드: U+{cp}. HTML 엔티티: {he}. 3,759개 이모지 무료 백과사전.",
        "kw_tpl": "{name} 이모지,{name} 복사,{name} emoji,이모지 {name},{name} 의미",
        "faq_q1": "{name} 이모지 복사 방법은?",
        "faq_a1": "페이지에서 {emoji} 이모지를 클릭하면 클립보드에 복사됩니다.",
        "faq_q2": "{name} 이모지의 유니코드는?",
        "faq_a2": "{name} 이모지의 유니코드 코드포인트는 U+{cp}입니다. HTML 엔티티: {he}.",
    },
}

total = 0
for lang in LANGS:
    seo = SEO[lang]
    emoji_dir = os.path.join(BASE, lang, "emoji")
    if not os.path.exists(emoji_dir): continue
    
    for fname in os.listdir(emoji_dir):
        if not fname.endswith(".html"): continue
        emoji_id = fname.replace(".html", "")
        e = emoji_map.get(emoji_id)
        if not e: continue
        
        path = os.path.join(emoji_dir, fname)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
        
        cp = e["codepoint"].upper().replace(" ", " U+")
        he_escaped = e["html_entity"].replace("&","&amp;")
        
        # Title
        new_title = seo["title_tpl"].format(emoji=e["emoji"], name=e["name"])
        html = re.sub(r'<title>.*?</title>', '<title>' + new_title + '</title>', html)
        
        # Description
        new_desc = seo["desc_tpl"].format(emoji=e["emoji"], name=e["name"], cp=cp, he=he_escaped)
        html = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + new_desc + '">', html)
        
        # Keywords  
        new_kw = seo["kw_tpl"].format(emoji=e["emoji"], name=e["name"], cp=cp, he=he_escaped)
        if '<meta name="keywords"' in html:
            html = re.sub(r'<meta name="keywords" content="[^"]*">', '<meta name="keywords" content="' + new_kw + '">', html)
        
        # FAQPage Schema
        if "FAQPage" not in html:
            faq = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":['
            faq += '{"@type":"Question","name":"' + seo["faq_q1"].format(name=e["name"], emoji=e["emoji"]) + '","acceptedAnswer":{"@type":"Answer","text":"' + seo["faq_a1"].format(name=e["name"], emoji=e["emoji"]) + '"}},'
            faq += '{"@type":"Question","name":"' + seo["faq_q2"].format(name=e["name"], cp=cp, he=he_escaped, emoji=e["emoji"]) + '","acceptedAnswer":{"@type":"Answer","text":"' + seo["faq_a2"].format(name=e["name"], cp=cp, he=he_escaped, emoji=e["emoji"]) + '"}}'
            faq += ']}</script>'
            html = html.replace("</head>", faq + "\n</head>")
        
        # BreadcrumbList
        if "BreadcrumbList" not in html:
            bc = '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":['
            bc += '{"@type":"ListItem","position":1,"name":"Home","item":"https://' + DOMAIN + '/' + lang + '/"},'
            bc += '{"@type":"ListItem","position":2,"name":"' + e["emoji"] + ' ' + e["name"] + '","item":"https://' + DOMAIN + '/' + lang + '/emoji/' + fname + '"}]}</script>'
            html = html.replace("</head>", bc + "\n</head>")
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        total += 1
    
    print(f"  {lang}: {len(os.listdir(emoji_dir))} pages")

print(f"\nSEO applied to {total} pages")

# Generate sitemap
with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for lang in LANGS:
        f.write(f'  <url><loc>https://{DOMAIN}/{lang}/</loc><priority>0.9</priority></url>\n')
        for emoji_id in emoji_map:
            f.write(f'  <url><loc>https://{DOMAIN}/{lang}/emoji/{emoji_id}.html</loc><priority>0.8</priority></url>\n')
    f.write('</urlset>\n')

urls = 4 + len(emoji_map) * 4
print(f"Sitemap: {urls} URLs")
