
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
from io import BytesIO
import os
import re

st.set_page_config(page_title="Thumbnail Mockup Generator", layout="centered")

st.markdown("🎯 **Thumbnail Mockup Generator**", unsafe_allow_html=True)

thumb_file = st.file_uploader("Upload Thumbnail (1920x1080)", type=["jpg", "jpeg", "png"])
channel_url = st.text_input("YouTube Channel or Video Link")
title = st.text_input("Video Title")

def get_channel_info(link):
    channel_name = "Channel Name"
    subscribers = "1M subscribers"
    match = re.search(r"@([a-zA-Z0-9_]+)", link)
    if match:
        name = match.group(1)
        channel_name = name[0].upper() + name[1:]
    if "mrbeast" in link.lower():
        channel_name = "MrBeast"
        subscribers = "382M subscribers"
    elif "willibed" in link.lower():
        channel_name = "Willibed"
        subscribers = "1.39M subscribers"
    return channel_name, subscribers

def round_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def draw_text(draw, text, position, font, fill):
    draw.text(position, text, font=font, fill=fill)

if thumb_file and title and channel_url:
    thumb = Image.open(thumb_file).convert("RGB").resize((1328, 747))
    thumb = round_corners(thumb, 36)

    canvas = Image.new("RGB", (1400, 980), "black")
    canvas.paste(thumb, (36, 36), thumb)

    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 62)
        font_meta = ImageFont.truetype("DejaVuSans.ttf", 44)
    except:
        font_title = ImageFont.load_default()
        font_meta = ImageFont.load_default()

    draw_text(draw, title, (66, 835), font_title, "white")

    channel_name, subs = get_channel_info(channel_url)

    subs = subs.replace(".00", "") if ".00" in subs else subs

    profile_box = Image.new("RGB", (1220, 100), (32, 32, 32))
    profile_box = ImageOps.expand(profile_box, border=30, fill="black")
    profile_box = round_corners(profile_box, 60)
    canvas.paste(profile_box, (66, 900), profile_box)

    try:
        pfp = Image.open("pfp.jpg").resize((87, 87)).convert("RGBA")
        mask = Image.new("L", (87, 87), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 87, 87), fill=255)
        pfp.putalpha(mask)
        canvas.paste(pfp, (96, 930), pfp)
    except:
        pass

    draw_text(draw, channel_name, (210, 945), font_meta, "white")
    draw_text(draw, subs, (980, 945), font_meta, "lightgray")

    st.image(canvas, caption="Mockup Output", use_container_width=True)
    st.success("Mockup generated successfully!")
