from multiprocessing import Pool
def f(x):
    print(x)

if __name__ == '__main__':
    p = Pool(5)
    p.map(f, [1, 2, 3])