import numpy as np
import scipy.io

global file

def open_file(name):
    global file
    file = open(name, 'r')
    title = file.readline()
    columns_names = file.readline()

def close_file():
    global file
    file.close()

def get_row():
    global file
    row_content = file.readline()
    
    array_string_values = row_content.split(', ')
    array_string = np.array(array_string_values)
    #Solo se convierte a float cuando el arreglo No esta vacío
    #De otro modo lanza error
    if len(array_string) > 1:
        array_float  = array_string.astype(np.float)
    else:
        #Se regresa una cadena vacia solo para que no de error
        array_float = []

    return array_float



##################################################################
#FOR MATLAB
global matlab_file_index
global matlab_file
global matlab_file_max_index


def open_matlab_file(name):
    global matlab_file
    global matlab_file_index
    global matlab_file_max_index

    matlab_file = scipy.io.loadmat(name)
    
    matlab_file_index = 0
    matlab_file_max_index = len(matlab_file['data'][0][0]['X'][0][0])




def get_next_row_from_matlab_file():
    global matlab_file_index

    if matlab_file_index < matlab_file_max_index:
        array_row = matlab_file['data'][0][0]['X'][0][0][matlab_file_index]
        array_taken_values = array_row[:25]
    else:
        array_taken_values = []

    matlab_file_index = matlab_file_index + 1

    return array_taken_values