from ultralytics import YOLO
import cv2

# Eğitimde kullandığın sınıf isimleri
CLASS_NAMES = ["Insan", "Tasit", "nuai", "nuap", "uai", "uap"]

class Detector:
    def __init__(self, model_path=r"D:\GöktenAI havacılıkta yapay zeka Teknofest\models\best (1).pt"):
        
        self.model = YOLO(model_path)

    def detect_frame(self, frame):
        """
        Tek bir görüntü karesi üzerinde YOLO tahmini yapar.
        Geriye yalnızca ilk sonuç nesnesini döner.
        """
        results = self.model.predict(source=frame, conf=0.4, device=0, verbose=False)

        return results[0]  # detection result object

    def extract_detections(self, result):
        """
        YOLO çıktısını sadeleştirilmiş dict listesine dönüştürür.
        Her bir detection için class_id, sınıf adı, skor ve bbox bilgisi döner.
        """
        detections = []
        for box in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = box
            class_id = int(class_id)
            label = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else "Bilinmeyen"

            # İniş alanı sınıfıysa kontrol için işaretle (uai/uap => sınıf; nuai/nuap => non-sınıf)
            if label == "uai" or label == "uap":
                landing_status = 1  # Başlangıçta uygun, sonra postprocessor kontrol edecek
            elif label == "nuai" or label == "nuap":
                landing_status = -1  # iniş alanı değil
            else:
                landing_status = -1  # insan, taşıt vs. için geçerli değil

            detections.append({
                "cls": str(class_id),
                "label": label,
                "landing_status": landing_status,
                "score": round(float(score), 4),
                "top_left_x": round(x1, 2),
                "top_left_y": round(y1, 2),
                "bottom_right_x": round(x2, 2),
                "bottom_right_y": round(y2, 2)
            })
        return detections
