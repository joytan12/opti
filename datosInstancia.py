import random

def generarMatriz(M, tope = 0, costoInicial = 30, demandaInicial = 40, i = 0):
    lista = []
    while i < len(M) - tope:
        meses = random.randint(M[i][0], M[i][1])
        j = 0
        lista.append({'Meses': meses, 'Costos' : [costoInicial], 'Demanda' : [demandaInicial]})
        while j < meses - 1:
            lista[i]['Costos'].append(lista[i]['Costos'][j] + random.randint(1, 10))
            lista[i]['Demanda'].append(lista[i]['Demanda'][j] + random.randint(1, 3))
            j += 1
        i += 1
    return lista

def simulacion():
    M = [[5, 10], 
        [10, 20],
        [20, 30],
        [30, 40],
        [40, 50],
        [100, 130],
        [130, 160],
        [160, 180],
        [170, 190],
        [190, 200],
        [400, 600],
        [500, 700],
        [600, 800],
        [700, 900],
        [800, 1000],
        ]

    b = random.randint(2, 4)
    simulaciones = generarMatriz(M)
    for x in simulaciones:
        promedioD = (sum(x['Demanda']) // x['Meses'])
        promedioC = (sum(x['Costos']) // x['Meses'])
        x['ValorChip'] = (promedioC + b) * 2
        x['CosteAlmacen'] = b
        x['Almacen'] = promedioC * 5 // 9
        x['TopeProduccion'] = (promedioC) * 11 // 14
    
    return simulaciones