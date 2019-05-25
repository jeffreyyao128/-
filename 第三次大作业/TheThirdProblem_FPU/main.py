#encoding=utf-8
'''
The third problem, FPU model
'''

import numpy as np
import matplotlib.pyplot as plt

class phonon:
    alpha = 0
    __n = 0
    Q =[]
    Q_dot=[]
    q =[]
    p =[]
    dt = 0.05
    def __init__(self,Q0,Q00,a=0):
        self.alpha=a
        self.Q = Q0[:]
        self.Q_dot=Q00[:]
        self.__n = len(self.Q)
        self.__Trans_q()
        self.omega=2*np.sin(np.pi*0.5/(self.__n+1))
    def __Trans_q(self):
        '''
        利用Q和\ dot(Q)，计算p和q
        '''
        self.q = [np.sqrt(2.0/(self.__n+1))*sum([np.sin(np.pi*((i+1)*(j+1))/(self.__n+1))*self.Q[j] for j in range(self.__n)]) for i in range(self.__n)]
        self.p = [np.sqrt(2.0/(self.__n+1))*sum([np.sin(np.pi*((i+1)*(j+1))/(self.__n+1))*self.Q_dot[j] for j in range(self.__n)]) for i in range(self.__n)]
    def __Tans_Q(self):
        self.Q = [np.sqrt(2.0/(self.__n+1))*sum([np.sin(np.pi*((i+1)*(j+1))/(self.__n+1))*self.q[j]
                                           for j in range(self.__n)]) for i in range(self.__n)]
        self.Q_dot = [np.sqrt(2.0/(self.__n+1))*sum([np.sin(np.pi*((i+1)*(j+1))/(self.__n+1))*self.p[j]
                                           for j in range(self.__n)]) for i in range(self.__n)]
    def Evolve(self):
        '''
        演化函数，只演化一步
        利用RK-4
        '''
        tp=self.p
        tq=self.q
        n = self.__n
        kp1 = [-2*tq[0]+tq[1]+self.alpha*((-tq[0])**2-(tq[0]-tq[1])**2)]+[\
            tq[i-1]-2*tq[i]+tq[i+1]+self.alpha*((tq[i-1]-tq[i])**2-(tq[i]-tq[i+1])**2) for i in range(1, n-1)]\
                +[tq[n-2]-2*tq[n-1]+self.alpha*((tq[n-2]-tq[n-1])**2-(tq[n-1])**2)]
        kq1 = tp
        tp = [tp[i]+ self.dt*0.5*kp1[i] for i in range(n)]
        tq = [tq[i]+ self.dt*0.5*kq1[i] for i in range(n)]
        kp2 = [-2*tq[0]+tq[1]+self.alpha*((-tq[0])**2-(tq[0]-tq[1])**2)]+[tq[i-1]-2*tq[i]+tq[i+1]+self.alpha*((tq[i-1]-tq[i])**2-(tq[i]-tq[i+1])**2) for i in range(1, n-1)]\
            + [tq[n-2]-2*tq[n-1]+self.alpha *((tq[n-2]-tq[n-1])**2-(tq[n-1])**2)]
        kq2 = tp
        tp = [tp[i] + self.dt*0.5*kp2[i] for i in range(n)]
        tq = [tq[i] + self.dt*0.5*kq2[i] for i in range(n)]
        kp3 = [-2*tq[0]+tq[1]+self.alpha*((-tq[0])**2-(tq[0]-tq[1])**2)]+[tq[i-1]-2*tq[i]+tq[i+1]+self.alpha*((tq[i-1]-tq[i])**2-(tq[i]-tq[i+1])**2) for i in range(1, n-1)]\
            + [tq[n-2]-2*tq[n-1]+self.alpha * ((tq[n-2]-tq[n-1])**2-(tq[n-1])**2)]
        kq3 = tp
        tp = [tp[i] + self.dt*kp3[i] for i in range(n)]
        tq = [tq[i] + self.dt*kq3[i] for i in range(n)]
        kp4 = [-2*tq[0]+tq[1]+self.alpha*((-tq[0])**2-(tq[0]-tq[1])**2)]+[tq[i-1]-2*tq[i]+tq[i+1]+self.alpha*((tq[i-1]-tq[i])**2-(tq[i]-tq[i+1])**2) for i in range(1, n-1)]\
            + [tq[n-2]-2*tq[n-1]+self.alpha *((tq[n-2]-tq[n-1])**2-(tq[n-1])**2)]
        kq4 = tp
        # 更新q,p
        self.p = [self.p[i]+self.dt/6*(kp1[i]+2*kp2[i]+2*kp3[i]+kp4[i]) for i in range(n)]
        self.q = [self.q[i]+self.dt/6 *(kq1[i]+2*kq2[i]+2*kq3[i]+kq4[i]) for i in range(n)]
        # 更新Q，Q_dot
        self.__Tans_Q()

    def Energ(self,i):
        '''
        计算第i个模式的能量
        Energy 函数测试正确
        '''
        return (0.5*self.Q_dot[i]**2+0.5*(2*np.sin(np.pi*0.5/(self.__n+1)))**2*self.Q[i]**2)

    def plot(self,T,p):
        '''
        画出前p个模式的能量随时间的变化
        T: 周期数
        '''
        t_max = T *2*np.pi/self.omega
        intern = np.linspace(0,T,int(t_max/self.dt))
        E = []
        for _ in intern:
            E.append([self.Energ(i) for i in range(p)])
            self.Evolve()
        res = [np.array([each[i] for each in E]) for i in range(p)]
        for each in res:
            plt.plot(intern,each)
        plt.show()

    def check(self):
        print(self.Energ(0))
        self.__Tans_Q()
        print(self.Energ(0))


if __name__ == "__main__":
    p=phonon([4]+[0 for _ in range(31)],[0 for _ in range(32)],a=0.25)
    # p.check()
    # print(p.q)
    # E1 = p.Energ(1)
    # p.Evolve()
    # print(p.Energ(1))
    p.plot(5,2)
    # A = np.array([[np.sqrt(2.0/(32+1))*np.sin(np.pi*(i+1)*(j+1)/(32+1)) for i in range(32)] for j in range(32)])



