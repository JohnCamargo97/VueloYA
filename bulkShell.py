from lib.models import Vuelo, puestos

nVuelos = len() Vuelo.objects.all() )
print(nVuelos)

BulkPuestos = []

for vuelo in range(nVuelos):
    for puestio in range(8):
        id = str(Vuelos[vuelo].id) + str(puestio).zfill(2) 
        BulkPuestos.append( puestos(id= id, Vuelo_id=Vuelos[vuelo], numero= puestio, Ejecutivo_bool=False, Ventana_bool = False) )