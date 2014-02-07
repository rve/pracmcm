def column(matrix, i):
    return [row[i] for row in matrix]
A = [[1,2,3,4], [5,6,7,8]]

print (column(A, 1))

B = {{1,2},{5,6}}
print (column(B,1))
