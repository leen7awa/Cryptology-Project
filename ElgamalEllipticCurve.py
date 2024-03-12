# print("ElGamal based Elliptic Curve Cryptography\nby Dhruv Dixit:\t 15BCE1324\nVIT University, Chennai\n\nElliptic Curve General Form:\t y^2 mod n=(x^3  + a*x + b)mod n\nEnter 'n':")

import random as r


# EC equation
def polynomial(LHS,RHS,n):
    for i in range(0,n):
        LHS[0].append(i)
        RHS[0].append(i)
        LHS[1].append((i*i*i + a*i + b)%n) # y^2 = x^3 + ax + b
        RHS[1].append((i*i)%n)


def points_generate(arr_x,arr_y,n):
    count=0
    for i in range(0,n):
        for j in range(0,n):
            if(LHS[1][i]==RHS[1][j]):
                count+=1
                arr_x.append(LHS[0][i])
                arr_y.append(RHS[0][j])
    return count

def encrypt(msg):
    #Cipher text 1 generation ---> Y1 = (C1x,C1y)
    C1x=AlicePrivateKey*bx
    C1y=AlicePrivateKey*by
    # print("y1=\t(",C1x,",",C1y,")\n")
    #Cipher text 2 generation ---> Y2 = (C2x,C2y)
    C2x=msg+AlicePrivateKey*Px
    C2y=msg+AlicePrivateKey*Py
    # print("y2=\t(",C2x,",",C2y,")\n")
    print('symmetric key encrypted')
    return C1x, C2x   
    
def decrypt(y1xx,y2xx):
    Mx=y2xx-BobPrivateKey*y1xx
    return Mx
    # print("Original plaintext (symmetric key) is:\t",Mx) 


n=1013 # prime number EC mod n
LHS=[[]] 
RHS=[[]]
LHS.append([])
RHS.append([])
a=r.randint(1, 100) # coefficient a in polynomial
b=r.randint(1, 100) # coefficient a in polynomial

#Polynomial
polynomial(LHS,RHS,n)

arr_x=[]
arr_y=[]
#Generating base points
count=points_generate(arr_x,arr_y,n)
    
#Calculation of Base Point
bx=arr_x[0]
by=arr_y[0]
# print("Base Point taken is:\t(",bx,",",by,")\n")

# Private key of Sender (key<n)
AlicePrivateKey = r.randint(1, 1000)
BobPrivateKey = r.randint(1, 1000)

#Q i.e. sender's public key generation
Qx=AlicePrivateKey*bx
Qy=AlicePrivateKey*by
# print("Public key of Alice is:\t(",Qx,",",Qy,")\n")
Px=BobPrivateKey*bx
Py=BobPrivateKey*by
# print("Public key of Bob is:\t(",Px,",",Py,")\n")


# M = 123
# #Cipher text 1 generation ---> Y1 = (C1x,C1y)
# C1x=k*bx
# C1y=k*by
# print("Value of Cipher text 1 i.e. C1:\t(",C1x,",",C1y,")\n")
# #Cipher text 2 generation ---> Y2 = (C2x,C2y)
# C2x=k*Qx+M
# C2y=k*Qy+M
# print("Value of Cipher text 2 i.e. C2:\t(",C2x,",",C2y,")\n")


# #Deryption
# Mx=C2x-AlicePrivateKey*C1x
# # My=C2y-AlicePrivateKey*C1y
# print("The message recieved by reciever is:\t",Mx)          