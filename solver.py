from pulp import *

def solver(data):
    # Crear el problema
    prob = LpProblem("MiProblema", LpMaximize)
    print(data['Meses'])

    # Crear las variables
    pF = [LpVariable("pF{}".format(i), lowBound=0, cat="Integer") for i in range(data['Meses'])]
    pE = [LpVariable("pE{}".format(i), lowBound=0, cat="Integer") for i in range(data['Meses'])]
    almacen = [LpVariable("almacen{}".format(i), lowBound=0, cat="Integer") for i in range(data['Meses'])]

    # Definir la función objetivo
    prob += lpSum(((data['ValorChip']) * data['Demanda'][i]) - (data['Costos'][i] * pF[i] + (data['Costos'][i] + 1) * pE[i] + data['CosteAlmacen'] * (almacen[i])) for i in range(data['Meses']))

    # Definir las restricciones

    ## Para la producion 
    prob += pF[0] <= ((sum(data['Demanda'])) // 5)
    for i in range(data['Meses']):
        prob += pE[i] >= pF[i]*(1/2)

## Almacen y restricciones para la produccion 
    for i in range(data['Meses']):
        if i == 0:
            # Satisfaccion de demanda diaria
            prob += pF[i] + pE[i]  >= data['Demanda'][i]
            # La cantidad que se almacena
            # prob += almacen[i] == pE[i] + pF[i] - data['Demanda'][i]
            # Restriccion almacen 
            # prob += almacen[i] <= data['Almacen']
        else:
            # Satisfaccion de demanda diaria
            prob += pF[i] + pE[i] + almacen[i - 1]  >= data['Demanda'][i]
            # La cantidad que se almacena
            # prob += almacen[i] == almacen[i - 1] + pE[i] + pF[i] - data["Demanda"][i]
            # Restriccion almacen
            # prob += almacen[i] <= data['Almacen']

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

    for i in range(data['Meses']):
        prob += data['TopeProduccion'] >= pF[i]
    
    for i in range(data['Meses']):
        prob += data['TopeProduccion'] >= 2 * pE[i]

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
        print('')
        print("Valor óptimo de pF = ", pF[i].value(), end=" ")
        print("Valor óptimo de pE = ", pE[i].value(), end=" ")
        print("Valor óptimo de almacen = ", almacen[i].value(), end=" ")

    resultado = prob.objective.value()
    print("Resultado de la función objetivo:", resultado)