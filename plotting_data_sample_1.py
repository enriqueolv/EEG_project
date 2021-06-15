import signals_reader as SR
import queue as QUEUE

#Para graficar los datos
import matplotlib.pyplot as PLT
#Herramientas por si se ocupa a la hora de graficar datos
import numpy as NP


#Calcula el promedio de los valores del arreglo dado
def get_baseline(array):
    suma = NP.sum(array)
    average = NP.divide(suma, len(array)) 
    return average







if __name__ == "__main__":

    #Definimos el tamaño de la cola
    queue_size = 160
    #Canal de información 1 data original
    F1_data_queue = QUEUE.Queue(queue_size)
    #ES la cola con los valores de la linea de promedio
    base_line_queue = QUEUE.Queue(queue_size)
    #Canal de información 1 data procesada
    F1_processed_data_queue = QUEUE.Queue(queue_size)

    
    SR.open_matlab_file("S01T.mat")
    #Valores dados por el casco en el tiempo t
    current_values = SR.get_next_row_from_matlab_file()


    iterator = 0    
    while len(current_values) > 0:
        #Si la ventana esta llena hay que sacar el primer dato para dar lugar a otro nuevo
        #En otro caso simplemente siguen entrando los datos
        if F1_data_queue.its_full():
            #Se sacan los valores más viejo
            trash = F1_data_queue.pop()
            #Se sacan los valores de la cola de promedios
            trash = base_line_queue.pop()
            #Los datos procesados viejos se van
            trash = F1_processed_data_queue.pop()
        #FIN_IF


        F1_current_value = current_values[0]
        
        #Se introducen nuevos valores para cada canal
        F1_data_queue.push(F1_current_value)
        
        #Actualizamos la cola de promedios
        base_line_queue.push(get_baseline(F1_data_queue.get_as_array()))
        
        #El valor actual lo proceso y luego lo meto a la cola de datos procesados
        F1_current_value_processed = F1_current_value - get_baseline(F1_data_queue.get_as_array())
        

        #Ahora meto el valor procesado a la cola de datos procesados para el canal 1
        F1_processed_data_queue.push(F1_current_value_processed)
            

        #Obtenemos los datos de la cola como un array     
        F1_data_array = F1_data_queue.get_as_array()
        #obtenemos los datos de la cola de promeios como un arreglo
        base_line_array = base_line_queue.get_as_array()
        #Sacamos los datos de la cola de datos del canal 1 procesados y la metemos en un array
        F1_processed_data_array = F1_processed_data_queue.get_as_array()


        #GRAFICANDO EL ESTADO ALCUAL DE LAS COLAS
        #Rellenamos con ceros los datos si no miden el tamaño máximo
        while len(F1_data_array) < queue_size:
            F1_data_array.append(0)
            base_line_array.append(0)
            F1_processed_data_array.append(0)
        

        PLT.style.use('dark_background')
        #Regresa un conjunto de numeros para poner en X, 0, 1, 2, 3, 4 ....
        base = NP.linspace(iterator, len(F1_data_array)+iterator, len(F1_data_array))
        #Regresa la linea con puros ceros
        cero_line = NP.linspace(0, 0, len(F1_data_array))

        #Para graficar se pasa el arreglo de valores de X y el de valores de Y
        PLT.plot(base, cero_line, label='cero', color='white')
        PLT.plot(base, F1_data_array, label='F1 pure data', color='blue')
        #Agregamos la linea de promedio también
        PLT.plot(base, base_line_array, label='baseline', color='grey')
        #Agregamos los datos procesados para visualizarlos
        PLT.plot(base, F1_processed_data_array, label='F1 processed data', color='lightgreen')
        #se fija el eje de las Y's
        PLT.ylim(-50, 50)
        PLT.legend()
        PLT.show()

        iterator = iterator + 1

        #Siguiente fila de valores
        current_values = SR.get_next_row_from_matlab_file()
    #FIN_WHILE



    