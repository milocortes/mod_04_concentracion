from agents import Tienda, Hogar
import geopandas as gpd 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

hogares_random_gpd = gpd.read_file("../output/hogares_random.geojson")
tiendas = gpd.read_file("../output/tiendas_campeche.geojson")

## Definimos los productos que venden las tiendas así como precios mínimos y máximos
productos = ["queso", "tortillas", "carne", "huevo"]
n_prod = len(productos)

## Definimos precio máximo y mínimo de los precios de los productos
precio_min = 10
precio_max = 50

## Definimos ingreso máximo y mínimo de los agentes Hogares
ingreso_min = 200
ingreso_max = 2000

## Inicializamos la lista de agentes
tiendas_agentes = []
hogares_agentes = []

## Tiempo total
total_time = 100

# Diccionario de precios promedio
precios_promedio = {p:{t:0 for t in range(total_time+1)} for p in productos}
precios_promedio_inicio = {"queso" : 12, "tortillas" : 6, "carne" : 25, "huevo": 16}

## Descuento 
descuento = 0.05

## Incremento de precio
inc_prec = 0.2

## Inicializamos los agentes
for id,point in enumerate(tiendas["geometry"]):

    productos_dic = {p:{i:0 for i in range(total_time+1)} for p in productos}
    for p in productos:
        productos_dic[p][0] = np.random.normal(precios_promedio_inicio[p],1)

    tiendas_agentes.append(
        Tienda(id, point, productos_dic,total_time)
    )
    

for id, point in enumerate(hogares_random_gpd["geometry"]):
    ingreso_rand = np.random.uniform(ingreso_min, ingreso_max)
    n_p_canasta = np.random.randint(1,n_prod)
    canasta_consumo = np.random.choice(productos, n_p_canasta, replace = False)
    hogares_agentes.append(
        Hogar(id, point, ingreso_rand, canasta_consumo)
    )

buffer_dist = 2000

## Obtenemos las tiendas cercanas a los hogares
for hogar in hogares_agentes:
    hogar.busca_tiendas(tiendas_agentes, buffer_dist)

for tiempo in range(total_time):
    print(tiempo)
    ## Los hogares compran los productos
    for producto in productos:
        for hogar in hogares_agentes:
            hogar.compra_producto(producto, tiempo)

    ## Actualiza precios
    # Precio promedio
    for producto in productos:
        suma_p = 0
        n_p = len(tiendas_agentes)

        for tienda in tiendas_agentes:
            suma_p += tienda.productos[producto][tiempo]
        
        precios_promedio[producto][tiempo] = suma_p/n_p 

    # Actualiza precios
    for producto in productos:
        for tienda in tiendas_agentes:
            tienda.actualiza_precios(producto, descuento, inc_prec, precios_promedio[producto], tiempo)

df_precios_promedio = pd.DataFrame(precios_promedio)