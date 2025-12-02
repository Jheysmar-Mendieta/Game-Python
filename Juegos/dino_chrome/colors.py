"""Colores para cada valor de ficha en 2048"""

# Colores de las fichas (valor: (color_fondo, color_texto))
TILE_COLORS = {
    0: ((205, 193, 180), (119, 110, 101)),
    2: ((238, 228, 218), (119, 110, 101)),
    4: ((237, 224, 200), (119, 110, 101)),
    8: ((242, 177, 121), (249, 246, 242)),
    16: ((245, 149, 99), (249, 246, 242)),
    32: ((246, 124, 95), (249, 246, 242)),
    64: ((246, 94, 59), (249, 246, 242)),
    128: ((237, 207, 114), (249, 246, 242)),
    256: ((237, 204, 97), (249, 246, 242)),
    512: ((237, 200, 80), (249, 246, 242)),
    1024: ((237, 197, 63), (249, 246, 242)),
    2048: ((237, 194, 46), (249, 246, 242)),
    4096: ((60, 58, 50), (249, 246, 242)),
    8192: ((30, 29, 25), (249, 246, 242)),
}

def get_tile_color(value):
    """Obtiene el color de fondo de una ficha según su valor"""
    if value in TILE_COLORS:
        return TILE_COLORS[value][0]
    return TILE_COLORS[8192][0]  # Color por defecto para valores mayores

def get_text_color(value):
    """Obtiene el color del texto de una ficha según su valor"""
    if value in TILE_COLORS:
        return TILE_COLORS[value][1]
    return TILE_COLORS[8192][1]  # Color por defecto para valores mayores