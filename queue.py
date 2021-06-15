class Queue:
    max_size = 0
    queue = []

    def __init__(self, max_size):
        self.max_size = max_size
        self.queue = []

    def print_queue(self):
        print("[", end="")
        for i in range(len(self.queue)):
            if i < (len(self.queue) -1):
                print (str(self.queue[i]) + ", ", end="")
            else:
                print (str(self.queue[i]), end="")
        
        print("]")

    def get_as_array(self):
        return self.queue

    def max_size(self):
        return self.max_size


    def get_size(self):
        return len(self.queue)


    def push(self, new_value):
        current_size = len(self.queue)
        if current_size < self.max_size:
            self.queue.append(new_value)
    
    def pop(self):
        #Este método no es eficiente porque la eliminacion del primero de la lista
        #hace que todos los valores se recorran en memoria, resultadno en una complejidad O(n)
        #pero no importa porque esto es python y todo es ineficiente
        return self.queue.pop(0)
    
    def its_full(self):
        current_size = len(self.queue)
        if current_size < self.max_size:
            return False
        else:
            return True
    
    def clear(self):
        self.queue = []
    





#Pruebas
#print ("Hello")
#queue = Queue(3)
#queue.print_queue()
#queue.push(1)
#queue.print_queue()
#queue.push(2)
#queue.print_queue()
#queue.push(3)
#queue.print_queue()
#queue.push(4)
#queue.print_queue()
#trash = queue.pop()
#trash = queue.pop()
#queue.print_queue()    
