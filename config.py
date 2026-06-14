#!/usr/bin/env python3
"""EmojiWiki configuration"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "emojiwiki.world"

SITE = {
    "name": "EmojiWiki",
    "description": "Copy and paste emoji — Free online emoji encyclopedia",
    "domain": "emojiwiki.world",
    "theme": "#f59e0b",
}

LANGS = ["en","zh-CN","ja","ko","es","pt","fr","de","ar","hi","th","vi","id","ru"]

OG_LOCALE = {
    "en":"en_US","zh-CN":"zh_CN","ja":"ja_JP","ko":"ko_KR",
    "es":"es_ES","pt":"pt_BR","fr":"fr_FR","de":"de_DE",
    "ar":"ar_SA","hi":"hi_IN","th":"th_TH","vi":"vi_VN",
    "id":"id_ID","ru":"ru_RU",
}
