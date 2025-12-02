"""Sistema de sonidos para el juego de carreras"""
import pygame
import numpy as np
import math


class SoundManager:
    """Maneja todos los sonidos del juego"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_playing = False
        self.volume = 0.5
        self.engine_sound = None
        self.engine_channel = None
        self._generate_sounds()
        
    def _generate_tone(self, frequency, duration, volume=0.3, wave_type='sine'):
        """Genera un tono sintético"""
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, n_samples)
        
        # Diferentes tipos de onda
        if wave_type == 'sine':
            wave = np.sin(2 * np.pi * frequency * t)
        elif wave_type == 'square':
            wave = np.sign(np.sin(2 * np.pi * frequency * t))
        elif wave_type == 'sawtooth':
            wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
        else:
            wave = np.sin(2 * np.pi * frequency * t)
            
        # Envelope
        attack = int(0.05 * n_samples)
        decay = int(0.1 * n_samples)
        release = int(0.15 * n_samples)
        
        envelope = np.ones(n_samples)
        if attack > 0:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release > 0:
            envelope[-release:] = np.linspace(1, 0, release)
            
        wave = wave * envelope * volume
        
        # Convertir a formato pygame
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
        
    def _generate_engine_sound(self, rpm_factor=1.0):
        """Genera sonido de motor continuo"""
        sample_rate = 22050
        duration = 1.0  # 1 segundo para loop
        n_samples = int(sample_rate * duration)
        
        t = np.linspace(0, duration, n_samples)
        
        # Frecuencias base del motor
        base_freq = 80 * rpm_factor
        
        # Mezcla de frecuencias para sonido de motor
        wave = (
            0.3 * np.sin(2 * np.pi * base_freq * t) +
            0.2 * np.sin(2 * np.pi * base_freq * 2 * t) +
            0.15 * np.sin(2 * np.pi * base_freq * 3 * t) +
            0.1 * np.sin(2 * np.pi * base_freq * 4 * t)
        )
        
        # Agregar ruido para textura
        noise = np.random.normal(0, 0.05, n_samples)
        wave = wave + noise
        
        # Normalizar
        wave = wave / np.max(np.abs(wave))
        wave = wave * 0.15  # Volumen bajo
        
        # Fade suave en los extremos para loop sin clicks
        fade_samples = int(0.05 * n_samples)
        wave[:fade_samples] *= np.linspace(0, 1, fade_samples)
        wave[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
        
    def _generate_sounds(self):
        """Genera todos los efectos de sonido"""
        try:
            # Motor
            self.sounds['engine_low'] = self._generate_engine_sound(0.8)
            self.sounds['engine_mid'] = self._generate_engine_sound(1.2)
            self.sounds['engine_high'] = self._generate_engine_sound(1.6)
            
            # Choque - sonido metálico
            crash_samples = []
            for freq in [200, 300, 150, 250]:
                tone = self._generate_tone(freq, 0.15, 0.3, 'square')
                samples = pygame.sndarray.samples(tone)
                crash_samples.append(np.array(samples, copy=True))
            combined = np.concatenate(crash_samples)
            self.sounds['crash'] = pygame.sndarray.make_sound(combined)
            
            # Derrape - ruido continuo
            self.sounds['drift'] = self._generate_tone(150, 0.3, 0.2, 'sawtooth')
            
            # Checkpoint - beep
            self.sounds['checkpoint'] = self._generate_tone(800, 0.1, 0.25)
            
            # Vuelta completada - secuencia
            lap_samples = []
            for freq in [600, 700, 800]:
                tone = self._generate_tone(freq, 0.15, 0.2)
                samples = pygame.sndarray.samples(tone)
                lap_samples.append(np.array(samples, copy=True))
            combined = np.concatenate(lap_samples)
            self.sounds['lap_complete'] = pygame.sndarray.make_sound(combined)
            
            # Victoria
            victory_samples = []
            melody = [523, 659, 784, 1047, 1175]  # Do, Mi, Sol, Do, Re
            for freq in melody:
                tone = self._generate_tone(freq, 0.2, 0.2)
                samples = pygame.sndarray.samples(tone)
                victory_samples.append(np.array(samples, copy=True))
            combined = np.concatenate(victory_samples)
            self.sounds['victory'] = pygame.sndarray.make_sound(combined)
            
            # Botón
            self.sounds['button'] = self._generate_tone(440, 0.05, 0.15)
            
            print("✓ Sonidos generados exitosamente")
        except Exception as e:
            print(f"⚠ Error al generar sonidos: {e}")
            
    def play(self, sound_name):
        """Reproduce un sonido"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].set_volume(self.volume)
                self.sounds[sound_name].play()
            except:
                pass
                
    def play_engine(self, speed_factor):
        """Reproduce sonido de motor según velocidad"""
        try:
            # Seleccionar sonido según velocidad
            if speed_factor < 0.3:
                sound = self.sounds['engine_low']
            elif speed_factor < 0.7:
                sound = self.sounds['engine_mid']
            else:
                sound = self.sounds['engine_high']
                
            if self.engine_channel is None or not self.engine_channel.get_busy():
                self.engine_channel = sound.play(loops=-1)
                
            # Ajustar volumen según velocidad
            volume = 0.1 + speed_factor * 0.15
            if self.engine_channel:
                self.engine_channel.set_volume(volume * self.volume)
        except:
            pass
            
    def stop_engine(self):
        """Detiene sonido de motor"""
        if self.engine_channel:
            self.engine_channel.stop()
            self.engine_channel = None
            
    def play_background_music(self):
        """Inicia música de fondo"""
        if not self.music_playing:
            try:
                # Crear música ambiental
                sample_rate = 22050
                duration = 8.0
                n_samples = int(sample_rate * duration)
                
                t = np.linspace(0, duration, n_samples)
                
                # Acordes simples
                chord1 = (
                    np.sin(2 * np.pi * 220 * t) * 0.15 +  # A
                    np.sin(2 * np.pi * 277 * t) * 0.12 +  # C#
                    np.sin(2 * np.pi * 330 * t) * 0.12    # E
                )
                
                # Modulación lenta
                modulation = np.sin(2 * np.pi * 0.5 * t) * 0.3 + 0.7
                wave = chord1 * modulation
                
                # Fade
                fade = int(0.5 * sample_rate)
                wave[:fade] *= np.linspace(0, 1, fade)
                wave[-fade:] *= np.linspace(1, 0, fade)
                
                wave = np.int16(wave * 32767)
                stereo_wave = np.column_stack((wave, wave))
                
                music = pygame.sndarray.make_sound(stereo_wave)
                music.set_volume(self.volume * 0.3)
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
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)