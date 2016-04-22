__author__ = 'luoming'

X = [(3, 3), (4, 3), (1, 1)]
Y = [1, 1, -1]

def PLA(w, b):
    wt = list(w); bt = b
    while True:
        bFlag = True
        for i in range(len(X)):
            if Y[i] * (wt[0]*X[i][0] + wt[1] * X[i][1] + bt) <= 0:
                wt[0] = wt[0]+Y[i]*X[i][0]
                wt[1] = wt[1]+Y[i]*X[i][1]
                bt = bt + Y[i]
                bFlag = False
                print wt, bt
                break
        if bFlag:
            break

def Gram_Matrix(M):
    length = len(M)
    G = []
    for i in range(length):
        t = []
        for j in range(length):
            v = 0
            for k in range(len(M[0])):
                v += M[i][k] * M[j][k]
            t.append(v)
        G.append(t)
    return G


def PLA_Antithesis(M, G, a, b):
    A = [];
    for i in range(len(M)):
        A.append(a)
    bt = b
    while True:
        bFlag = True
        for i in range(len(M)):
            v = 0
            for j in range(len(A)):
                v += A[j] * Y[j] * G[j][i]
            v += b
            v = v * Y[i]
            if v <= 0:
                A[i] = A[i] + 1
                b = b + Y[i]
                bFlag = False
                for k in range(len(A)):
                    print A[k],
                print b
                break
        if bFlag:
            break
    return

if __name__ == '__main__':
#    PLA((0, 0), 0)
    G = Gram_Matrix(X)
    PLA_Antithesis(X, G, 0, 0)