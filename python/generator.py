

def chain_generator():
    gen1 = (i for i in range(10))
    gen2 = (i * 2 for i in gen1 if i % 2)
    print(list(gen2))  
