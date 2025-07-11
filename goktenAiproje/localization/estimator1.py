"""
class Estimator:
    def __init__(self):
       
        pass

    def estimate_from_video(self, video_path):
        
        Örnek olarak videodan alınan pozisyonları rastgele üretir.
        İleride optical flow tabanlı hesaplamaya çevrilebilir.
        
        positions = []

        for frame_num in range(30):  
            x = round(random.uniform(0, 10), 2)
            y = round(random.uniform(0, 10), 2)
            z = round(random.uniform(0, 5), 2)

            positions.append({
                "frame": frame_num,
                "position": {"x": x, "y": y, "z": z}
            })

        return json.dumps(positions, indent=2)
"""
import json
import numpy as np
import random

class Estimator:
    def __init__(self, use_random=False, position_data=None):
        # Kamera iç parametreleri
        self.camera_intrinsics = {
            "focal_length": np.array([2792.2, 2795.2]),
            "principal_point": np.array([1988.0, 1562.2]),
            "radial_distortion": np.array([0.0798, -0.1867]),
            "tangential_distortion": np.array([0.0, 0.0]),
            "image_size": np.array([3000, 4000]),
            "intrinsic_matrix": np.array([
                [2792.2, 0.0, 1988.0],
                [0.0, 2795.2, 1562.2],
                [0.0, 0.0, 1.0]
            ])
        }

        self.use_random = use_random
        self.position_data = position_data if position_data is not None else []

    def estimate_all_positions(self):
        """
        Her frame için pozisyon kestirimi yapar.
        Health status == 1 ise verilen veriyi kullanır.
        Health status == 0 ise rastgele pozisyon üretir (veya daha sonra optical flow eklersin).
        """
        estimated_positions = []

        for item in self.position_data:
            frame = item.get("frame")
            health = item.get("health", 1)

            if health == 1:
                position = item["position"]
            else:
                position = {
                    "x": round(random.uniform(0, 10), 2),
                    "y": round(random.uniform(0, 10), 2),
                    "z": round(random.uniform(0, 5), 2)
                }

            estimated_positions.append({
                "frame": frame,
                "position": position
            })

        return json.dumps(estimated_positions, indent=2)

    def get_camera_intrinsics(self):
        """
        Kamera iç parametrelerine erişim fonksiyonu
        """
        return self.camera_intrinsics
