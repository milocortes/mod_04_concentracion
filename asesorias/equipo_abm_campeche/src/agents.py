class Tienda:
    def __init__(self, id, point_geom, productos, total_time):
        self.id = id
        self.point_geom = point_geom
        self.productos = productos
        self.ventas_productos = {p:{i:0 for i in range(total_time)} for p in productos}

    def realiza_venta(self, producto, tiempo):
        self.ventas_productos[producto][tiempo] += 1

    def actualiza_precios(self, producto, descuento, inc_precio, precio_promedio, tiempo):
        if self.ventas_productos[producto][tiempo] == 0:
            self.productos[producto][tiempo+1] = self.productos[producto][tiempo] * (1 - descuento)
            if self.productos[producto][tiempo] < 0:
                self.productos[producto][tiempo+1] = precio_promedio
        else:
            self.productos[producto][tiempo + 1] = self.productos[producto][tiempo]* (1 + inc_precio)

class Hogar:
    def __init__(self, id, point_geom, ingreso, canasta_consumo):
        self.id = id
        self.point_geom = point_geom
        self.ingreso = ingreso
        self.canasta_consumo = canasta_consumo
        self.tiendas_cercanas = []
    
    def busca_tiendas(self, lista_tiendas, radio_busqueda):
        for tienda in lista_tiendas:
            if self.point_geom.buffer(radio_busqueda).contains(tienda.point_geom):
                self.tiendas_cercanas.append(tienda)

    def compra_producto(self,producto,tiempo):
        if producto in self.canasta_consumo:
            precio = 10000000
            index_tienda_barata = None

            for index, tienda in enumerate(self.tiendas_cercanas):
                if tienda.productos[producto][tiempo] < precio:
                    precio = tienda.productos[producto][tiempo]
                    index_tienda_barata = index
            
            if self.ingreso < precio:
                self.tiendas_cercanas[index_tienda_barata].realiza_venta(producto,tiempo)
                self.ingreso -= precio

        else:
            pass
