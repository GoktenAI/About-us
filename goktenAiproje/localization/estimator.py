import json
import cv2
import numpy as np
import random
import os

class Estimator:
    def __init__(self, use_random=False, position_data=None, frames_dir=None):
        # Kamera iç parametreleri (şu an kullanılmıyor ama saklanıyor)
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
        self.frames_dir = frames_dir  # Dışarıdan gelen frame klasörü yolu

    def estimate_from_video(self, video_path=None):
        if self.frames_dir:
            return self.estimate_from_frames()
        else:
            return self.estimate_from_data()

    def estimate_from_data(self):
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

    def estimate_from_frames(self):
        reference_positions = {
            item["frame"]: item["position"]
            for item in self.position_data if item["health"] == 1
        }
        estimated_positions = []

        prev_gray = None
        prev_position = None
        scale = 0.005  # her 1 piksel kayma = 0.005 metre
        sorted_items = sorted(self.position_data, key=lambda x: x["frame"])

        for item in sorted_items:
            frame_id = item["frame"]
            health = item["health"]

            frame_path = os.path.join(self.frames_dir, f"frame_{frame_id:06d}.jpg")
            if not os.path.exists(frame_path):
                print(f" Frame not found: {frame_path}")
                continue

            frame = cv2.imread(frame_path)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if health == 1:
                position = item["position"]
                prev_position = position
            else:
                if prev_gray is not None and prev_position is not None:
                    flow = cv2.calcOpticalFlowFarneback(
                        prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
                    )
                    dx = float(np.mean(flow[..., 0]) * scale)
                    dy = float(np.mean(flow[..., 1]) * scale)
                    dz = random.uniform(-0.01, 0.01)

                    position = {
                        "x": round(prev_position["x"] + dx, 4),
                        "y": round(prev_position["y"] + dy, 4),
                        "z": round(prev_position["z"] + dz, 4)
                    }
                    prev_position = position
                else:
                    position = {"x": 0.0, "y": 0.0, "z": 0.0}

            estimated_positions.append({
                "frame": frame_id,
                "position": position
            })

            prev_gray = gray

        return json.dumps(estimated_positions, indent=2)

    def estimate_from_pair(self, prev_frame, curr_frame, prev_position):
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )

        scale = 0.005
        dx = float(np.mean(flow[..., 0]) * scale)
        dy = float(np.mean(flow[..., 1]) * scale)
        dz = random.uniform(-0.01, 0.01)

        return {
            "x": round(prev_position["x"] + dx, 4),
            "y": round(prev_position["y"] + dy, 4),
            "z": round(prev_position["z"] + dz, 4)
        }

    def get_camera_intrinsics(self):
        return self.camera_intrinsics
