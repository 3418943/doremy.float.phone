#!/usr/bin/env python3
"""Keep PWA and Web Push imagery consistent with the installed Android app icon."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import math

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "android-shell/app/src/main/res/drawable/appicon.png"
PUBLIC = ROOT / "public"

with Image.open(SOURCE) as source:
    source = source.convert("RGBA")
    for size in (192, 512):
        icon = ImageOps.fit(source, (size, size), method=Image.Resampling.LANCZOS)
        icon.save(PUBLIC / f"icon-{size}.png", format="PNG", optimize=True)

# Android notification badges need a simple white mark with a transparent background.
# This follows the Saturn silhouette used by android-shell/res/drawable/ic_stat.xml.
scale = 4
size = 96
badge = Image.new("RGBA", (size * scale, size * scale), (0, 0, 0, 0))
draw = ImageDraw.Draw(badge)
k = lambda n: round(n * scale)
draw.ellipse((k(29), k(26), k(67), k(64)), fill=(255, 255, 255, 255))
orbit = []
theta = math.radians(-27)
for i in range(201):
    a = 2 * math.pi * i / 200
    x, y = 48 * math.cos(a), 16 * math.sin(a)
    orbit.append((k(48 + x * math.cos(theta) - y * math.sin(theta)),
                  k(48 + x * math.sin(theta) + y * math.cos(theta))))
draw.line(orbit, fill=(255, 255, 255, 255), width=k(4), joint="curve")
draw.polygon([(k(73), k(9)), (k(78), k(20)), (k(89), k(25)),
              (k(78), k(30)), (k(73), k(41)), (k(68), k(30)),
              (k(57), k(25)), (k(68), k(20))], fill=(255, 255, 255, 255))
badge.resize((size, size), Image.Resampling.LANCZOS).save(
    PUBLIC / "badge-96.png", format="PNG", optimize=True
)
print("Generated public/icon-192.png, public/icon-512.png, public/badge-96.png")
