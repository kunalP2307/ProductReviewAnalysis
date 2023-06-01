input_list = ['Hello', '\t', 'World', '\n']
output_list = [item for item in input_list if item != '\t' and item != '\n']

print(output_list)
