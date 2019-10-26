

class ArrayOps(object):

    def __init__(self):

        pass

    def split_array(self, array, size):
        return [array[offs:offs+size] for offs in range(0, len(array), size)]
