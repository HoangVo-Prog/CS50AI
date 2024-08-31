my_dict = {'a': 3, 'b': 5, 'c': 1, 'd': 5}

# Find the key with the maximum value
max_key = max(my_dict, key=my_dict.get)

print(max_key)  # Output: 'b'