import random


def get_random_float(lower, upper):
    secure_random = random.SystemRandom()
    randomfloat = secure_random.uniform(lower, upper)
    return randomfloat


def generate_row():
    array_float = []
    for i in range(8):
        array_float.append(get_random_float(0,10))
        #array_float.append(1.1)
    return array_float

def generate_row_as_string():
    array_float = generate_row()
    array_len = len(array_float)

    string_row = ""
    for i in range(array_len):
        if i < (array_len-1):
            string_row = string_row + str(array_float[i]) + ", "
        else:
            string_row = string_row + str(array_float[i])
    
    string_row = string_row + "\r\n"
    
    return string_row


if __name__ == "__main__":
    #w = write- will create a file if the specified file does not exist
    file = open("generated_file.txt", 'w')

    file.write("Entrada de datos de BCI\r\n")
    file.write("E1  E2  E3  E4  E5  E6  E7  E8\r\n")
    
    lines = 500000
    
    for i in range(lines):
        string_row = generate_row_as_string()
        file.write(string_row)
    
    file.close()

