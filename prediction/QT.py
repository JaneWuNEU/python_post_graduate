import pandas as pd
import math
from sklearn.linear_model import LinearRegression

Lambda = 46 # arrival rate
Mu = 12 # process rate per VMs
Alpha = 0.8 # priority of cost
Kappa = 2 # threshold of SLA violation
T = 60 # latency threshold defined in SLAs
K = 14 # number of the selected key correlated features
N = 5 # limit of number of VMs purchased
Ts = 2 # execution time


class QT:
    def __init__(self, lamb=0, mu=0, alp=0.0, kap=0, t=0, k=0, n=0, ts=0):
        self.lamb = lamb
        self.mu = mu
        self.alp = alp
        self.kap = kap
        self.t = t
        self.k = k
        self.n = n
        self.ts = ts
        self.V = []
        self.maxN = 0
        self.lr = None
        self.MAX = 5
        self.MIN = 2

    def fit(self, data):
        self.__cal_V(data)
        X = []
        Y = []
        for j in range(data.shape[1]-self.maxN):
            x = []
            for k in range(self.k):
                x.append(sum(data[j+self.maxN-self.V[k]]))
            X.append(x)
            Y.append(data[j+self.maxN])
        self.lr = LinearRegression()
        self.lr.fit(X, Y)

    def pred_next(self, Xt):
        Xt = [Xt]
        return self.lr.predict(Xt)

    def pred_m(self):
        minV = float('inf')
        m = 0
        i = self.MIN
        while i <= self.MAX :
            p0 = self.__cal_p0(i)
            if p0 == float("inf"):
                print("Not Convergence when m = ", i)
                i += 1
                continue
            L = self.__cal_Tq(i) + self.ts
            G = L / self.t
            F = self.__cost_func(i) # todo: Cost Function need change, up to you
            newV = self.alp * F + (1-self.alp) * G
            if newV < minV and self.__constrain(i) :
                m = i
                minV =newV
            i += 1
        return m

    def __cal_V(self, data):
        cols = data.shape[1]
        Ps = []
        for i in range(cols - 1):
            p = data[cols - 1].corr(data[cols - 2 - i])
            Ps.append(p)
        mean_Ps = {}
        for i in range(cols):
            mean_p = sum(Ps[:i + 1]) / (i + 1)
            mean_Ps[mean_p] = i + 1
        keys = list(mean_Ps.keys())
        keys = sorted(keys, reverse=True)
        V = []
        for i in range(self.k):
            V.append(mean_Ps[keys[i]])
        self.V = sorted(V)
        self.maxN = self.V[len(V)-1]

    def __cal_p0(self, m):
        p1 = 0
        for i in range(m):
            p1 += self.lamb**i / (math.factorial(i) * self.mu**i)
        p2 = 0
        i = m
        pu_0 = self.lamb**i / (m**(i-m) * math.factorial(m) * self.mu**i)
        pr_pu = pu_0
        i += 1
        while True:
            pu = self.lamb**i / (m**(i-m) * math.factorial(m) * self.mu**i)
            if pu >= pr_pu :
                return float("inf")
            pr_pu = pu
            p2 += pu
            if (pu_0 / pu) > 10**5:
                break
            i += 1
        return (p1 + p2)**(-1)

    def __cal_Tq(self, m):
        return self.__cal_p0(m) * (self.lamb / self.mu)**m / math.factorial(m) / m / self.mu / (1-(self.lamb / self.mu /m)**2)

    def __cost_func(self, m):
        return (m - self.MIN) / (self.MAX - self.MIN)

    def __cal_Pi(self, i, m):
        if (i>=1) and (i < m) :
            return (self.lamb ** i) * self.__cal_p0(m) / math.factorial(i) / (self.mu ** i)
        else :
            return (self.lamb ** i) * self.__cal_p0(m) / (m ** (i - m)) / math.factorial(m) / (self.mu ** i)

    def __constrain(self, m):
        sum =0.0
        for i in range(m * self.k):
            sum += self.__cal_Pi(i,m)
        if sum > 1 - 1.0 * self.kap / 100 :
            return True
        return False

# ----------------------------

def get_data_for_pred(data, V):
    cols = data.shape[1]
    X = []
    for i in range(len(V)):
        X.append(sum(data[cols-2-V[i]])) # todo: change 2 to 1
    return X

if __name__ == '__main__':

    print('START')

    # process data
    print("\nprocess data")
    data = pd.read_excel('D:\cloudsim\log/workload/QT.xlsx', sheetname=0)
    list_data = list(data['number_of_request(per minute)'])
    rows = int(len(list_data) / 60)
    dict_data = {}
    for i in range(rows):
        dict_data[i] = list_data[i*60:i*60+60]
    data = pd.DataFrame(dict_data)

    # create model
    print("\ncreate model")
    model = QT(lamb=Lambda, mu=Mu, alp=Alpha, kap=Kappa, t=T, k=K, n=N, ts=Ts)
    model.fit(data)

    # prediction
    print("\nprediction")
    data4pred = get_data_for_pred(data, model.V)
    print("data for prediction is ",data4pred)
    Xtnext = model.pred_next(data4pred)
    print("Xt is \n\t",list(data[data.shape[1]-2])) # the 23 hour data
    print("real Xt+1 is \n\t",list(data[data.shape[1]-1])) # the 24 hour data
    print("predicted Xt+1 is \n\t",Xtnext[0])
    print("sum of real Xt+1 is ",sum(data[data.shape[1]-1]))
    print("sum of predicted Xt+1 is ",sum(Xtnext[0]))

    # calculate m
    print("\ncalculate m (Cost function need change, maybe, up to you)")
    m = model.pred_m()
    print("m is ", m)


