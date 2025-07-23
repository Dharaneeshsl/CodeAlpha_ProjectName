import os
import requests

MIDI_URLS = [
    # Free classical MIDI files (public domain)
    'https://bitmidi.com/uploads/45734.mid',  # Beethoven - Fur Elise
    'https://bitmidi.com/uploads/46515.mid',  # Mozart - Turkish March
    'https://bitmidi.com/uploads/46516.mid',  # Mozart - Rondo Alla Turca
]

os.makedirs('TASK 3/midi_data', exist_ok=True)

def download_midi(url, save_path):
    r = requests.get(url)
    if r.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(r.content)
        print(f"Downloaded: {save_path}")
    else:
        print(f"Failed to download: {url}")

for i, url in enumerate(MIDI_URLS):
    filename = f"TASK 3/midi_data/song_{i+1}.mid"
    download_midi(url, filename)

print("All MIDI files downloaded.") 