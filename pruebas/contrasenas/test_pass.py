#!/usr/bin/python3

from contrasenas import passw_manager

## Se inicializa la base
base = "prueba.db"
passwords = passw_manager(base)

## Se ingresan los usuarios de prueba
passwords.save_new("erick.sancho", "hola")

# print(passwords.comparar("erick.sancho", "hola"))

user = passwords.get_data("erick.sancho")

print(user)

print(passwords.editname('erick.sancho', 'Erick Alonso'))

user = passwords.get_data("erick.sancho")

print(user)