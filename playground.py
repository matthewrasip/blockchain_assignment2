import sys
# String to be converted to bytes
my_string = "Hello, World!"

# Using the bytes() function to convert the string to bytes
my_bytes = bytes(my_string, 'utf-8')

# Displaying the result
test = int.from_bytes(my_bytes, "big")
print(sys.maxsize)


583203976610444444512684011088316970267080434367743516442137439503897912990463008432931926

583203976610444444512684011088316970267080434367743516442137439503897912990463008432931926