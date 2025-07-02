

def reverse_array(a):
    n = len(a)
    for i in range(n // 2):
        a[i], a[n-1-i] = a[n-1-i], a[i]
    return a


print(reverse_array([1,2,3,5,8]))