import math

d= 5000
cp = 25
ca = 6.4*0.25
p = 6.4
diasDeTrabajoPorAnio = 300
dd = 10000/diasDeTrabajoPorAnio  #Demanda diaria    d = 10000 ejemplo
l = 5   #Tiempo de demora del proveedor
k = 2000    #Tasa de produccion
z = 1.64



## SS lote fijo
def SSLF (l, z):
    ss = z*math.sqrt(l)
    return ss


## SS intervalo fijo
def SSIF (dd,cp,ca,k,l,z):
    t =  math.sqrt((2/dd)*(cp/ca)*(1/(1-(dd/k))))
    ss = z*math.sqrt(t+l)
    return ss

#Punto de Pedido
def PP(dd,l):
    pp = dd * l
    return pp

pp = math.ceil(PP(dd,l))

#Sistema de Tamaño de lote fijo - EOQ - Lote optimo
def EOQ(d, cp, ca):
    q = math.sqrt(2*d*(cp/ca))
    return math.ceil(q)

q = EOQ(d, cp, ca)


#Sistema de Tamaño Fijo de Lote - MPR
def MPR(d=1000,cp=10,ca=0.5,k = k):
    q = math.sqrt(2*d*(cp/ca)*(1/(1-(d/k))))
    return math.ceil(q)

q2 = MPR(d=1000,cp=10,ca=0.5,k = k)
print(f'MPR = {q2}')

#Costo de Gestion de Inventario
def CGI(d,q,ca,cp):
    #costo de compra
    cc = p*d
    #Costo de Almacenamiento
    ca = ca * (q/2)
    #Costo de Pedido
    cp = cp*(d/q)
    # CGI
    cgi = cc + ca + cp
    return cgi

q2 = CGI(d, q, ca, cp)
q1= EOQ(d, cp, ca)
ss1 = SSLF(l, z)
ss2 = SSIF(dd,cp,ca,k,l,z)


print(f'GGI = {q2}')
print(f'EOQ = {q1}')
print(f'Punto de Pedido: {pp}')
print(f'SSLF = {ss1}')
print(f'SSIF = {ss2}')