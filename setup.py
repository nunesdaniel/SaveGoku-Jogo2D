import cx_Freeze
import os

executaveis = [ 
    cx_Freeze.Executable(script="main.py", icon="recursos/icons/icon.png") 
]

# Caminho absoluto para a pasta drivers do pyttsx3
pyttsx3_drivers_path = r"C:\Users\Daniel\AppData\Local\Programs\Python\Python313\Lib\site-packages\pyttsx3\drivers"

include_files = [
    "recursos",
    pyttsx3_drivers_path
]

cx_Freeze.setup(
    name = "Iron Man",
    options={
        "build_exe":{
            "packages": ["pygame", "pyttsx3"],
            "include_files": include_files
        }
    },
    executables=executaveis
)
