

name = "generated_file.txt"
file = open(name, 'r')
title = file.readline()
columns_names = file.readline()


row_content = file.readline()
array_string_values = row_content.split(' ')
array_string = np.array(array_string_values)
array_float  = array_string.astype(np.float)

print(row_content)
