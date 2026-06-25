from PIL import Image, ImageDraw, ImageFilter
import math
import random

W, H = 1400, 1180
random.seed(11)

img = Image.new("RGB", (W, H), "#f6f8f4")
draw = ImageDraw.Draw(img)

for y in range(H):
    t = y / H
    r = int(246 * (1 - t) + 229 * t)
    g = int(248 * (1 - t) + 238 * t)
    b = int(244 * (1 - t) + 229 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)

for _ in range(56):
    x = random.randint(-80, W + 60)
    y = random.randint(-80, H + 60)
    rx = random.randint(40, 120)
    ry = random.randint(20, 70)
    color = random.choice([(122, 75, 42, 35), (15, 118, 110, 24), (143, 53, 92, 20)])
    od.ellipse((x - rx, y - ry, x + rx, y + ry), fill=color)

for i in range(14):
    x0 = 90 + i * 94
    od.line((x0, 120, x0 + 440, H - 90), fill=(15, 118, 110, 18), width=2)

img = Image.alpha_composite(img.convert("RGBA"), overlay)
draw = ImageDraw.Draw(img)

wave_points = []
for x in range(80, W - 80, 8):
    y = H * 0.49 + math.sin(x / 34) * 36 + math.sin(x / 13) * 12
    wave_points.append((x, y))
draw.line(wave_points, fill=(15, 118, 110, 230), width=6)

for x, y in wave_points[::11]:
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(15, 118, 110, 245))

node_color = (23, 32, 28, 230)
accent_colors = [(15, 118, 110, 235), (184, 121, 42, 235), (143, 53, 92, 235)]
nodes = [
    (250, 250), (510, 180), (845, 260), (1090, 170),
    (350, 760), (665, 860), (1010, 735), (1165, 500),
    (640, 480), (820, 620)
]
for a, b in [(0, 1), (1, 2), (2, 3), (2, 8), (8, 9), (9, 6), (6, 7), (8, 5), (5, 4), (4, 0), (1, 8)]:
    draw.line((nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]), fill=(23, 32, 28, 90), width=3)

for idx, (x, y) in enumerate(nodes):
    c = accent_colors[idx % len(accent_colors)]
    draw.ellipse((x - 18, y - 18, x + 18, y + 18), fill=c)
    draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=node_color)

def coffee_bean(cx, cy, scale, angle, fill):
    bean = Image.new("RGBA", (220, 150), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bean)
    bd.ellipse((18, 16, 202, 134), fill=fill)
    bd.arc((70, 18, 150, 132), start=88, end=272, fill=(67, 39, 24, 180), width=9)
    bd.arc((78, 22, 158, 128), start=88, end=272, fill=(230, 206, 176, 70), width=3)
    bean = bean.resize((int(220 * scale), int(150 * scale)))
    bean = bean.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    img.alpha_composite(bean, (int(cx - bean.width / 2), int(cy - bean.height / 2)))

for args in [
    (292, 506, 1.18, -18, (119, 73, 43, 245)),
    (441, 580, 0.84, 24, (92, 52, 31, 240)),
    (1010, 402, 0.92, 16, (132, 82, 47, 242)),
    (1132, 612, 0.74, -28, (99, 58, 34, 238)),
    (690, 660, 0.62, 38, (121, 70, 38, 230)),
]:
    coffee_bean(*args)

soft = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(soft)
sd.rounded_rectangle((72, 82, W - 72, H - 78), radius=26, outline=(255, 255, 255, 120), width=3)
sd.rounded_rectangle((96, 106, W - 96, H - 102), radius=22, outline=(23, 32, 28, 42), width=2)
img = Image.alpha_composite(img, soft)

img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=105, threshold=3))
img.convert("RGB").save("public/assets/coffee-multimodal-hero.png", quality=94)
