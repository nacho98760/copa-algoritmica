#--------------------- Módulos / Librerías ----------------------
# Se importa el módulo json para facilitar la lectura y escritura de archivos json.
import json

# Se importa una clase (SequenceMatcher) de una librería (difflib) que nos ayuda a calcular la similitud de dos strings basandonse en el ratio entre un string y otro.
from difflib import SequenceMatcher
#--------------------- Módulos / Librerías ----------------------

#--------------------- Funciones ---------------------
def anadir_pregunta_y_respuesta(pregunta):
    respuesta = input("Escriba una respuesta para su pregunta: ")

    # Se abre el archivo json nuevamente
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

def main():

    # Se guarda la pregunta del usuario en una variable
    pregunta = input("Escriba una pregunta: ")

    # Boolean para saber si se encontró la pregunta del usuario
    pregunta_encontrada = False 

    with open("preguntas.json", "r", encoding="utf-8") as archivo_json:  

        data = json.load(archivo_json)

        for item in data:     
            # Se calcula la similitud entre la pregunta del archivo y la del usuario, eso devuelve un número entre 0 y 1. Mientras más cercano al 1, más similares son las preguntas.
            ratio_de_similitud = SequenceMatcher(None, pregunta, data[item][0]["pregunta"]).ratio()

            if pregunta == data[item][0]["pregunta"] or ratio_de_similitud >= 0.85:
                pregunta_encontrada = True
                print(data[item][0]["respuesta"])
                break
        
        # Si la pregunta del usuario se encuentra, se retorna el programa. Sino, se prosigue con lo demas
        if pregunta_encontrada:
            return
        
        # Se inician una variable y una lista respectivamente para llevar la cuenta de la cantidad de preguntas similares a la del usuario.
        cantidad_de_preguntas_similares_encontradas = 0
        preguntas_similares = []

        # Se calcula la similitud entre dicha línea y la pregunta del usuario, eso devuelve un número entre 0 y 1. Mientras más cercano al 1, más similares son las preguntas.
        with open("preguntas.json", "r", encoding="utf-8") as archivo_json:
            data = json.load(archivo_json)
            for item in data:
                ratio_de_similitud = SequenceMatcher(None, pregunta, data[item][0]["pregunta"]).ratio()

                # Si el valor devuelto es mayor o igual a 0.58, significa que las preguntas son bastante similares, así que se procede a incrementar la variable de preguntas encontradas, además de agregar la pregunta a la lista.
                if ratio_de_similitud >= 0.58:
                    cantidad_de_preguntas_similares_encontradas += 1
                    preguntas_similares.append(data[item][0]["pregunta"])

            # Despues de iterar sobre todas las preguntas del archivo json, se manejan los tres casos posibles de valores que puede tomar la variable de preguntas encontradas:

            # Si la variable es 0, se imprime que no hay preguntas similares y se le pregunta al usuario si quiere agregar su pregunta al archivo o no.
            if cantidad_de_preguntas_similares_encontradas == 0:
                print("No se encontraron preguntas similares a la suya")

                aceptar_nueva_pregunta = input("Desea agregar su pregunta a la lista? Responda Si o No: ")

                # Si el usuario desea añadir su pregunta, se le pide que escriba una respuesta para esta.
                if aceptar_nueva_pregunta.capitalize() == "Si" or aceptar_nueva_pregunta.capitalize() == "Sí":
                        anadir_pregunta_y_respuesta(pregunta)
                else:
                    quit()
                
            # Si la variable es 1, se imprime que se encontró 1 pregunta (singular) seguido de la lista que contiene la pregunta encontrada. 
            elif cantidad_de_preguntas_similares_encontradas == 1:
                print("Se encontró " + str(cantidad_de_preguntas_similares_encontradas) + " pregunta similar a la suya.")

                for item in preguntas_similares:
                    print("1. " + item)

                    
                # A continuación, se le pide al usuario que escriba 1 para saber la respuesta a su pregunta, 2 para agregar su pregunta al archivo o 3 para cerrar el programa.
                respuesta_de_pregunta_similar = int(input("Escriba 1 para saber la respuesta a la pregunta similar encontrada, 2 para agregar su pregunta al archivo o 3 para cerrar el programa: "))
                    

                if respuesta_de_pregunta_similar == 1:
                    with open("preguntas.json", "r", encoding="utf-8") as archivo_json:
                        data = json.load(archivo_json)

                        for item in data:
                            if data[item][0]["pregunta"] == preguntas_similares[0]:
                                print(data[item][0]["respuesta"])
                    
                elif respuesta_de_pregunta_similar == 2:
                        anadir_pregunta_y_respuesta(pregunta)
                    
                else:
                    quit()
                
            # Si la variable es 2 o más, se imprime que se encontraron "x" preguntas (plural) seguido de la lista que contiene las preguntas encontradas.
            else:
                print("Se encontraron " + str(cantidad_de_preguntas_similares_encontradas) + " preguntas similares a la suya.")
                counter = 0
                for item in preguntas_similares:
                    counter += 1
                    print(str(counter) + ". " + item)

                # A continuación, se le pide al usuario que escriba el número de la pregunta de la cual quiera saber la respuesta, u otros 2 números para agregar su pregunta al archivo o cerrar el programa respectivamente.
                respuesta_de_pregunta_similar = int(input("Escriba un número del 1 al " + str(len(preguntas_similares)) + " para saber la respuesta a la pregunta similar encontrada. Sino, escriba " + str(len(preguntas_similares) + 1) + " para agregar su pregunta al archivo o " + str(len(preguntas_similares) + 2) + " para cerrar el programa: "))

                # Si el número ingresado corresponde a una pregunta, se abre el archivo json y se busca la respuesta de la pregunta similar que el usuario haya elegido.
                if respuesta_de_pregunta_similar >= 1 and respuesta_de_pregunta_similar <= len(preguntas_similares):
                    with open("preguntas.json", "r", encoding="utf-8") as archivo_json:
                        data = json.load(archivo_json)
                        
                        for item in data:
                            if data[item][0]["pregunta"] == preguntas_similares[respuesta_de_pregunta_similar - 1]:
                                print(data[item][0]["respuesta"])
                    
                elif respuesta_de_pregunta_similar == len(preguntas_similares) + 1:
                    anadir_pregunta_y_respuesta(pregunta_encontrada)
                    
                else:
                    quit()
#--------------------- Funciones ---------------------


main()