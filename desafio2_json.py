#--------------------- Módulos / Librerías ----------------------
# Se importa el módulo json para facilitar la lectura y escritura de archivos json.
import json

# Se importa una clase (SequenceMatcher) de una librería (difflib) que nos ayuda a calcular la similitud de dos strings basandonse en el ratio entre un string y otro.
from difflib import SequenceMatcher
#--------------------- Módulos / Librerías ----------------------

#--------------------- Funciones auxiliares ---------------------
def anadir_pregunta_y_respuesta(pregunta):
    respuesta = input("Escriba una respuesta para su pregunta: ")

    with open("preguntas.json", "r", encoding="utf-8", newline='') as archivo_json:
        
        data = json.load(archivo_json)

        # Se verifica cual es el siguiente número de pregunta en el archivo de preguntas.
        numero_de_pregunta = "pregunta_" + str(len(data) + 1)

        # Se añade la nueva pregunta del usuario con su respuesta
        data[numero_de_pregunta] = [
            {
            "pregunta": pregunta,
            "respuesta": respuesta
            }
        ]
        
        # Se abre el archivo json y se escribe la informacion anteriormente añadida en formato json.
        with open('preguntas.json', 'w', encoding='utf-8') as archivo_json_actualizado:
            json.dump(data, archivo_json_actualizado, ensure_ascii=False, indent=4)
        
        hacer_otra_pregunta()


def calcular_similtud(data, item, pregunta) -> float:
    ratio_de_similitud = SequenceMatcher(None, pregunta, data[item][0]["pregunta"]).ratio()
    return ratio_de_similitud


def buscar_y_responder_pregunta(data, preguntas_similares, respuesta_de_pregunta_similar):
    for item in data:
        if data[item][0]["pregunta"] == preguntas_similares[respuesta_de_pregunta_similar - 1]:
            print(data[item][0]["respuesta"])
            break
    
    hacer_otra_pregunta()


def hacer_otra_pregunta():
    se_quiere_hacer_otra_pregunta = input("Si quiere hacer otra pregunta escriba 'Sí'. Caso contrario, escriba 'No': ")

    if se_quiere_hacer_otra_pregunta.capitalize() == "Si" or se_quiere_hacer_otra_pregunta.capitalize() == "Sí":
        main()
    else:
        quit()


def caso_cero_preguntas_encontradas(pregunta):
    print("No se encontraron preguntas similares a la suya")

    aceptar_nueva_pregunta = input("Desea agregar su pregunta a la lista? Responda Si o No: ")

    # Si el usuario desea añadir su pregunta, se le pide que escriba una respuesta para esta.
    if aceptar_nueva_pregunta.capitalize() == "Si" or aceptar_nueva_pregunta.capitalize() == "Sí":
        anadir_pregunta_y_respuesta(pregunta)
    else:
        hacer_otra_pregunta()


def caso_una_pregunta_encontrada(pregunta: str, preguntas_similares: list):
    print("Se encontró " + str(len(preguntas_similares)) + " pregunta similar a la suya.")

    for item in preguntas_similares:
        print("1. " + item)

    respuesta_de_pregunta_similar = int(input("Escriba 1 para saber la respuesta a la pregunta similar encontrada, 2 para agregar su pregunta al archivo o 3 para cerrar el programa: "))
                    
    if respuesta_de_pregunta_similar == 1:
        with open("preguntas.json", "r", encoding="utf-8") as archivo_json:
            data = json.load(archivo_json)

            buscar_y_responder_pregunta(data, preguntas_similares, respuesta_de_pregunta_similar)
                    
    elif respuesta_de_pregunta_similar == len(preguntas_similares) + 1:
        anadir_pregunta_y_respuesta(pregunta)
                    
    else:
        hacer_otra_pregunta()


def caso_dos_o_mas_preguntas_encontradas(pregunta, preguntas_similares):
    print("Se encontraron " + str(len(preguntas_similares)) + " preguntas similares a la suya.")

    for n, item in enumerate(preguntas_similares):
        print(str(n + 1) + ". " + item)

    # Se le pide al usuario que escriba el número de la pregunta de la cual quiera saber la respuesta, u otros 2 números para agregar su pregunta al archivo o cerrar el programa respectivamente.
    respuesta_de_pregunta_similar = int(input("Escriba un número del 1 al " + str(len(preguntas_similares)) + " para saber la respuesta a la pregunta similar encontrada. Sino, escriba " + str(len(preguntas_similares) + 1) + " para agregar su pregunta al archivo o " + str(len(preguntas_similares) + 2) + " para cerrar el programa: "))

    if respuesta_de_pregunta_similar >= 1 and respuesta_de_pregunta_similar <= len(preguntas_similares):
        with open("preguntas.json", "r", encoding="utf-8") as archivo_json:
            data = json.load(archivo_json)

            buscar_y_responder_pregunta(data, preguntas_similares, respuesta_de_pregunta_similar)
                    
    elif respuesta_de_pregunta_similar == len(preguntas_similares) + 1:
        anadir_pregunta_y_respuesta(pregunta)
                    
    else:
        hacer_otra_pregunta()
#--------------------- Funciones auxiliares ---------------------


#---------------------- Función principal ----------------------
def main():
    pregunta = input("Escriba una pregunta: ")

    pregunta_encontrada = False 

    with open("preguntas.json", "r", encoding="utf-8") as archivo_json:  

        data = json.load(archivo_json)

        for item in data:     
            ratio_de_similitud = calcular_similtud(data, item, pregunta)

            if pregunta == data[item][0]["pregunta"] or ratio_de_similitud >= 0.85:
                pregunta_encontrada = True
                print(data[item][0]["respuesta"])
                break
    
        
        # Si la pregunta del usuario se encuentra, se retorna el programa. Sino, se prosigue con lo demas
        if pregunta_encontrada:
            hacer_otra_pregunta()
        
        # Se inicia una lista para llevar la cuenta de la cantidad de preguntas similares a la del usuario.
        preguntas_similares = []

        # Se calcula la similitud entre todas las preguntas del archivo y la pregunta del usuario, eso devuelve un número entre 0 y 1. Mientras más cercano al 1, más similares son las preguntas.
        with open("preguntas.json", "r", encoding="utf-8") as archivo_json:

            data = json.load(archivo_json)

            for item in data:
                ratio_de_similitud = calcular_similtud(data, item, pregunta)

                # Si el valor devuelto es mayor o igual a 0.58, significa que las preguntas son bastante similares, así que se procede a incrementar la variable de preguntas encontradas, además de agregar la pregunta a la lista.
                if ratio_de_similitud >= 0.58:
                    preguntas_similares.append(data[item][0]["pregunta"])


            # Despues de iterar sobre todas las preguntas del archivo json, se manejan los tres casos posibles de valores que puede tomar la variable de preguntas encontradas:
            if len(preguntas_similares) == 0:
                caso_cero_preguntas_encontradas(pregunta)
                
            elif len(preguntas_similares) == 1:
                caso_una_pregunta_encontrada(pregunta, preguntas_similares)
                
            else:
                caso_dos_o_mas_preguntas_encontradas(pregunta, preguntas_similares)
#---------------------- Función principal ----------------------


main()