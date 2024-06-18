import math

d= 5000
cp = 25
ca = 6.4*0.25
p = 6.4


def PP():

    pass

#Sistema de Tamaño de lote fijo - EOQ
def EOQ(d, cp, ca):
    q = math.sqrt(2*d*(cp/ca))
    return math.ceil(q)
q = EOQ(d, cp, ca)
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

a = CGI(d, q, ca, cp)
print(f'GGI = {a}')

print(f'EOQ = {EOQ(d, cp, ca)}')
