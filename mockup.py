
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

st.set_page_config(page_title="Thumbnail Mockup Generator", layout="centered")

st.markdown("### 🎯 Thumbnail Mockup Generator")

thumb_file = st.file_uploader("Upload Thumbnail (1920x1080)", type=["jpg", "jpeg", "png"])
channel_url = st.text_input("YouTube Channel or Video Link")
title = st.text_input("Video Title")

if thumb_file and channel_url and title:
    from urllib.parse import urlparse
    import re

    def extract_channel_username(url):
        parsed = urlparse(url)
        return parsed.path.split("/")[-1].replace("@", "")

    def get_mock_subs(channel_name):
        # Dummy values for demo
        return "1.39M" if "Willibed" in channel_name else "382M"

    def round_corners(img, rad):
        circle = Image.new("L", (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new("L", img.size, 255)
        w, h = img.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        img.putalpha(alpha)
        return img

    thumb = Image.open(thumb_file).convert("RGB").resize((1328, 747))
    thumb = round_corners(thumb, 60)

    canvas = Image.new("RGB", (1400, 1100), "#000000")
    canvas.paste(thumb, (36, 40), thumb)

    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    font_channel = ImageFont.truetype("DejaVuSans.ttf", 48)
    font_subs = ImageFont.truetype("DejaVuSans.ttf", 45)

    draw = ImageDraw.Draw(canvas)
    draw.text((66, 835), title, font=font_title, fill="white")

    # Channel section
    channel_name = extract_channel_username(channel_url)
    subs = get_mock_subs(channel_name)
    subs = subs.replace(".00", "") if subs.endswith(".00M") else subs

    # Draw dark rounded box
    box_x, box_y, box_w, box_h = 66, 910, 1268, 100
    box = Image.new("RGBA", (box_w, box_h), (255, 255, 255, 0))
    draw_box = ImageDraw.Draw(box)
    draw_box.rounded_rectangle([(0, 0), (box_w, box_h)], radius=50, fill=(40, 40, 40, 255))
    canvas.paste(box, (box_x, box_y), box)

    # PFP
    pfp = Image.open("pfp.jpg").resize((87, 87)).convert("RGBA")
    mask = Image.new("L", (87, 87), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 87, 87), fill=255)
    canvas.paste(pfp, (box_x + 20, box_y + 7), mask)

    draw.text((box_x + 120, box_y + 28), channel_name, font=font_channel, fill="white")
    text_w = draw.textlength(subs + " subscribers", font=font_subs)
    draw.text((box_x + box_w - text_w - 40, box_y + 30), subs + " subscribers", font=font_subs, fill="lightgray")

    st.image(canvas)
    st.success("Mockup generated successfully!")
