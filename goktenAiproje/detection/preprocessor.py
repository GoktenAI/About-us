import cv2
import numpy as np

class Preprocessor:
    def __init__(self, apply_blur_correction=True, enhance_contrast=True):
        """
        Görüntü ön işleme seçenekleri:
        - Bulanıklık giderme (sharpen)
        - Kontrast artırma (CLAHE)
        """
        self.apply_blur_correction = apply_blur_correction
        self.enhance_contrast = enhance_contrast

    def preprocess(self, frame):
        """
        Girdi görüntüsünü ön işler ve çıktıyı döner.
        """
        if self.apply_blur_correction:
            frame = self.sharpen(frame)
        if self.enhance_contrast:
            frame = self.apply_clahe(frame)
        return frame

    def sharpen(self, frame):
        """
        Basit bir sharpening filtresi (kenarları vurgular, bulanıklığı azaltır).
        """
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        return cv2.filter2D(src=frame, ddepth=-1, kernel=kernel)

    def apply_clahe(self, frame):
        """
        CLAHE (Contrast Limited Adaptive Histogram Equalization) uygulanır.
        Görüntünün aydınlık/kontrast dengesini iyileştirir.
        """
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        merged = cv2.merge((cl, a, b))
        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
