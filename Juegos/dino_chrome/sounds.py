"""Sistema de sonidos para el juego Dino"""
import pygame
import numpy as np


class SoundManager:
    """Maneja todos los sonidos del juego"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self._generate_sounds()
    
    def _generate_tone(self, frequency, duration=0.1, volume=0.3):
        """Genera un tono simple"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        
        # Generar onda sinusoidal
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(frequency * 2 * np.pi * t)
        
        # Aplicar envolvente ADSR
        attack = int(0.01 * sample_rate)
        release = int(0.05 * sample_rate)
        
        envelope = np.ones(n_samples)
        if attack < n_samples:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release < n_samples:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        
        # Convertir a formato de audio
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def _generate_sounds(self):
        """Genera todos los sonidos del juego"""
        try:
            # Sonido de salto (tono ascendente corto)
            jump_sound = self._generate_sweep(300, 500, 0.1, 0.25)
            self.sounds['jump'] = jump_sound
            
            # Sonido de choque (ruido descendente)
            crash_sound = self._generate_crash()
            self.sounds['crash'] = crash_sound
            
            # Sonido de checkpoint (ding agradable)
            checkpoint_sound = self._generate_checkpoint()
            self.sounds['checkpoint'] = checkpoint_sound
            
        except Exception as e:
            print(f"⚠ Error generando sonidos: {e}")
            # Crear sonidos silenciosos si falla
            silent = pygame.mixer.Sound(buffer=np.zeros((100, 2), dtype=np.int16))
            for key in ['jump', 'crash', 'checkpoint']:
                self.sounds[key] = silent
    
    def _generate_sweep(self, freq_start, freq_end, duration, volume):
        """Genera un barrido de frecuencia"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        # Barrido lineal de frecuencia
        freq_sweep = np.linspace(freq_start, freq_end, n_samples)
        phase = np.cumsum(freq_sweep) * 2 * np.pi / sample_rate
        wave = np.sin(phase)
        
        # Envolvente
        envelope = np.ones(n_samples)
        attack = int(0.01 * sample_rate)
        release = int(0.03 * sample_rate)
        if attack < n_samples:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release < n_samples:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_crash(self):
        """Genera sonido de choque"""
        sample_rate = 22050
        duration = 0.3
        n_samples = int(duration * sample_rate)
        
        # Ruido blanco con filtro descendente
        noise = np.random.uniform(-1, 1, n_samples)
        
        # Filtro descendente
        frequencies = np.linspace(1000, 100, n_samples)
        for i in range(1, n_samples):
            # Filtro simple pasa-bajos
            noise[i] = noise[i] * 0.3 + noise[i-1] * 0.7
        
        # Envolvente descendente
        envelope = np.linspace(1, 0, n_samples)
        wave = noise * envelope * 0.25
        
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_checkpoint(self):
        """Genera sonido de checkpoint"""
        sample_rate = 22050
        duration = 0.25
        n_samples = int(duration * sample_rate)
        
        # Dos notas rápidas (E y A)
        t1 = np.linspace(0, duration/2, n_samples//2, False)
        note1 = np.sin(659 * 2 * np.pi * t1)  # E5
        
        t2 = np.linspace(0, duration/2, n_samples//2, False)
        note2 = np.sin(880 * 2 * np.pi * t2)  # A5
        
        wave = np.concatenate([note1, note2])
        
        # Envolvente
        envelope = np.ones(n_samples)
        attack = int(0.01 * sample_rate)
        release = int(0.05 * sample_rate)
        if attack < n_samples:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release < n_samples:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * 0.2
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def play(self, sound_name):
        """Reproduce un sonido"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"⚠ Error reproduciendo sonido {sound_name}: {e}")
    
    def stop_all(self):
        """Detiene todos los sonidos"""
        pygame.mixer.stop()