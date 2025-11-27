"""Manejo de la base de datos para guardar puntuaciones"""
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


class DatabaseManager:
    """Clase para manejar todas las operaciones de base de datos"""
    
    def __init__(self):
        self.connection = None
        self.conectar()
    
    def conectar(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                print("✓ Conexión exitosa a la base de datos")
        except Error as e:
            print(f"✗ Error al conectar a la base de datos: {e}")
            self.connection = None
    
    def cerrar(self):
        """Cierra la conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("✓ Conexión cerrada")
    
    def obtener_o_crear_usuario(self, username):
        """Obtiene el ID de un usuario o lo crea si no existe"""
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            
            # Buscar usuario existente
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            resultado = cursor.fetchone()
            
            if resultado:
                user_id = resultado[0]
            else:
                # Crear nuevo usuario
                cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
                self.connection.commit()
                user_id = cursor.lastrowid
                print(f"✓ Nuevo usuario creado: {username}")
            
            cursor.close()
            return user_id
            
        except Error as e:
            print(f"✗ Error al obtener/crear usuario: {e}")
            return None
    
    def obtener_game_id(self, game_name):
        """Obtiene el ID de un juego por su nombre"""
        if not self.connection:
            return None
        
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM games WHERE game_name = %s", (game_name,))
            resultado = cursor.fetchone()
            cursor.close()
            
            if resultado:
                return resultado[0]
            else:
                print(f"✗ Juego '{game_name}' no encontrado en la base de datos")
                return None
                
        except Error as e:
            print(f"✗ Error al obtener game_id: {e}")
            return None
    
    def guardar_puntuacion(self, username, game_name, score):
        """Guarda una puntuación en la base de datos"""
        if not self.connection:
            print("✗ No hay conexión a la base de datos")
            return False
        
        try:
            user_id = self.obtener_o_crear_usuario(username)
            if not user_id:
                return False
            
            game_id = self.obtener_game_id(game_name)
            if not game_id:
                return False
            
            cursor = self.connection.cursor()
            query = "INSERT INTO scores (user_id, game_id, score) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, game_id, score))
            self.connection.commit()
            cursor.close()
            
            print(f"✓ Puntuación guardada: {username} - {score} puntos")
            return True
            
        except Error as e:
            print(f"✗ Error al guardar puntuación: {e}")
            return False
    
    def obtener_top_puntuaciones(self, game_name, limite=10):
        """Obtiene las mejores puntuaciones de un juego"""
        if not self.connection:
            return []
        
        try:
            game_id = self.obtener_game_id(game_name)
            if not game_id:
                return []
            
            cursor = self.connection.cursor()
            query = """
                SELECT u.username, s.score, s.created_at
                FROM scores s
                JOIN users u ON s.user_id = u.id
                WHERE s.game_id = %s
                ORDER BY s.score DESC
                LIMIT %s
            """
            cursor.execute(query, (game_id, limite))
            resultados = cursor.fetchall()
            cursor.close()
            
            return resultados
            
        except Error as e:
            print(f"✗ Error al obtener puntuaciones: {e}")
            return []
