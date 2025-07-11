# localization/utils.py
import json
import pandas as pd
import os

def load_position_json(path):
    """
    Pozisyon verisini JSON dosyasından yükler.
    Her öğe: {"frame": int, "position": {"x": float, "y": float, "z": float}, "health": int}
    """
    with open(path) as f:
        return json.load(f)

def load_position_csv(path):
    """
    Pozisyon verisini CSV dosyasından yükler.
    Beklenen sütunlar: translation_x, translation_y, translation_z, frame_numbers
    """
    df = pd.read_csv(path)
    result = []
    for _, row in df.iterrows():
        frame_str = str(row['frame_numbers'])
        if "frame_" in frame_str:
            frame_idx = int(frame_str.replace("frame_", "").replace(".jpg", ""))
        else:
            frame_idx = int(frame_str)

        result.append({
            "frame": frame_idx,
            "position": {
                "x": float(row['translation_x']),
                "y": float(row['translation_y']),
                "z": float(row['translation_z'])
            },
            "health": 1  # CSV'de sağlık bilgisi yoksa varsayılan olarak 1 veriyoruz
        })
    return result
