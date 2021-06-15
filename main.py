import signals_reader as SR
import queue as QUEUE



if __name__ == "__main__":

    #Definimos el tamaño de la cola
    queue_size = 6;
    channel_1_window = QUEUE.Queue(queue_size)
    channel_2_window = QUEUE.Queue(queue_size)
    channel_3_window = QUEUE.Queue(queue_size)
    channel_4_window = QUEUE.Queue(queue_size)



    SR.open_matlab_file("S01T.mat")
    current_values = SR.get_next_row_from_matlab_file()

    

    #Mientras el arvhivo siga dando renglones con datos
    while len(current_values) > 0:
        #Si la ventana esta llena hay que sacar primer dato para dar lugar a otro nuevo
        #En otro caso simplemente siguen entrando los datos
        if channel_1_window.its_full():
            #Se sacan los valores más viejos
            trash = channel_1_window.pop()
            trash = channel_2_window.pop()
            trash = channel_3_window.pop()
            trash = channel_4_window.pop()

            #Se introducen nuevos valores para cada canal
            channel_1_window.push(current_values[0])
            channel_2_window.push(current_values[1])
            channel_3_window.push(current_values[2])
            channel_4_window.push(current_values[3])
        
        else:
              #Se introducen nuevos valores para cada canal
            channel_1_window.push(current_values[0])
            channel_2_window.push(current_values[1])
            channel_3_window.push(current_values[2])
            channel_4_window.push(current_values[3])


        #Mostrando el estado actual    
        channel_1_window.print_queue()
        channel_2_window.print_queue()
        channel_3_window.print_queue()
        channel_4_window.print_queue()
        print("")


        #Siguiente fila de valores
        current_values = SR.get_next_row_from_matlab_file()
    #FIN_WHILE




    