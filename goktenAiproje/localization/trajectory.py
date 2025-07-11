"""
import math

class TrajectoryAnalyzer:
    def __init__(self):
        self.positions = []

    def add_position(self, x, y, z):
        self.positions.append((x, y, z))

    def calculate_displacement(self):
        
        if len(self.positions) < 2:
            return 0.0

        x1, y1, z1 = self.positions[0]
        x2, y2, z2 = self.positions[-1]

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        return round(math.sqrt(dx**2 + dy**2 + dz**2), 2)

    def get_path_length(self):
        
        total = 0.0
        for i in range(1, len(self.positions)):
            x1, y1, z1 = self.positions[i-1]
            x2, y2, z2 = self.positions[i]

            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            total += dist

        return round(total, 2)
"""
import math

class TrajectoryAnalyzer:
    def __init__(self):
        self.positions = []  # (frame, x, y, z)

    def add_position(self, frame, x, y, z):
        self.positions.append((frame, x, y, z))

    def calculate_displacement(self):
        """
        İlk ve son pozisyon arasındaki düz mesafeyi hesaplar.
        """
        if len(self.positions) < 2:
            return 0.0

        _, x1, y1, z1 = self.positions[0]
        _, x2, y2, z2 = self.positions[-1]

        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1

        return round(math.sqrt(dx**2 + dy**2 + dz**2), 2)

    def get_path_length(self):
        """
        Ardışık tüm frameler arası toplam mesafeyi verir.
        """
        total = 0.0
        for i in range(1, len(self.positions)):
            _, x1, y1, z1 = self.positions[i-1]
            _, x2, y2, z2 = self.positions[i]

            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            dist = math.sqrt(dx**2 + dy**2 + dz**2)
            total += dist

        return round(total, 2)

    def calculate_average_velocity(self):
        """
        Ortalama hız (toplam yol / toplam süre). FPS sabit: 7.5
        """
        if len(self.positions) < 2:
            return 0.0

        frame_start = self.positions[0][0]
        frame_end = self.positions[-1][0]
        duration = (frame_end - frame_start) / 7.5

        if duration <= 0:
            return 0.0

        path_length = self.get_path_length()
        velocity = path_length / duration

        return round(velocity, 3)

    def is_approaching(self):
        """
        Z azalıyorsa yaklaşma olabilir (kamera nesneye yaklaşıyor)
        """
        if len(self.positions) < 2:
            return False

        _, _, _, z1 = self.positions[0]
        _, _, _, z2 = self.positions[-1]
        return z2 < z1
