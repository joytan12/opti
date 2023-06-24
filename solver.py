from pulp import *

def solver(data):
    # Crear el problema
    prob = LpProblem("MiProblema", LpMaximize)

    # Crear las variables
    pF = [LpVariable("pF{}".format(i), lowBound=0, cat="Integer") for i in range(data['Meses'])]
    pE = [LpVariable("pE{}".format(i), lowBound=0, cat="Integer") for i in range(data['Meses'])]
    binA = [LpVariable("binA{}".format(i), lowBound=0, cat="Binary") for i in range(data['Meses'])]
    binB = [LpVariable("binB{}".format(i), lowBound=0, cat="Binary") for i in range(data['Meses'])]

    almacen = [LpVariable("almacen{}".format(i), lowBound=0, cat="Integer") for i in range(data['Meses'])]

    # Definir la función objetivo
    prob += lpSum(((data['ValorChip']) * data['Demanda'][i]) - (data['Costos'][i] * pF[i] + (data['Costos'][i] + 1) * pE[i] + data['CosteAlmacen'] * (almacen[i])) for i in range(data['Meses']))

    # Definir las restricciones

    ## Almacen 
    for i in range(data['Meses']):
        if i == 0:
            # Satisfaccion de demanda diaria
            prob += pF[i] + pE[i]  >= data['Demanda'][i]
        else:
            # Satisfaccion de demanda diaria
            prob += pF[i] + pE[i] + almacen[i - 1]  >= data['Demanda'][i]

    for i in range(data['Meses']):
        if i == 0:
            # Restriccion almacen 
            prob += almacen[i] <= data['Almacen']
        else:
            # Restriccion almacen
            prob += almacen[i] <= data['Almacen']

    for i in range(data['Meses']):
        if i == 0:
            # La cantidad que se almacena
            prob += almacen[i] == pE[i] + pF[i] - data['Demanda'][i]
        else:
            # La cantidad que se almacena
            prob += almacen[i] == almacen[i - 1] + pE[i] + pF[i] - data["Demanda"][i]

    ## Restricciones de produccion
    prob += pF[0] <= ((sum(data['Demanda'])) // 5)
    for i in range(data['Meses']):
        prob += data['TopeProduccion'] >= pF[i]

    # Restricciones de procuccion extra

    for i in range(data['Meses']):
        prob += binA[i] + binB[i] == 1
    
    for i in range(data['Meses']):
        prob += pE[i] >= pF[i] * 0.5 - (1 - binB[i]) * 100000
        prob += pE[i] <= ((data['TopeProduccion'] // 2) + 1) + (1 - binB[i]) * 100000
    
    for i in range(data['Meses']):
        prob += pE[i] <= 0 + (1 - binA[i]) * 100000

    archivo = "instancia.txt"

    with open(archivo, 'w') as file:
        # Escribir la función objetivo
        file.write("max: " + str(prob.objective) + ";\n")
        
        # Escribir las restricciones
        for constraint in prob.constraints.values():
            file.write(str(constraint) + ";\n")


    # Imprimir la función objetivo
    print("Función objetivo:")
    print(prob.objective)
        
    # Imprimir todas las restricciones
    # print("Restricciones:")
    # for constraint in prob.constraints.values():
    #     print(constraint) 
    
    # Resolver el problema
    prob.solve()

    # Imprimir el estado de la solución
    # print("Estado:", LpStatus[prob.status])

    # Imprimir los valores óptimos de las variables
    for i in range(data['Meses']):
        print("Valor óptimo de pF = ", pF[i].value(), end=" ")
        print("Valor óptimo de pE = ", pE[i].value(), end=" ")
        print("Valor óptimo de almacen = ", almacen[i].value(), end="    ")
        print("bin1 = ", binA[i].value(), end=" ")
        print("bin2 = ", binB[i].value(), end="    ")
        print(i)

    resultado = prob.objective.value()
    print("Resultado de la función objetivo:", resultado)