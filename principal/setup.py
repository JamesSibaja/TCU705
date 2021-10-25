from distutils.core import setup 
import py2exe 
 
setup(name="Bases de Datos Acosta", 
 version="1.0", 
 description="Breve descripcion", 
 author="autor", 
 author_email="email del autor", 
 url="url del proyecto", 
 license="tipo de licencia", 
 scripts=["main.py"], 
 console=["main.py"], 
 options={"py2exe": {"excludes": ["_pytest","qtpy"]}}, 
 zipfile=None,
)

#setup(options = {"py2exe":{   "excludes": ["_pytest","qtpy","pydevd"] } },