import signals_reader    as SR
import queue             as QUEUE
import matplotlib.pyplot as PLT
import numpy             as NP
import scipy.signal      as SIGNAL


def get_baseline(array):
    suma = NP.sum(array)
    average = NP.divide(suma, len(array)) 
    return average


def plot_data(array_1):
        PLT.style.use('dark_background')
        #Regresa un conjunto de numeros para poner en X, 0, 1, 2, 3, 4 ....
        base = NP.linspace(0, len(array_1), len(array_1))
        #Regresa la linea con puros ceros
        cero_line = NP.linspace(0, 0, len(array_1))


        ##Se recorre el areglo para ver si hay un pico
        for i in range(len(array_1)):
            if array_1[i] > 10:
                print("pico encontrado")
                PLT.axvline(i, 0, 1, label='pico encontrado', color='red')

        #Para graficar se pasa el arreglo de valores de X y el de valores de Y
        PLT.plot(base, cero_line, label='cero', color='white')
        PLT.plot(base, array_1, label='F7 processed data', color='lightgreen')
        #PLT.plot(base, array_2, label='F8 processed data', color='red')
        
        #se fija el eje de las Y's
        PLT.ylim(-300, 300)
        PLT.legend()
        PLT.show()


if __name__ == "__main__":

    buffer_size       = 640
    w                 = 128 #window_size
    F7_buffer         = QUEUE.Queue(buffer_size)
    F8_buffer         = QUEUE.Queue(buffer_size)
    current_values    = []  #array of values representing electrodes voltages
    i                 = 0 
    F7_processed_data = []
    F8_processed_data = []


    SR.open_matlab_file("Files/S03E.mat")
    current_values = SR.get_next_row_from_matlab_file()

    while len(current_values) > 0:
        i = 0
        F7_buffer.clear()
        F8_buffer.clear()
        while (len(current_values) > 0) and (i < buffer_size):
            F7_buffer.push(current_values[1])
            F8_buffer.push(current_values[5])
            i = i + 1
            current_values = SR.get_next_row_from_matlab_file()
        #end_while

        if i < buffer_size:
            print("No hay suficientes datos para llenar el buffer")
            exit()
        

        ##PROCESSING THE DATA
        F7_array = F7_buffer.get_as_array()
        F8_array = F8_buffer.get_as_array()        
        F7_baseline = get_baseline(F7_array)
        F8_baseline = get_baseline(F8_array)

        #removing baseline
        for index in range(buffer_size):
            F7_array[index] = F7_array[index] - F7_baseline
            F8_array[index] = F8_array[index] - F8_baseline

        #applying butterworth filtter
        sos = SIGNAL.butter(10, 15, 'hp', fs=1000, output='sos')
        filtered_F7 = SIGNAL.sosfilt(sos, F7_array)
        filtered_F8 = SIGNAL.sosfilt(sos, F8_array)

        subtracted_filtered_signal = NP.subtract(filtered_F7, filtered_F8)
        
        ##PLOTTING DATA
        plot_data(subtracted_filtered_signal)
        #plot_data(F7_array, F8_array)

        current_values = SR.get_next_row_from_matlab_file()












        

        












