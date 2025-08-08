from dataclasses import dataclass

@dataclass
class Settings:
    music_volume: float = 0.5   # 0..1
    sfx_volume: float = 0.7     # 0..1
    brightness: float = 1.0     # 0.5..1.2 (мультипликатор отрисовки)

    def clamp(self):
        self.music_volume = max(0.0, min(1.0, self.music_volume))
        self.sfx_volume   = max(0.0, min(1.0, self.sfx_volume))
        self.brightness   = max(0.5, min(1.2, self.brightness))
