import constantes
from items import Item
from personaje import Personaje

#obstaculos = [0,2,7,39,46,54,55]
obstaculos = [110,130,153]
class Mundo():
    def __init__(self):
        self.map_tiles = []
        self.obstaculos_tiles = []


    def process_data(self,data,tile_list):
        self.level_length = len(data)
        for y , row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x*constantes.TILE_SIZE
                image_y = y*constantes.TILE_SIZE
                image_rect.center = (image_x,image_y)
                title_data = [image,image_rect,image_x,image_y]
                self.map_tiles.append((title_data))
                #agregar tiles a obstaculos
                if tile in obstaculos:
                    self.obstaculos_tiles.append(title_data)

    def update(self,posicion_pantalla):
        for tile in self.map_tiles:
            tile[2] += posicion_pantalla[0]
            tile[3] += posicion_pantalla[1]
            tile[1].center = (tile[2],tile[3])

    def draw(self,surface):
        for tile in self.map_tiles:
            surface.blit(tile[0],tile[1])