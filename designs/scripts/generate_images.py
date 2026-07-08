import base64
import json
import os
import sys
import urllib.request
import urllib.error

from PIL import Image
import io

API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    sys.exit("OPENAI_API_KEY not set in environment")

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

IMAGES = [
    dict(
        name="d6-hero-orbital.jpg",
        prompt="Photorealistic wide-angle shot of a massive robotic solar energy array unfolding in lunar orbit above the moon's cratered surface, Earth visible small in the far background, dramatic cool blue rim lighting, deep black space with stars, cinematic sci-fi documentary photography style, ultra detailed, ultra wide composition",
        size="1536x1024",
        transparent=False,
    ),
    dict(
        name="d6-ops-lunarnight.jpg",
        prompt="Photorealistic wide shot of an autonomous lunar power station operating at night, glowing blue instrument lights and telemetry towers against a dark starfield, machinery silhouettes in the foreground, cinematic sci-fi documentary photography, ultra wide composition",
        size="1536x1024",
        transparent=False,
    ),
    dict(
        name="d6-stats-arrayfield.jpg",
        prompt="Photorealistic aerial wide shot of a large field of solar energy collector arrays spread across the lunar surface, Earth rising on the horizon, cool blue-toned lighting, cinematic sci-fi documentary photography, ultra detailed, ultra wide composition",
        size="1536x1024",
        transparent=False,
    ),
    dict(
        name="d6-ops-control.jpg",
        prompt="Photorealistic control room interior viewed from behind two engineers silhouetted against wide monitors showing lunar telemetry data with blue-toned displays, no visible faces, cinematic sci-fi documentary photography",
        size="1536x1024",
        transparent=False,
    ),
    dict(
        name="d6-product-array.png",
        prompt="Photorealistic product render of a compact autonomous lunar solar power array unit, sleek matte white and dark titanium panels with blue accent LED strips, three-quarter angle, clean isolated subject, high detail studio product photography",
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-product-relay.png",
        prompt="Photorealistic product render of a lunar surface power relay and energy transmission tower, metallic structure with a dish antenna and blue status lights, clean isolated subject, high detail studio product photography",
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-product-rover.png",
        prompt="Photorealistic product render of a compact autonomous lunar rover energy-collection unit with solar wings and blue navigation lights, three-quarter angle, clean isolated subject, high detail studio product photography",
        size="1024x1024",
        transparent=True,
    ),
]


def request_gpt_image(prompt, size, transparent):
    body = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": size,
        "quality": "high",
    }
    if transparent:
        body["background"] = "transparent"
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    return base64.b64decode(data["data"][0]["b64_json"])


def request_dalle3(prompt, size):
    dalle_size = "1792x1024" if size == "1536x1024" else "1024x1024"
    body = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": dalle_size,
        "quality": "hd",
        "n": 1,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    url = data["data"][0]["url"]
    with urllib.request.urlopen(url, timeout=60) as img_resp:
        return img_resp.read()


def strip_white_background(png_bytes, tolerance=18):
    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    pixels = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if r > 255 - tolerance and g > 255 - tolerance and b > 255 - tolerance:
                pixels[x, y] = (r, g, b, 0)
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    return buf.getvalue()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    use_gpt_image = True
    for item in IMAGES:
        out_path = os.path.join(OUT_DIR, item["name"])
        print(f"Generating {item['name']}...")
        img_bytes = None
        if use_gpt_image:
            try:
                img_bytes = request_gpt_image(item["prompt"], item["size"], item["transparent"])
            except urllib.error.HTTPError as e:
                err_body = e.read().decode(errors="replace")
                print(f"  gpt-image-1 failed ({e.code}): {err_body[:300]}")
                if e.code in (403, 404):
                    use_gpt_image = False
        if img_bytes is None:
            print("  falling back to dall-e-3")
            img_bytes = request_dalle3(item["prompt"], item["size"])
            if item["transparent"]:
                img_bytes = strip_white_background(img_bytes)

        if item["name"].endswith(".jpg"):
            im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            im.save(out_path, "JPEG", quality=92)
        else:
            with open(out_path, "wb") as f:
                f.write(img_bytes)
        print(f"  saved {out_path} ({len(img_bytes)} bytes)")


if __name__ == "__main__":
    main()
