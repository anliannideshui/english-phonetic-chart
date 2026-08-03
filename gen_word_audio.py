import asyncio
import edge_tts
import os
import re

async def generate_word_audio(word, voice, output_dir):
    filepath = os.path.join(output_dir, f"{word}.mp3")
    if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
        print(f"  SKIP {word} (exists)")
        return True
    try:
        communicate = edge_tts.Communicate(word, voice, rate="-10%")
        await communicate.save(filepath)
        size = os.path.getsize(filepath)
        if size > 100:
            print(f"  OK {word} ({size} bytes)")
            return True
        else:
            print(f"  FAIL {word} (too small)")
            return False
    except Exception as e:
        print(f"  FAIL {word} ({e})")
        return False

async def main():
    html_path = r"D:\AI\日常工作\phonics-app\www\index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    words = set()
    for m in re.finditer(r"w:'([^']+)'", html):
        w = m.group(1)
        if not w.startswith("+") and not w.startswith(" "):
            words.add(w)
    for m in re.finditer(r"w[12]:'([^']+)'", html):
        w = m.group(1)
        if not w.startswith("+") and not w.startswith(" "):
            words.add(w)
    for m in re.finditer(r'class="word">([^<]+)<', html):
        w = m.group(1).strip()
        if w and not w.startswith("+"):
            words.add(w)
    for m in re.finditer(r'data-w[12]="([^"]+)"', html):
        w = m.group(1)
        if not w.startswith("+"):
            words.add(w)

    words = sorted(words)
    print(f"Total words: {len(words)}")

    output_dir = r"D:\AI\日常工作\phonics-app\www\audio\words"
    os.makedirs(output_dir, exist_ok=True)

    voice = "en-GB-SoniaNeural"
    print(f"Using voice: {voice}")
    print()

    success = 0
    fail = 0
    for i, word in enumerate(words):
        print(f"[{i+1}/{len(words)}] {word}")
        ok = await generate_word_audio(word, voice, output_dir)
        if ok:
            success += 1
        else:
            fail += 1

    print(f"\n=== Done: {success}/{len(words)} success, {fail} failed ===")

asyncio.run(main())
