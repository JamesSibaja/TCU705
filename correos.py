import os
import pandas as pd

f = open('correos2.txt','a')
cant = 0
df = pd.read_excel('cv_acosta.xlsx')
correoDireccion = ''
listo = False
for correo in df['Correo electronico'].values:
    for letra in str(correo):
        if letra == '@':
            listo = True
        if (letra == '/' or letra == ' ') and listo:
            f.write(correoDireccion +',')
            cant += 1
            listo = False
            correoDireccion = ''
        if not (letra == '/' or letra == ' '):
            correoDireccion = correoDireccion + letra
    if not correoDireccion == 'nan':
        f.write(correoDireccion +',')
        cant += 1
    listo = False
    correoDireccion = ''
print (cant)
f.close()