"""Sistema de sonidos para Arkanoid"""
import pygame
import numpy as np
from settings import *


class SoundManager:
    """Gestiona todos los sonidos del juego"""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.music_enabled = True
        self.sfx_enabled = True
        self._generate_sounds()
    
    def _generate_tone(self, frequency, duration=0.1, volume=0.3):
        """Genera un tono simple"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(frequency * 2 * np.pi * t)
        
        # Envolvente ADSR
        attack = int(0.01 * sample_rate)
        release = int(0.05 * sample_rate)
        
        envelope = np.ones(n_samples)
        if attack < n_samples:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release < n_samples:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_sounds(self):
        """Genera todos los sonidos del juego"""
        try:
            # Rebote en pala (tono medio)
            self.sounds['paddle'] = self._generate_tone(440, 0.08, 0.3)
            
            # Rebote en pared (tono bajo)
            self.sounds['wall'] = self._generate_tone(220, 0.06, 0.25)
            
            # Ladrillo roto (acorde)
            self.sounds['brick'] = self._generate_chord([523, 659], 0.12, 0.3)
            
            # Ladrillo resistente (dos tonos)
            self.sounds['resistant'] = self._generate_sweep(400, 600, 0.1, 0.3)
            
            # Power-up recogido (ascendente)
            self.sounds['powerup'] = self._generate_sweep(440, 880, 0.15, 0.3)
            
            # Vida perdida (descendente triste)
            self.sounds['life_lost'] = self._generate_sweep(440, 220, 0.3, 0.35)
            
            # Nivel completado (triunfal)
            self.sounds['level_complete'] = self._generate_victory()
            
            # Game over (descendente largo)
            self.sounds['game_over'] = self._generate_gameover()
            
        except Exception as e:
            print(f"⚠ Error generando sonidos: {e}")
            silent = pygame.mixer.Sound(buffer=np.zeros((100, 2), dtype=np.int16))
            for key in ['paddle', 'wall', 'brick', 'resistant', 'powerup', 
                       'life_lost', 'level_complete', 'game_over']:
                self.sounds[key] = silent
    
    def _generate_chord(self, frequencies, duration=0.15, volume=0.3):
        """Genera un acorde con múltiples frecuencias"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        wave = np.zeros(n_samples)
        for freq in frequencies:
            wave += np.sin(freq * 2 * np.pi * t) / len(frequencies)
        
        # Envolvente
        attack = int(0.02 * sample_rate)
        release = int(0.08 * sample_rate)
        envelope = np.ones(n_samples)
        if attack < n_samples:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release < n_samples:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_sweep(self, freq_start, freq_end, duration, volume):
        """Genera un barrido de frecuencia"""
        sample_rate = 22050
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        
        freq_sweep = np.linspace(freq_start, freq_end, n_samples)
        phase = np.cumsum(freq_sweep) * 2 * np.pi / sample_rate
        wave = np.sin(phase)
        
        # Envolvente
        envelope = np.ones(n_samples)
        attack = int(0.01 * sample_rate)
        release = int(0.05 * sample_rate)
        if attack < n_samples:
            envelope[:attack] = np.linspace(0, 1, attack)
        if release < n_samples:
            envelope[-release:] = np.linspace(1, 0, release)
        
        wave = wave * envelope * volume
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_victory(self):
        """Genera sonido de victoria"""
        sample_rate = 22050
        duration = 0.6
        n_samples = int(duration * sample_rate)
        
        notes = [523, 659, 784, 1047]  # C-E-G-C
        wave = np.zeros(n_samples)
        
        note_duration = duration / len(notes)
        samples_per_note = n_samples // len(notes)
        
        for i, freq in enumerate(notes):
            start = i * samples_per_note
            end = start + samples_per_note
            t = np.linspace(0, note_duration, samples_per_note, False)
            note_wave = np.sin(freq * 2 * np.pi * t)
            
            envelope = np.ones(samples_per_note)
            attack = samples_per_note // 4
            if attack < samples_per_note:
                envelope[:attack] = np.linspace(0, 1, attack)
                envelope[-attack:] = np.linspace(1, 0, attack)
            
            wave[start:end] = note_wave * envelope * 0.3
        
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def _generate_gameover(self):
        """Genera sonido de game over"""
        sample_rate = 22050
        duration = 0.5
        n_samples = int(duration * sample_rate)
        
        notes = [392, 349, 294, 262]  # G-F-D-C descendente
        wave = np.zeros(n_samples)
        
        note_duration = duration / len(notes)
        samples_per_note = n_samples // len(notes)
        
        for i, freq in enumerate(notes):
            start = i * samples_per_note
            end = start + samples_per_note
            t = np.linspace(0, note_duration, samples_per_note, False)
            note_wave = np.sin(freq * 2 * np.pi * t)
            
            envelope = np.ones(samples_per_note)
            attack = samples_per_note // 5
            if attack < samples_per_note:
                envelope[:attack] = np.linspace(0, 1, attack)
                envelope[-attack:] = np.linspace(1, 0.2, attack)
            
            wave[start:end] = note_wave * envelope * 0.25
        
        wave = np.int16(wave * 32767)
        stereo_wave = np.column_stack((wave, wave))
        
        return pygame.sndarray.make_sound(stereo_wave)
    
    def play(self, sound_name):
        """Reproduce un sonido"""
        if not self.sfx_enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].set_volume(SFX_VOLUME)
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"⚠ Error reproduciendo sonido {sound_name}: {e}")
    
    def toggle_sfx(self):
        """Activa/desactiva efectos de sonido"""
        self.sfx_enabled = not self.sfx_enabled
        return self.sfx_enabled
    
    def toggle_music(self):
        """Activa/desactiva música"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
        else:
            pygame.mixer.music.set_volume(0)
        return self.music_enabled
    
    def stop_all(self):
        """Detiene todos los sonidos"""
        pygame.mixer.stop()