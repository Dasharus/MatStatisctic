import random
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np


type = input("\n\nВведіть тип випадкової змінної: \"discrete\"(дискретна) або \"continuous\"(неперервна).\nВи обрали: ")
method = input("\n\nВи хочете \"enter\"(ввести) чи \"generate\"(згенерувати автоматично) вибірку?\nВи обрали: ")
n = int(input("\n\nВведіть кількість експериментів: "))
r = 0
for i in range(100):
    if 2**i>=n:
        r = i-1
        break
print("\nВведіть початок а та кінець b проміжку [a, b): ")
a = float(input())
b = float(input())
step = (b-a)/r
    
discrete_values = []
discrete_frequency = []
interval_frequency = []
intervals = []
if method=="enter":
    
    if type=="discrete":
        print("\nВведіть результати експерименту(" + str(n) + " дійсних чисел): ")
        array = [float(input()) for i in range(n)]
        
    if type=="continuous":
        print("\nВведіть результати експерименту.")
        for i in range(r):
            interval_frequency.append(int(input("На проміжку [" + "{0:.2f}".format(a+i*step, 2) + ", " + "{0:.2f}".format(a+(i+1)*step) + "): ")))
            intervals.append((a+i*step, a+(i+1)*step))

if method=="generate":
    
    if type=="discrete":
        array = [random.randint(a, b) for i in range(n)]
        
    if type=="continuous":
        sum = 0
        for i in range(r):
            intervals.append((a+i*step, a+(i+1)*step))
            frequency = random.randint(0, n//r*2)
            if sum+frequency <= n:
                interval_frequency.append(frequency)
                sum += frequency
            else:
                interval_frequency.append(n-sum)
                sum = n
        if sum!=n:
            interval_frequency[0] += n-sum

if type=="discrete":
    array.sort()
    k = 0
    for i in range(r):
        intervals.append((a+i*step, a+(i+1)*step))
        interval_frequency.append(0)
    for i in range(n):
        for j in range(len(intervals)):
            if array[i]>=intervals[j][0] and array[i]<intervals[j][1]:
                interval_frequency[j] += 1
        if i!=0 and array[i]!=array[i-1]:
            discrete_values.append(array[i-1])
            discrete_frequency.append(k)
            k = 0
        k += 1
    discrete_values.append(array[n-1])
    discrete_frequency.append(k)
    
    
if type=="continuous":
    discrete_frequency = interval_frequency
    for i in range(r):
        z = (intervals[i][0] + intervals[i][1])/2
        discrete_values.append(z)
    array = []
    for i in range(len(discrete_values)):
        for j in range(discrete_frequency[i]):
            array.append(discrete_values[i])

point_table = dict()
for i in range(len(discrete_values)):
    point_table["{0:.1f}".format(float(discrete_values[i]))] = discrete_frequency[i]
pd.DataFrame(point_table, index=["n[i]"])
interval_table = dict()
for i in range(len(intervals)):
    interval_table["[" + "{0:.2f}".format(a+i*step, 2) + ", " + "{0:.2f}".format(a+(i+1)*step) + ")"] = interval_frequency[i]
pd.DataFrame(interval_table, index=["n[i]"])

plt.bar(discrete_values, discrete_frequency)
plt.grid()
plt.title("Діаграма частот")
plt.xlabel("Значення")
plt.ylabel("Частота")

plt.plot(discrete_values, discrete_frequency)
plt.title("Полігон частот")
plt.xlabel("Значення")
plt.ylabel("Частота")

if type=="continuous":
    plt.bar(discrete_values, discrete_frequency, width=step)
    plt.grid()
    plt.title("Гістограма")
    plt.xlabel("Значення")
    plt.ylabel("Частота")

x = []
y = []
x.append(a-step)
y.append(0.0)

if type=="discrete":
    y.append(0)
    for i in range(len(discrete_values)):
        value = discrete_values[i]
        x.append(value)
        y.append(y[len(y)-1]+discrete_frequency[i]/n)
    x.append(b+step)

    plt.step(x, y,'k-');

    for i in range(len(x)):
        x1=[]
        if i != len(x)-1:
            y1 = np.linspace(y[i], y[i+1])
        for j in range(len(y1)):
            x1.append(x[i])
        plt.plot(x1, y1, 'w--')

    plt.plot(x, y,'k>');

if type=="continuous":
    x.append(a)
    y.append(0)
    for i in range(len(intervals)):
        right = intervals[i][1]
        x.append(right)
        y.append(y[len(y)-1]+interval_frequency[i]/n)
    x.append(b+step)
    y.append(1.0)
    plt.plot(x, y)

plt.title("Функція розподілу")
plt.grid()


plt.show()

mean = 0
for el in array:
    mean += el
mean /= n

median = array[n//2] if n%2==0 else (array[n//2-1]+array[n//2])/2

cmp = 0
mode = 0
for i in range(len(discrete_values)):
    if discrete_frequency[i]>cmp:
        cmp = discrete_frequency[i]
        mode = discrete_values[i]

ro = max(array)-min(array)
        
dev=0
for i in range(len(discrete_values)):
    dev += discrete_frequency[i]*(discrete_values[i]-mean)**2
    
variance = dev/(n-1)
standart = math.sqrt(variance)
variation = standart/mean
dispersion = dev/n

def quartile():    
    if (n % 4) == 0:
        L = n // 4
        Q=[]
        for i in range(1,4):
            Q.append(array[i*L])
        return Q
    else:
        return "Обсяг вибірки не кратний 4 !"
    
def decile():
    if (n % 10) == 0:
        L = n // 10
        d=[]
        for i in range(1,10):
            d.append(array[i*L])
        return d
    else:
        return "Обсяг вибірки не кратний 10 !"
    
def moment(k, C):
    mom = 0
    for i in range(len(discrete_values)):
        mom+=((discrete_values[i]-C)**k)*discrete_frequency[i]
    mom/=n
    return mom

asymetry=moment(3, mean)/(moment(2, mean)**1.5)
excess=moment(4, mean)/(moment(2, mean)**2)-3

print("Числові характеристики:")
print("Середнє:", mean)
print("Медіана:", median)
print("Мода:", mode)
print("Девіація:", dev)
print("Розмах:", ro)
print("Варінса:", variance)
print("Стандарт:", standart)
print("Варіація:", variation)
print("Вибіркова дисперсія:", dispersion)
print("Квартилі:", quartile())
print("Децилі:", decile())
print("Асиметрія:", asymetry)
print("Ексцес:", excess)
print("DONE.")