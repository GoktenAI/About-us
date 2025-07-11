class Postprocessor:
    def __init__(self):
        pass

    def check_landing_zone(self, detections):
        """
        Gerçek UAP (label='uap') ve UAI (label='uai') alanlarının üzerine
        Taşıt ('Tasit') veya İnsan ('Insan') bindiyse landing_status = 0 yapılır.
        Başlangıçta status = 1, çakışma yoksa 1 olarak kalır.
        nuap/nuai sınıfları zaten iniş alanı DEĞİL -> landing_status = -1 kalmalı.
        """
        # Gerçek iniş alanlarını bul
        landing_zones = []
        for det in detections:
            if det.get("label") in ["uap", "uai"]:
                landing_zones.append(det)

        # Diğer nesneleri al (taşıt ve insan)
        obstacles = [det for det in detections if det.get("label") in ["Tasit", "Insan"]]

        # Her iniş alanı için kontrol et
        for zone in landing_zones:
            zx1, zy1 = zone["top_left_x"], zone["top_left_y"]
            zx2, zy2 = zone["bottom_right_x"], zone["bottom_right_y"]

            for obj in obstacles:
                ox1, oy1 = obj["top_left_x"], obj["top_left_y"]
                ox2, oy2 = obj["bottom_right_x"], obj["bottom_right_y"]

                if self._iou([zx1, zy1, zx2, zy2], [ox1, oy1, ox2, oy2]) > 0.01:
                    zone["landing_status"] = 0  # uygunsuz
                    break  # biri bile çakışsa yeter

        return detections

    def _iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)
        if interArea == 0:
            return 0.0

        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou
