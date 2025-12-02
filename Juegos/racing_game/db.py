"""Manejo de la base de datos para Racing Game"""
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG, GAME_NAME


class DatabaseManager:
    """Clase para manejar todas las operaciones de base de datos"""
    
    def __init__(self):
        self.connection = None
        self.game_name = GAME_NAME
        self.conectar()
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("✓ Conexión exitosa a la base de datos")
                return True
        except Error as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
            self.connection = None
            return False
    
    def cerrar(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Conexión cerrada")
    
    def _verificar_conexion(self):
        """Verifica y reestablece la conexión si es necesario"""
        try:
            if not self.connection or not self.connection.is_connected():
                print("⚠ Reconectando a la base de datos...")
                return self.conectar()
            return True
        except Error:
            return self.conectar()
    
    def obtener_o_crear_usuario(self, username):
        """Obtiene el ID de un usuario o lo crea si no existe"""
        if not self._verificar_conexion():
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            resultado = cursor.fetchone()
            
            if resultado:
                user_id = resultado[0]
            else:
                cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
                self.connection.commit()
                user_id = cursor.lastrowid
                print(f"✓ Nuevo usuario creado: {username}")
            
            cursor.close()
            return user_id
        except Error as e:
            print(f"✗ Error al obtener/crear usuario: {e}")
            if self.connection:
                self.connection.rollback()
            return None
    
    def obtener_game_id(self):
        """Obtiene el ID del juego Racing Game"""
        if not self._verificar_conexion():
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM games WHERE game_name = %s", (self.game_name,))
            resultado = cursor.fetchone()
            
            if not resultado:
                # Crear el juego si no existe
                cursor.execute("INSERT INTO games (game_name) VALUES (%s)", (self.game_name,))
                self.connection.commit()
                game_id = cursor.lastrowid
            else:
                game_id = resultado[0]
            
            cursor.close()
            return game_id
        except Error as e:
            print(f"✗ Error al obtener game_id: {e}")
            return None
    
    def guardar_puntuacion(self, username, score, track_id):
        """Guarda una puntuación en la base de datos"""
        username_track = f"{username}-{track_id}"
        
        if not self._verificar_conexion():
            print("✗ No hay conexión a la base de datos")
            return False
        
        try:
            user_id = self.obtener_o_crear_usuario(username_track)
            if not user_id:
                return False
            
            game_id = self.obtener_game_id()
            if not game_id:
                return False
            
            cursor = self.connection.cursor()
            query = "INSERT INTO scores (user_id, game_id, score) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, game_id, score))
            self.connection.commit()
            cursor.close()
            
            print(f"✓ Puntuación guardada: {username_track} - {score} segundos")
            return True
        except Error as e:
            print(f"✗ Error al guardar puntuación: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def obtener_top_puntuaciones(self, track_id, limite=10):
        """Obtiene las mejores puntuaciones de una pista"""
        if not self._verificar_conexion():
            return []
        
        try:
            game_id = self.obtener_game_id()
            if not game_id:
                return []
            
            cursor = self.connection.cursor()
            query = """
                SELECT u.username, s.score, s.created_at
                FROM scores s
                JOIN users u ON s.user_id = u.id
                WHERE s.game_id = %s AND u.username LIKE %s
                ORDER BY s.score ASC
                LIMIT %s
            """
            patron = f"%-{track_id}"
            cursor.execute(query, (game_id, patron, limite))
            resultados = cursor.fetchall()
            cursor.close()
            
            return resultados
        except Error as e:
            print(f"✗ Error al obtener puntuaciones: {e}")
            return []
    
    def verificar_nuevo_record(self, username, track_id, score):
        """Verifica si el score es un nuevo récord personal"""
        username_track = f"{username}-{track_id}"
        
        if not self._verificar_conexion():
            return False
        
        try:
            user_id = self.obtener_o_crear_usuario(username_track)
            if not user_id:
                return True
            
            game_id = self.obtener_game_id()
            if not game_id:
                return False
            
            cursor = self.connection.cursor()
            query = "SELECT MIN(score) FROM scores WHERE user_id = %s AND game_id = %s"
            cursor.execute(query, (user_id, game_id))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado[0] is None:
                return True
            
            return score < resultado[0]
        except Error as e:
            print(f"✗ Error al verificar récord: {e}")
            return False