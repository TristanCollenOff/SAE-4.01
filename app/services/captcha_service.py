import random

class CaptchaService:
    def __init__(self):
        pass
    
    def generate_captcha_style(self, word):
        """
        Génère un style CSS pour l'effet de buée sur vitre avec le mot caché
        """
        word_upper = word.upper()
        styles = {
            'word': word_upper,
            'rotation': random.uniform(-8, 8),
            'blur_amount': random.randint(2, 5),
            'opacity': random.uniform(0.3, 0.6),
            'font_size': random.randint(32, 40),
            'letter_spacing': random.randint(4, 10),
            'background': self._get_foggy_background()
        }
        return styles
    
    def _get_foggy_background(self):
        """Génère un fond effet buée sur vitre"""
        backgrounds = [
            'linear-gradient(135deg, rgba(200, 220, 255, 0.3) 0%, rgba(150, 180, 220, 0.4) 50%, rgba(180, 200, 240, 0.3) 100%)',
            'linear-gradient(135deg, rgba(180, 200, 230, 0.35) 0%, rgba(160, 190, 220, 0.45) 50%, rgba(170, 195, 225, 0.35) 100%)',
            'linear-gradient(135deg, rgba(190, 210, 240, 0.3) 0%, rgba(140, 170, 210, 0.4) 50%, rgba(165, 190, 220, 0.3) 100%)',
            'linear-gradient(135deg, rgba(175, 195, 225, 0.4) 0%, rgba(155, 185, 215, 0.5) 50%, rgba(160, 185, 215, 0.4) 100%)',
        ]
        return random.choice(backgrounds)
