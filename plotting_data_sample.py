import signals_reader as SR
import queue as QUEUE


#Para graficar los datos
import matplotlib.pyplot as PLT


#Herramientas por si se ocupa a la hora de graficar datos
import numpy as NP



#Para ir calculando el promedio
def get_baseline(array_signal):
    suma = NP.sum(array_signal)
    return NP.divide(suma, len(array_signal))







if __name__ == "__main__":

    #Definimos el tamaño de la cola
    queue_size = 128
    #Canal de información 1 data original
    channel_1_window = QUEUE.Queue(queue_size)
    #ES la cola con los valores de la linea de promedio
    base_line_queue = QUEUE.Queue(queue_size)
    #Canal de información 1 data procesada
    channel_1_processed = QUEUE.Queue(queue_size)

    
    SR.open_matlab_file("S01T.mat")
    current_values = SR.get_next_row_from_matlab_file()


    iterator = 0    
    while len(current_values) > 0:
        #Si la ventana esta llena hay que sacar primer dato para dar lugar a otro nuevo
        #En otro caso simplemente siguen entrando los datos
        if channel_1_window.its_full():
            #Se sacan los valores más viejo
            trash = channel_1_window.pop()
            #Se sacan los valores de la cola de promedios
            trash = base_line_queue.pop()
            #Los datos procesados viejos se van
            trash = channel_1_processed.pop()
        #FIN_IF

        channel_1_current_value = current_values[0]
        #Se introducen nuevos valores para cada canal
        channel_1_window.push(channel_1_current_value)
        #Actualizamos la cola de promedios
        base_line_queue.push(get_baseline(channel_1_window.get_as_array()))
        #El valor actual lo proceso y luego lo meto a la cola de datos procesados
        channel_1_current_value_processed = channel_1_current_value - get_baseline(channel_1_window.get_as_array())
        

        #Ahora meto el valor procesado a la cola de datos procesados para el canal 1
        channel_1_processed.push(channel_1_current_value_processed)
            

        #Obtenemos los datos de la cola como un array     
        prepared_data = channel_1_window.get_as_array()
        #obtenemos los datos de la cola de promeios como un arreglo
        base_line_array = base_line_queue.get_as_array()
        #Sacamos los datos de la cola de datos del canal 1 procesados y la metemos en un array
        channel_1_processed_array = channel_1_processed.get_as_array()


        #Mostrando el estado actual
        #Rellenamos con ceros los datos si no miden el tamaño máximo
        while len(prepared_data) < queue_size:
            prepared_data.append(0)
            base_line_array.append(0)
            channel_1_processed_array.append(0)
        

        PLT.style.use('dark_background')
        #Regresa un conjunto de numeros para poner en X, 0, 1, 2, 3, 4 ....
        base = NP.linspace(iterator, len(prepared_data)+iterator, len(prepared_data))
        #Regresa la linea con puros ceros
        cero_line = NP.linspace(0, 0, len(prepared_data))

        #Para graficar se pasa el arreglo de valores de X y el de valores de Y
        PLT.plot(base, cero_line, label='cero', color='white')
        PLT.plot(base, prepared_data, label='channel 1 pure data', color='blue')
        #Agregamos la linea de promedio también
        PLT.plot(base, base_line_array, label='baseline', color='grey')
        #Agregamos los datos procesados para visualizarlos
        PLT.plot(base, channel_1_processed_array, label='channel 1 processed data', color='lightgreen')
        #se fija el eje de las Y's
        PLT.ylim(-50, 50)
        PLT.legend()
        PLT.show()

        iterator = iterator + 1

        #Siguiente fila de valores
        current_values = SR.get_next_row_from_matlab_file()
    #FIN_WHILE



    