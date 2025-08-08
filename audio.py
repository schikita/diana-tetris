from pathlib import Path
import pygame

def resource_path(*parts) -> str:
    base = Path(__file__).resolve().parent
    return str(base.joinpath(*parts))

def init_audio():    
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
