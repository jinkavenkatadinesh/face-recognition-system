"""
Dataset Expander - Downloads sample face images for testing
Uses free, publicly available sample images from the web.
"""

import os
import urllib.request
import ssl

# Disable SSL verification for downloading
ssl._create_default_https_context = ssl._create_unverified_context

# Output folder
raw_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dataset", "raw")
os.makedirs(raw_folder, exist_ok=True)

# Free sample face images (public domain / freely available)
image_urls = {
    # Single person - frontal
    "img4_single_woman.jpg": "https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=600",
    # Single person - man
    "img5_single_man.jpg": "https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=600",
    # Group of people
    "img6_group.jpg": "https://images.pexels.com/photos/1595385/pexels-photo-1595385.jpeg?auto=compress&cs=tinysrgb&w=600",
    # Family/group outdoor
    "img7_outdoor_group.jpg": "https://images.pexels.com/photos/1516036/pexels-photo-1516036.jpeg?auto=compress&cs=tinysrgb&w=600",
    # Side profile
    "img8_side_profile.jpg": "https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=600",
    # Low light portrait
    "img9_low_light.jpg": "https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=600",
    # Multiple people close up
    "img10_couple.jpg": "https://images.pexels.com/photos/1024311/pexels-photo-1024311.jpeg?auto=compress&cs=tinysrgb&w=600",
}

print("[*] Downloading sample face images...\n")

downloaded = 0
failed = 0

for filename, url in image_urls.items():
    filepath = os.path.join(raw_folder, filename)

    if os.path.exists(filepath):
        print(f"  [~] {filename} already exists, skipping.")
        continue

    try:
        print(f"  [-] Downloading {filename}...", end=" ")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read()
            with open(filepath, "wb") as f:
                f.write(data)
        size_kb = len(data) / 1024
        print(f"SUCCESS ({size_kb:.1f} KB)")
        downloaded += 1
    except Exception as e:
        print(f"FAILED: {e}")
        failed += 1

print(f"\n{'='*40}")
print(f"  [+] Downloaded: {downloaded} images")
print(f"  [-] Failed: {failed} images")
print(f"  [+] Total in dataset/raw/: {len(os.listdir(raw_folder))} images")
print(f"{'='*40}")
