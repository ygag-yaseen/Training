N = int(input())

storage = map(int, input().split())
storage = sorted(storage)
print ()
for i in range(len(storage)):
    if(i != len(storage)-1):
        if(storage[i]!=storage[i-1] and storage[i]!=storage[i+1]):
            print(storage[i])
            break
    else:
        print(storage[i])

#1 2 3 6 5 4 4 2 5 3 6 1 6 5 3 2 4 1 2 5 1 8 4 3 6 4 3 1 5 6 2
