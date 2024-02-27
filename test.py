from multiprocessing import Pool

def f(x,i):
    print(i*x)
    

if __name__ == '__main__':
    with Pool(5) as p:
        a= p.starmap(f,[(1,1)])
        