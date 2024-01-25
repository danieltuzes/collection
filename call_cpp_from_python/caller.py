import call_cpp_from_python

v1 = [1.0, 2.0, 3.0]
v2 = [4.0, 5.0, 6.0]
result = call_cpp_from_python.combine_vectors(v1, v2)
print(result)
