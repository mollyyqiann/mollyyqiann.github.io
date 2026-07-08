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
        name="d6-whoweare-bg.jpg",
        prompt="Photorealistic wide shot of a connected network of lunar surface habitat modules and power infrastructure linked by cabling and relay towers, dusk lighting with cool blue accent glow, dark lunar sky with stars, cinematic sci-fi documentary photography, ultra wide composition",
        size="1536x1024",
        transparent=False,
    ),
    dict(
        name="d6-outputs-bg.jpg",
        prompt="Photorealistic close-up detail shot of a regenerative fuel cell and electrolyzer stack hardware unit, glowing blue instrumentation and piping, dark industrial technical background, shallow depth of field, cinematic sci-fi documentary photography",
        size="1536x1024",
        transparent=False,
    ),
    dict(
        name="d6-float-tank.png",
        prompt="Photorealistic product render of a small cylindrical hydrogen storage canister/tank unit, matte white and dark titanium with blue accent markings, three-quarter angle, clean isolated subject, high detail studio product photography",
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-float-panel.png",
        prompt="Photorealistic product render of a single folded solar panel fragment/module with blue accent LED strip along the edge, three-quarter angle, clean isolated subject, high detail studio product photography",
        size="1024x1024",
        transparent=True,
    ),
    dict(
        name="d6-float-module.png",
        prompt="Photorealistic product render of a small compact water reclamation module unit, sleek matte white and dark titanium casing with blue status light, three-quarter angle, clean isolated subject, high detail studio product photography",
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
