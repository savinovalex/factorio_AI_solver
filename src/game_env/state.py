import numpy as np

class State:
    def __init__(self, data):
        if isinstance(data, tuple):
            rows, cols = data
            self.map = np.zeros((rows, cols), dtype=np.uint8)
        else:
            self.map = data.copy()

    def apply_path_legs(self, path_legs):
        for leg in path_legs:
            self.map[leg[0], leg[1]] = leg[2]

    def __repr__(self):
        # Define the mapping
        mapping = {0: '.', 1: '>', 2: '|', 3: '<', 4: '^', 5: '#'}

        # Create a vectorized function to apply the mapping
        vec_map = np.vectorize(lambda x: mapping.get(x, '.'))

        # Apply the mapping to your array 'a'
        mapped_array = vec_map(self.map)

        # Print the result in a readable format
        return '\n'.join(''.join(row) for row in mapped_array)
