"""
array_length = 5
A = ("A","D","B","C","E")

for i in range(array_length):
    print(A[i])

for i in range(array_length):
    j = i
    while j > 0 and A[j-1] > A[j]:
        Temp = "0"
        Temp = A[j]
        A[j] = A[j-1]
        A[j-1] = Temp
        j = j-1

for i in range(array_length):
    print(A[i])
"""

A = [8,1,4,2]
x = 1

print("Iteration 0: ", end = " ")
for i in range(len(A)):
    print(A[i], end = " ")
print(" ")
for i in range(len(A)-1):
    for j in range(len(A)-1-i):
        print(f"Iteration {x}: ", end = " ")
        if A[j] > A[j+1]:
            Temp = 0
            Temp = A[j]
            A[j] = A[j+1]
            A[j+1] = Temp
        for i in range(len(A)):
            print(A[i], end = " ")
        x = x + 1
        print(" ")