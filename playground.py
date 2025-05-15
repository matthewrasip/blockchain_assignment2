# String to be converted to bytes
my_string = "Hello, World!"

# Using the bytes() function to convert the string to bytes
my_bytes = bytes(my_string, 'utf-8')

# Displaying the result
test = int.from_bytes(my_bytes, "big")
print("Bytes to int: ", test)
