
from detection.detector import Detector
from localization.estimator import Estimator
from pipeline.vision_pipeline import VisionPipeline
from localization.utils import load_position_json
from ultralytics import YOLO
import os
import json

#  Yol ayarları
model_path = r"models\best (1).pt"
frame_dir = r"frame"
position_path = r"D:\GöktenAI havacılıkta yapay zeka Teknofest\jsonlar\deneme.json"
output_dir = "output/sonuc1"

def main():
    os.makedirs(output_dir, exist_ok=True)

    print("Model yükleniyor...")
    detector = Detector(model_path=model_path)

    print(" Pozisyon verisi yükleniyor...")
    position_data = load_position_json(position_path)

    # Sadece health=1 olanlar: ilk pozisyon referansları
    initial_positions = {
        item["frame"]: item["position"]
        for item in position_data if item["health"] == 1
    }

    estimator = Estimator(
        use_random=False,
        position_data=position_data,
        frames_dir=frame_dir
    )

    pipeline = VisionPipeline(detector=detector, estimator=estimator)

    print(" Frame klasörü kontrol ediliyor...")
    total_frames = len([f for f in os.listdir(frame_dir) if f.endswith(".jpg")])
    print(f" Bulunan frame sayısı: {total_frames}")

    if total_frames == 0:
        print("HATA: .jpg uzantılı frame bulunamadı.")
        return

    print(" Frame'ler işleniyor...")
    final_json = pipeline.process_frames(frame_dir, initial_positions)

    output_file = os.path.join(output_dir, "result1.json")
    if final_json.strip():
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(final_json)
        print(f" JSON dosyası kaydedildi → {output_file}")
        print(f" Toplam frame işlendi: {len(json.loads(final_json))}")
        print(f" JSON boyutu: {len(final_json) / 1024:.2f} KB")
    else:
        print(" Uyarı: Çıktı boş. Tahmin üretilememiş olabilir.")

    # (Opsiyonel test için) Model cihazı kontrol
    model = YOLO(model_path)
    print("Model cihazı:", next(model.model.parameters()).device)

if __name__ == "__main__":
    main()
