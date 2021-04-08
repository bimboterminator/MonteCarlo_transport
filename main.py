import matplotlib.pyplot as plt
import vis
import numpy as np
with open('./X4sShowData.txt') as f:
    lines = f.readlines()
lines = lines[11:-2]
x_el = []
y_el = []
for line in lines:
    plot = line.split()
    map_object = map(float, plot)
    tup = tuple(map_object)
    x_el.append(tup[0])
    y_el.append(tup[1])


#fig, _ = plt.subplots()
#plt.loglog(x_el, y_el)
#plt.show()


with open('./al27tot.txt') as tot:
    lines_tot = tot.readlines()
lines_tot = lines_tot[11:-2]
x_tot = []
y_tot = []
for line in lines_tot:
    plot = line.split()
    map_object = map(float, plot)
    tup = tuple(map_object)
    x_tot.append(tup[0])
    y_tot.append(tup[1])

with open('./al27cap.txt') as cap:
    lines_cap = cap.readlines()
lines_cap = lines_cap[11:-2]
x_c = []
y_c = []
for line in lines_cap:
    plot = line.split()
    map_object = map(float, plot)
    tup = tuple(map_object)
    x_c.append(tup[0])
    y_c.append(tup[1])

with open('./al27nonel.txt') as inel:
    lines_inel = inel.readlines()
lines_inel = lines_inel[11:-2]
x_nonel = []
y_nonel = []
for line in lines_inel:
    plot = line.split()
    map_object = map(float, plot)
    tup = tuple(map_object)
    x_nonel.append(tup[0])
    y_nonel.append(tup[1])


N_D = (6.02214076 * (10 ** 23) * 2.7)/26.981538


def macro_tot(E):
    micro = np.interp(E, x_tot, y_tot)* 10**(-24)
    return micro*N_D
def macrto_el(E):
    micro = np.interp(E, x_el, y_el)* 10**(-24)
    return micro * N_D
def macro_cap(E):
    micro = np.interp(E, x_c, y_c)* 10**(-24)
    return micro * N_D
def macro_nonel(E):
    micro = np.interp(E, x_nonel, y_nonel)* 10**(-24)
    return micro * N_D


def transform(track):
    vertices = []
    for el in track:
        tup = (el[0], el[1], el[2])
        vertices.append(tup)
    return vertices


dimensions = (100,100,100)
y_pos = 5
thikness = 20
to_viz = []
abs = 0
leak  = 0
transmitted = 0
for i in range(100):
    e = np.random.uniform(0.00001,2)
    z = np.random.uniform(-5,5)
    x = np.random.uniform(-5,5)
    track = [[x, 0, z],[x, 5, z]]
    teta0  = np.array([0,1,0])
    r0 = np.array([x, 0, z])
    A = 26.981538
    alpha = (A-1)/(A+1)
    while True:
        e0=e
        eta = np.random.uniform()
        s = -1*np.log(eta)/macro_tot(e0)
        r = r0+s*teta0

        r1 = r[1] - 5
        r2 = r[1] - (5+thikness)

        if r1 < 0 :
            #track.append(r.tolist())
            leak+=1
            break
        if r2 >=0:
            track.append(r.tolist())
            transmitted+=1
            leak +=1
            break
        if r[2] > dimensions[2]/2 or r[2] < -dimensions[2]/2:
            leak+=1
            break
        if r[0] > dimensions[0]/2 or r[0] < -dimensions[0]/2:
            leak+=1
            break

        track.append(r.tolist())
        xsi = np.random.uniform()
        tot = macro_tot(e0)
        el = macrto_el(e0)
        capt = macro_cap(e0) + macro_nonel(e0)
        #print(capt)
        #print(el)
        if xsi < capt/tot:
            abs+=1
            break
        if xsi > capt/tot :
            mu = 2*np.random.uniform(0, 1) - 1
            e = 0.5*e0*((1-alpha**2)*mu +1 + alpha**2)
            cos = (1+A*mu)/np.sqrt(1+A**2 + 2*A*mu)
            sin = np.sqrt(1-cos**2)
            omega = 2*np.pi*np.random.uniform()
            x = sin/np.sqrt(1-teta0[2]**2)*(teta0[1]*np.sin(omega)-teta0[1]*teta0[0]*np.cos(omega)) + teta0[0]*cos
            y = sin/np.sqrt(1-teta0[2]**2)*(-1*teta0[0]*np.sin(omega)-teta0[1]*teta0[2]*np.cos(omega)) + teta0[1]*cos
            z = sin*np.sqrt(1-teta0[2]**2)*np.cos(omega) + teta0[2]*cos
            teta0 = np.array([x, y, z])
        #if teta0[2] > 1 :
         #   print(r,teta0)
        if e < 10**(-9):
            abs+=1
            break
        r0[0] = r[0]
        r0[1] = r[1]
        r0[2] = r[2]

    to_viz.append(transform(track))
    print(len(transform(track)))

vis.main(to_viz,thikness)
print("Abs", abs)
print("Leak", leak)
print("Left", transmitted)




