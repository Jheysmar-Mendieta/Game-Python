"""Sistema de sonidos para Memory Game"""
import pygame
import numpy as np


class SoundManager:
    """Maneja todos los sonidos del juego"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_playing = False
        self._generate_sounds()
        
    def _generate_tone(self, frequency, duration, volume=0.3):
        """Genera un tono sintético"""
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        
        # Generar onda
        t = np.linspace(0, duration, n_samples)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Envelope ADSR simple
        attack = int(0.1 * n_samples)
        decay = int(0.1 * n_samples)
        release = int(0.2 * n_samples)
        
        envelope = np.ones(n_samples)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        
        # Convertir a formato pygame
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def _generate_sounds(self):
        """Genera todos los efectos de sonido"""
        try:
            # Flip de carta - tono corto ascendente
            self.sounds['flip'] = self._generate_tone(600, 0.1, 0.2)
            
            # Pareja encontrada - acorde alegre
            match_sound = self._generate_tone(800, 0.3, 0.25)
            self.sounds['match'] = match_sound
            
            # Victoria - secuencia de tonos
            victory_samples = []
            for freq in [523, 659, 784, 1047]:
                tone = self._generate_tone(freq, 0.2, 0.2)
                samples = pygame.sndarray.samples(tone)
                victory_samples.append(np.array(samples, copy=True))
            
            combined = np.concatenate(victory_samples)
            self.sounds['victory'] = pygame.sndarray.make_sound(combined)
            
            # Botón - click corto
            self.sounds['button'] = self._generate_tone(400, 0.05, 0.15)
            
            # Hover - tono suave
            self.sounds['hover'] = self._generate_tone(500, 0.05, 0.1)
            
            print("✓ Sonidos generados exitosamente")
        except Exception as e:
            print(f"⚠ Error al generar sonidos: {e}")
            
    def play(self, sound_name):
        """Reproduce un sonido"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def play_background_music(self):
        """Inicia música de fondo (tono ambiental)"""
        if not self.music_playing:
            try:
                # Crear música ambiental simple
                music = self._generate_tone(220, 2.0, 0.08)
                music.play(loops=-1)
                self.music_playing = True
            except:
                pass
    
    def stop_music(self):
        """Detiene la música"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def set_volume(self, volume):
        """Ajusta volumen global (0.0 a 1.0)"""
        for sound in self.sounds.values():
            sound.set_volume(volume)