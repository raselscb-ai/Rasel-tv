import requests
import re

input_file = "source.m3u"
output_file = "active.m3u"

with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

active_lines = []
i = 0

def is_live(url):
    try:
        r = requests.get(url, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

while i < len(lines):
    line = lines[i]

    if line.startswith("#EXTINF"):
        if i + 1 < len(lines):
            url = lines[i + 1].strip()

            if url.startswith("http") and is_live(url):
                active_lines.append(line)
                active_lines.append(url)

        i += 2
    else:
        i += 1

with open(output_file, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.writelines(active_lines)

print("Done: active channels saved")