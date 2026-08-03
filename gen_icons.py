from PIL import Image
import os

src = r"D:\AI\日常工作\phonics-app\icon.png"
img = Image.open(src)
print(f"Source image: {img.size} ({img.mode})")

# Center crop to square
w, h = img.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
square = img.crop((left, top, left + side, top + side))

# Generate 1024x1024 for @capacitor/assets
icon_1024 = square.resize((1024, 1024), Image.LANCZOS)
icon_1024.save(os.path.join(os.path.dirname(src), "icon-1024.png"))
print("Saved icon-1024.png (1024x1024)")

# Also generate a round icon (for Android adaptive icon foreground)
# For now just save the square version

# Generate individual Android sizes for manual placement if needed
sizes = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

for folder, size in sizes.items():
    resized = square.resize((size, size), Image.LANCZOS)
    out_dir = os.path.join(os.path.dirname(src), "android-icons", folder)
    os.makedirs(out_dir, exist_ok=True)
    resized.save(os.path.join(out_dir, "ic_launcher.png"))
    print(f"Saved {folder}/ic_launcher.png ({size}x{size})")

# 512x512 for Play Store
play = square.resize((512, 512), Image.LANCZOS)
play.save(os.path.join(os.path.dirname(src), "icon-512.png"))
print("Saved icon-512.png (512x512)")

print("Done!")
