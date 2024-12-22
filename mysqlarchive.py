import mysql.connector                      # Importa el módulo mysql.connector
from kivyarchive import (menuApp1, 
                         menuApp2, 
                         menuApp3, 
                         menuApp4, 
                         menuApp5)          # Importa las funciones de la librería kivyarchive

def Crea_lista(conexion, tabla,             # Función que crea una lista de los campos de una tabla
               campo,lambdeo = 0, 
               appendeo = 0):               # Función que crea una lista de los campos de una tabla
    cursor = conexion.cursor()              # Crea un cursor para la conexión
    query = f"SELECT {campo} FROM {tabla}"  # Crea una consulta SQL para seleccionar los campos de la tabla
    cursor.execute(query)                   # Ejecuta la consulta
    lista = cursor.fetchall()               # Guarda los resultados de la consulta en una lista
    if lambdeo == 0:                        # Si lambdeo es 0
        lista.sort(key=lambda x: x[2])      # Ordena la lista por el tercer elemento
    elif lambdeo == 1:                      # Si lambdeo es 1
        lista.sort(key=lambda x: x[1])      # Ordena la lista por el segundo elemento
    Lista = []                              # Crea una lista vacía
    for i in lista:                         # Para cada elemento en la lista
        if appendeo == 0:                   # Si appendeo es 0
            Lista.append(f"{i[0]} - {i[2]}, {i[1]}")
        elif appendeo == 1:                 # Si appendeo es 1
            Lista.append(f"{i[0]} - {i[1]}")# Añade a la lista el primer y segundo elemento
        elif appendeo == 2:                 # Si appendeo es 2
            Lista.append(i[0])              # Añade a la lista el primer elemento
    if lambdeo == 2:                        # Si lambdeo es 2
        Lista.sort()                        # Ordena la lista
    return Lista                            # Devuelve la lista
    
def conectar():                             # Función que conecta con la base de datos
    try:                                    # Intenta
        conexion = mysql.connector.connect(
            host="192.168.1.150",           # O la IP del servidor si es remoto
            user="casa",                    # Nombre de usuario
            password="chumino",             # Contraseña
            database="Biblioteca"           # Nombre de la base de datos
        )
        if conexion.is_connected():         # Si la conexión está establecida
            Mensaje = menuApp4(
                tamañoVentana = (600, 200),
                texto = "Conexión establecida",
                boton = "Continuar")        # Muestra un mensaje
            Mensaje.run()                   # Ejecuta el mensaje
            return conexion                 # Devuelve la conexión
    except mysql.connector.Error as err:    # Si hay un error
        Mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = f"Error de conexión: {err}",
            boton = "Volver")               # Muestra un mensaje
        Mensaje.run()                       # Ejecuta el mensaje
        return None                         # Devuelve None

def insertar_autor(conexion, nombre, apellidos):
    # Primero comprueba si ese autor con nombre y apellidos ya existe
    cursor = conexion.cursor()
    query = "SELECT id_autor FROM autor WHERE nombre = %s AND apellidos = %s"
    values = (nombre, apellidos)
    cursor.execute(query, values)
    autor = cursor.fetchone()
    # Si el autor ya existe, no lo inserta
    if autor:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "El autor ya existe en la base de datos",
            boton = "Volver")
        mensaje.run()
        return
    elif not nombre:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "El nombre del autor no puede estar vacío",
            boton = "Volver")
        mensaje.run()
        return    
    # Inserta el autor en la tabla autor
    cursor = conexion.cursor()
    query = "INSERT INTO autor (nombre, apellidos) VALUES (%s, %s)"
    values = (nombre, apellidos)
    cursor.execute(query, values)
    conexion.commit()
    mensaje = menuApp4(
        tamañoVentana = (600, 200),
        texto = "Autor insertado correctamente",
        boton = "Volver")
    mensaje.run()

def insertar_libro(conexion, idioma, año, tipologia, id_genero, estantería, título):
    cursor = conexion.cursor()
    query = "INSERT INTO libros (idioma, año, tipologia, id_genero, estantería, título) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (idioma, año, tipologia, id_genero, estantería, título)
    cursor.execute(query, values)
    conexion.commit()
    print("Libro insertado correctamente")

def insertar_genero(conexion, nombre_genero):   
    cursor = conexion.cursor()
    query = "SELECT id_genero FROM genero WHERE nombre = %s"
    cursor.execute(query, (nombre_genero,))
    genero = cursor.fetchone()
    if genero:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "El género ya existe en la base de datos",
            boton = "Volver")
        mensaje.run()
        return
    elif not nombre_genero:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "El nombre del género no puede estar vacío",
            boton = "Volver")
        mensaje.run()
        return
    # insertar el genero en la tabla genero
    query = "INSERT INTO genero (nombre) VALUES (%s)"
    ejecutar_Un_query(conexion,query, (nombre_genero,),
                      "Género insertado correctamente",
                      "Error al insertar el género")
    
def insertar_editorial(conexion, nombre_editorial):
    cursor = conexion.cursor()
    query = "SELECT id_editorial FROM editorial WHERE nombre = %s"
    values = (nombre_editorial,)
    cursor.execute(query, values)
    editorial = cursor.fetchone()
    if editorial:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "La editorial ya existe en la base de datos",
            boton = "Volver")
        mensaje.run()
        return
    elif not nombre_editorial:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "El nombre de la editorial no puede estar vacío",
            boton = "Volver")
        mensaje.run()
        return
       
    query = "INSERT INTO editorial (nombre) VALUES (%s)"
    ejecutar_Un_query(conexion,query, (nombre_editorial,),
                        "Editorial insertada correctamente",
                        "Error al insertar la editorial")    

def obtener_libros_y_autores(conexion):
    cursor = conexion.cursor()
    Lista_Autores = Crea_lista(conexion, "autor", "id_autor, nombre, apellidos")         
    Lista_tipología = ["Ficción", "No ficción"]
    Lista_Idiomas = ["Castellano", "Catalán", "Inglés", "Francés", "Japonés", "Alemán", "Italiano", "Portugués", "Otros"]
    Lista_Generos = Crea_lista(conexion, "genero", "id_genero, nombre",1 , 1)
    Lista_Editoriales = Crea_lista(conexion, "editorial", "nombre",2, 2)
    Preguntas = menuApp3(
        title = "Buscando libros",
        tamañoVentana = (500, 1080),
        opciones =[
            "Título",
            "Estantería",
            "Año",
            "Idioma",
            "Tipología",
            "Editorial",
            "Género",
            "Autor"
        ],
        texto = "Deja en blanco para no aplicar un filtro",
        textoBoton="Buscar",
        tipo = [[0],[0],[0],[1,Lista_Idiomas],[1,Lista_tipología],[1,Lista_Editoriales],[1,Lista_Generos],[1,Lista_Autores]]
    )
    Preguntas.run()
    # Construcción dinámica de la consulta SQL
    
    # Solicitar filtros al usuario
    titulo = Preguntas.valores["valor_1"].text
    estanteria = Preguntas.valores["valor_2"].text
    año = Preguntas.valores["valor_3"].text
    idioma = Preguntas.valores["valor_4"].text
    tipologia = Preguntas.valores["valor_5"].text
    editorial = Preguntas.valores["valor_6"].text
    id_genero = Preguntas.valores["valor_7"].text
    id_autor = Preguntas.valores["valor_8"].text
    # Buscamos el id_editorial en la tabla editorial que tenga el nombre editorial
    query = "SELECT id_editorial FROM editorial WHERE nombre = %s"
    cursor.execute(query, (editorial,))
    id_editorial = cursor.fetchone()
    if id_editorial:
        id_editorial = id_editorial[0]  
    else:
        id_editorial = "Despliega y escoge"        
    # Construcción dinámica de la consulta SQL
    filtros = []
    valores = []
    
    if titulo:
        filtros.append("libros.Título LIKE %s")
        valores.append(f"%{titulo}%")
    if estanteria:
        filtros.append("libros.Estantería = %s")
        valores.append(estanteria)
    if idioma and idioma != "Despliega y escoge":
        filtros.append("libros.idioma = %s")
        valores.append(idioma)
    if año:
        filtros.append("libros.año = %s")
        valores.append(año)
    if tipologia  and tipologia != "Despliega y escoge":
        filtros.append("libros.tipologia = %s")
        valores.append(tipologia)
    if id_editorial and id_editorial != "Despliega y escoge":
        filtros.append("libros.id_editorial = %s")
        valores.append(id_editorial)
    if id_genero  and id_genero != "Despliega y escoge":
        filtros.append("libros_géneros.id_genero = %s")
        valores.append(id_genero)
    if id_autor  and id_autor != "Despliega y escoge":
        filtros.append("libros_autores.id_autor = %s")
        valores.append(id_autor)

    # Construcción de la cláusula WHERE
    where_clause = " AND ".join(filtros)
    if where_clause:
        where_clause = "WHERE " + where_clause

    # Consulta con filtros
    query = f"""
    SELECT libros.id_libro, libros.Título, libros.Estantería, libros.idioma, libros.año, libros.tipologia,
           (SELECT nombre FROM editorial WHERE editorial.id_editorial = libros.id_editorial) AS editorial,
           GROUP_CONCAT(DISTINCT genero.nombre SEPARATOR ', ') AS generos, 
           GROUP_CONCAT(DISTINCT CONCAT(autor.nombre, ' ', autor.apellidos) SEPARATOR ', ') AS autores
    FROM libros
    JOIN libros_autores ON libros.id_libro = libros_autores.id_libro
    JOIN autor ON libros_autores.id_autor = autor.id_autor
    JOIN libros_géneros ON libros.id_libro = libros_géneros.id_libro
    JOIN genero ON libros_géneros.id_genero = genero.id_genero
    {where_clause}
    GROUP BY libros.id_libro;
    """
    # Ejecutar la consulta
    cursor.execute(query, valores)
    resultados = cursor.fetchall()

    # Mostrar resultados
    if resultados:
        if len(resultados) > 1:
            # Quitamos de la lista de resultados todos los datos de cada lista menos los dos primeros
            for i in range(len(resultados)):
                resultados[i] = resultados[i][0:2]
            
            resultados.sort(key=lambda x: x[1])    
            Listado = menuApp2(
                title = "Listado de libros",
                tamañoVentana = (800, 900),
                lista=resultados,
            )
            Listado.run()
        else:
            # convierte resultados en una lista única con la primera lista dentro de él
            resultados1 = resultados[0]
            valores = ["id", "Título", "Estantería", "Idioma", "Año", "Tipologia", "Editorial", "Géneros", "Autores"]
            # Convierte resultados en una lista de listas con 2 valores en cada una el correspondiente a valores y el correspondiente a resultados
            a=0
            resultados = []
            for i in valores:
                resultados.append([i, resultados1[a]])
                a += 1          
            Listado = menuApp2(
                title = "Único libro encontrado",
                tamañoVentana = (800, 400),
                lista=resultados,
            )
            Listado.run()
                    
    else:
        mensaje = menuApp4(
            tamañoVentana = (600, 200),
            texto = "No se encontraron resultados",
            boton = "Volver")
        mensaje.run()

def ver_autores(conexion):
    cursor = conexion.cursor()
    Preguntas = menuApp3(
        title = "Buscando autores",
        tamañoVentana = (500, 290),
        opciones =[
            "Nombre",
            "Apellidos"
        ],
        texto = "Deja en blanco para no aplicar un filtro",
        textoBoton="Buscar",
        tipo = [[0],[0]]
    )
    Preguntas.run()
    
    # Construcción dinámica de la consulta SQL
    filtros = []
    valores = []
    # si hay algo en el diccionario Preguntas.valores donde la clave es valor_1...
    valor1 = Preguntas.valores["valor_1"].text
    valor2 = Preguntas.valores["valor_2"].text
    if valor1:
        filtros.append("autor.nombre LIKE %s")
        valores.append(f"%{valor1}%")
    if valor2:
        filtros.append("autor.apellidos LIKE %s")
        valores.append(f"%{valor2}%")
    
    # Construcción de la cláusula WHERE
    where_clause = " AND ".join(filtros)
    if where_clause:
        where_clause = "WHERE " + where_clause
        
    # Consulta con filtros
    query = f"""
    SELECT id_autor, nombre, apellidos
    FROM autor
    {where_clause}
    """ 
    cursor.execute(query, valores)
    autores = cursor.fetchall()
    autores.sort(key=lambda x: x[2])
    for i in range(len(autores)):
        autores[i] = (autores[i][0], autores[i][2], autores[i][1])
    Lista = menuApp2(
        title = "Listado de autores",
        tamañoVentana = (300, 900),
        lista=autores,
        arquetipos = ","    

    )
    Lista.run()

def ver_generos(conexion):
    cursor = conexion.cursor()
    query = "SELECT id_genero, nombre FROM genero"
    cursor.execute(query)   
    generos = cursor.fetchall()
    # Ordena generos alfabéticamente por el valor [1]
    generos.sort(key=lambda x: x[1])
    Lista = menuApp2(
        title = "Listado de géneros",
        tamañoVentana = (300, 900),
        lista=generos

    )
    Lista.run()

def ver_editoriales(conexion):
    cursor = conexion.cursor()
    query = "SELECT id_editorial, nombre FROM editorial"
    cursor.execute(query)
    editoriales = cursor.fetchall()
    editoriales.sort(key=lambda x: x[1])
    Lista = menuApp2(
        title = "Listado de editoriales",
        tamañoVentana = (300, 900),
        lista=editoriales
    )
    Lista.run()    

def actualizar_autor(conexion, autor):
    cursor = conexion.cursor()
    # id_autor es el número del principio de la cadena autor hasta el primer espacio
    id_autor = int(autor.split(" ")[0])
    #autor es ahora desde "- " hasta el final de la cadena sin contar "- "
    autor = autor.split(" - ")[1]
    
    másPreguntas = menuApp1(
        title = f"Actualiza {autor}",
        tamañoVentana = (500, 200),
        opciones =[
            "Nombre",
            "Apellidos"
        ],
        colores = [ (0.4, 1, 0, 1), (0.4, 1, 0, 1)]
    )
    másPreguntas.run()
    if másPreguntas.valor == "Nombre":
        Dato = menuApp3(
            title = "Actualiza nombre",
            tamañoVentana = (500, 250),
            opciones =[ "Nombre"],
            texto = "Introduce el nuevo nombre del autor",
            textoBoton="Introducir",
            tipo = [[0]]
        )
        Dato.run()
        nuevo_nombre = Dato.valores["valor_1"].text
        query = "UPDATE autor SET nombre = %s WHERE id_autor = %s"
        values = (nuevo_nombre, id_autor)
        ejecutar_Un_query(conexion,query, values,
                          f"Nombre actualizado correctamente",
                          f"Error al actualizar el nombre")

    
    elif másPreguntas.valor == "Apellidos":
        Dato = menuApp3(
            title = "Actualiza apellidos",
            tamañoVentana = (500, 250),
            opciones =[ "Apellidos"],
            texto = "Introduce los nuevos apellidos del autor",
            textoBoton="Introducir",
            tipo = [[0]]
        )
        Dato.run()
        nuevos_apellidos = Dato.valores["valor_1"].text
        query = "UPDATE autor SET apellidos = %s WHERE id_autor = %s"
        values = (nuevos_apellidos, id_autor)
        ejecutar_Un_query(conexion,query, values,
                            f"Apellidos actualizados correctamente",
                            f"Error al actualizar los apellidos")            

def actualizar_genero(conexion, genero):
    cursor = conexion.cursor()
    id_genero = int(genero.split(" ")[0])
    genero = genero.split(" - ")[1]
    Dato = menuApp3(
        title = "Actualiza género",
        tamañoVentana = (500, 250),
        opciones =[ "Nombre"],
        texto = "Introduce el nuevo nombre del género",
        textoBoton="Introducir",
        tipo = [[0]]
    )
    Dato.run()
    nuevo_nombre = Dato.valores["valor_1"].text
    query = "UPDATE genero SET nombre = %s WHERE id_genero = %s"
    values = (nuevo_nombre, id_genero)
    ejecutar_Un_query(conexion,query, values,
                        f"Género actualizado correctamente",
                        f"Error al actualizar el género")
        
def actualizar_editorial(conexion, editorial):
    cursor = conexion.cursor()
    id_editorial = int(editorial.split(" ")[0])
    editorial = editorial.split(" - ")[1]
    Dato = menuApp3(
        title = "Actualiza editorial",
        tamañoVentana = (500, 250),
        opciones =[ "Nombre"],
        texto = "Introduce el nuevo nombre de la editorial",
        textoBoton="Introducir",
        tipo = [[0]]
    )
    Dato.run()
    nuevo_nombre = Dato.valores["valor_1"].text
    query = "UPDATE editorial SET nombre = %s WHERE id_editorial = %s"
    values = (nuevo_nombre, id_editorial)
    ejecutar_Un_query(conexion,query, values,
                        f"Editorial actualizada correctamente",
                        f"Error al actualizar la editorial")

def eliminar_libro(conexion, id_libro,nombre):
    estasSeguro = menuApp1(
        title = f"Eliminar {nombre}",
        tamañoVentana = (500, 200),
        opciones =[
            "Sí",
            "No"
        ],
        colores = [ (1, 0, 0, 1), (0.4, 1, 0, 1)]
    )
    estasSeguro.run()
    respuesta = estasSeguro.valor
    if respuesta == "No":
        return
    cursor = conexion.cursor()

    # Primero eliminamos las relaciones en la tabla intermedia
    query = "DELETE FROM libros_autores WHERE id_libro = %s"
    ejecutar_Un_query(conexion,query, (id_libro,))
    query = "DELETE FROM libros_géneros WHERE id_libro = %s"
    ejecutar_Un_query(conexion,query, (id_libro,))    
    # Luego eliminamos el libro
    query = "DELETE FROM libros WHERE id_libro = %s"
    ejecutar_Un_query(conexion,query, (id_libro,),
                      "Libro eliminado correctamente",
                        "Error al eliminar el libro")
    
def eliminar_autor(conexion, id_autor,nombre):
    estasSeguro = menuApp1(
        title = f"Eliminar {nombre}",
        tamañoVentana = (500, 200),
        opciones =[
            "Sí",
            "No"
        ],
        colores = [ (1, 0, 0, 1), (0.4, 1, 0, 1)]
    )  
    estasSeguro.run()
    respuesta = estasSeguro.valor
    if respuesta == "No":
        return
    cursor = conexion.cursor()

    # Primero eliminamos las relaciones en la tabla intermedia
    query = "DELETE FROM libros_autores WHERE id_autor = %s"
    ejecutar_Un_query(conexion,query, (id_autor,))
    # Luego eliminamos el autor
    query = "DELETE FROM autor WHERE id_autor = %s"
    ejecutar_Un_query(conexion,query, (id_autor,),
                      "Autor eliminado correctamente",
                        "Error al eliminar el autor")

def eliminar_genero(conexion, id_genero,nombre):
    EstasSeguro = menuApp1(
        title = f"Eliminar {nombre}",
        tamañoVentana = (500, 200),
        opciones =[
            "Sí",
            "No"
        ],
        colores = [ (1, 0, 0, 1), (0.4, 1, 0, 1)]
    )
    EstasSeguro.run()
    respuesta = EstasSeguro.valor
    if respuesta == "No":
        return
    
    cursor = conexion.cursor()

    # Primero eliminamos la tabla intermedia
    query = "DELETE FROM libros_géneros WHERE id_genero = %s"
    ejecutar_Un_query(conexion,query, (id_genero,))    
    # Luego eliminamos el género
    query = "DELETE FROM genero WHERE id_genero = %s"
    ejecutar_Un_query(conexion,query, (id_genero,),
                        "Género eliminado correctamente",
                            "Error al eliminar el género")

def eliminar_editorial(conexion, id_editorial,nombre):
    EstasSeguro = menuApp1(
        title = f"Eliminar {nombre}",
        tamañoVentana = (500, 200),
        opciones =[
            "Sí",
            "No"
        ],
        colores = [ (1, 0, 0, 1), (0.4, 1, 0, 1)]
    )
    EstasSeguro.run()
    respuesta = EstasSeguro.valor
    if respuesta == "No":
        return
    cursor = conexion.cursor()
    
    # Primero eliminamos de la tabla libros los libros que tengan el id_editorial y lo cambiamos por Null
    query = "UPDATE libros SET id_editorial = NULL WHERE id_editorial = %s"
    ejecutar_Un_query(conexion,query, (id_editorial,))  
    # Luego eliminamos la editorial
    query = "DELETE FROM editorial WHERE id_editorial = %s"
    ejecutar_Un_query(conexion,query, (id_editorial,),
                        "Editorial eliminada correctamente",
                        "Error al eliminar la editorial")

def ejecutar_Un_query(conexion,query, valores,mensaje_bueno="", mensaje_malo="Error indefinido"):
    try:
        cursor = conexion.cursor()
        cursor.execute(query, valores)
        conexion.commit()
        if mensaje_bueno:
            mensaje = menuApp4(
                tamañoVentana = (800, 200),
                texto = mensaje_bueno,
                boton = "Volver")
            mensaje.run()
        return cursor.lastrowid
    except Exception as e:
        print(e)
        mensaje = menuApp4(
            tamañoVentana = (800, 200),
            texto = mensaje_malo,
            boton = "Volver")
        mensaje.run()
        
def main():
    conexion = conectar()
    if conexion:
            while True:

                ventana = menuApp1(
                    title = "Menú principal",
                    tamañoVentana = (500, 920),
                    opciones = [
                        "Introduce libro", "Introduce autor", "Introduce género", "Introduce editorial",
                        "Consulta libros", "Consulta autores", "Consulta géneros", "Consulta editoriales",
                        "Actualiza un libro", "Actualiza un autor", "Actualiza un género", "Actualiza una editorial",
                        "Elimina un libro", "Elimina un autor", "Elimina un género", "Elimina una editorial", "Salir"
                    ],
                    colores = [
                        (0.4, 1, 0, 1), (0.4, 1, 0, 1), (0.4, 1, 0, 1), (0.4, 1, 0, 1),
                        (0.5, 0, 1, 1), (0.5, 0, 1, 1), (0.5, 0, 1, 1), (0.5, 0, 1, 1), 
                        (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), (0.5, 0.5, 0, 1), 
                        (0.6, 0, 0, 1), (0.6, 0, 0, 1), (0.6, 0, 0, 1), (0.6, 0, 0, 1), 
                        (0.4, 0.4, 0.4, 1)
                    ]
                )
                ventana.run()
                if ventana.valor == "Salir":
                    conexion.close()
                    exit()
                    
                elif ventana.valor == "Introduce autor":
                    Preguntas = menuApp3(
                        title = "Introduce autor",
                        tamañoVentana = (500, 330),
                        opciones =[
                            "Nombre",
                            "Apellidos",
                        ],
                        texto = "Introduce los datos del autor",
                        textoBoton="Introducir",
                        tipo = [[0],[0]]
                        
                    )
                    Preguntas.run()
                    nombre = Preguntas.valores["valor_1"].text
                    apellidos = Preguntas.valores["valor_2"].text
                    insertar_autor(conexion, nombre, apellidos)

                elif ventana.valor == "Introduce libro":
                    cursor = conexion.cursor()
                    Lista_Autores = Crea_lista(conexion, "autor", "id_autor, nombre, apellidos")
                    Lista_Generos = Crea_lista(conexion, "genero", "id_genero, nombre",1 , 1)
                    Lista_Editoriales = Crea_lista(conexion, "editorial", "nombre",2, 2)
                    Lista_tipología = ["Ficción", "No ficción"]
                    Lista_Idiomas = ["Castellano", "Catalán", "Inglés", "Francés", "Japonés", "Alemán", "Italiano", "Portugués", "Otros"]
                    Datos = menuApp3(
                        title = "Introduce libro",
                        tamañoVentana = (500, 880),
                        opciones =[
                            "Título",
                            "Estantería",
                            "Año",
                            "Idioma",
                            "Tipología",
                            "Editorial"
                        ],
                        texto = "Introduce los datos del libro",
                        textoBoton="Introducir",
                        tipo = [[0],[0],[0],[1,Lista_Idiomas],[1,Lista_tipología],[1,Lista_Editoriales]]
                        
                    )
                    Datos.run()
                    título = Datos.valores["valor_1"].text
                    estantería = Datos.valores["valor_2"].text
                    año = Datos.valores["valor_3"].text
                    idioma = Datos.valores["valor_4"].text
                    tipologia = Datos.valores["valor_5"].text
                    Editorial = Datos.valores["valor_6"].text
                    # Para Editorial, tenemos que encontrar el id_editorial en la tabla editorial que tenga el nombre Datos.valores["valor_6"].text
                    query = "SELECT id_editorial FROM editorial WHERE nombre = %s"
                    cursor.execute(query, (Editorial,))
                    editorial = cursor.fetchone()
                    if editorial:
                        Editorial = editorial[0]
                    else:
                        Editorial = None
                    # Insertar el libro en la tabla libros
                    cursor = conexion.cursor()
                    query_libro = "INSERT INTO libros ( idioma, año, tipologia, estantería, título, id_editorial) VALUES (%s, %s, %s, %s, %s, %s)"
                    id_libro = ejecutar_Un_query(conexion,query_libro, 
                                      (idioma, año, tipologia, estantería, título, Editorial))
                    # Obtener el ID del libro recién insertado
                    #id_libro = cursor.lastrowid
                    # Relacionar Autores con el libro
                    Seleccion = menuApp5(
                        título = "Selecciona autores",
                        tamañoVentana = (500, 600),
                        texto = "Selecciona los autores del libro",
                        textoBoton="Introducir",
                        ListaDeOpciones = Lista_Autores,
                    )
                    Seleccion.run()
                    autores = []
                    for i in Seleccion.selected_options:
                        autores.append(int(i.split(" ")[0]))
                    # Añadir autores al libro
                    # De la cadeta autores, quita todos los { } y ' y crea una lista separando por las ,
                    for id_autor in autores:    
                        query_relacion = "INSERT INTO libros_autores (id_libro, id_autor) VALUES (%s, %s)"
                        ejecutar_Un_query(conexion,query_relacion, (id_libro, id_autor),
                                          mensaje_malo="Error al insertar los autores")
                    # Relacionar Géneros con el libro
                    Seleccion = menuApp5(
                        título = "Selecciona géneros",
                        tamañoVentana = (500, 600),
                        texto = "Selecciona los géneros del libro",
                        textoBoton="Introducir",
                        ListaDeOpciones = Lista_Generos,
                    )
                    Seleccion.run()
                    generos = []
                    for i in Seleccion.selected_options:
                        generos.append(int(i.split(" ")[0]))
                    # Añadir géneros al libro
                    for id_genero in generos:
                        query_relacion = "INSERT INTO libros_géneros (id_libro, id_genero) VALUES (%s, %s)"
                        ejecutar_Un_query(conexion,query_relacion, (id_libro, id_genero),
                                            "Libro insertado correctamente",
                                            "Error al insertar los géneros")
                elif ventana.valor == "Introduce género":
                    Preguntas = menuApp3(
                        title = "Introduce género",
                        tamañoVentana = (500, 330),
                        opciones =[
                            "Nombre"
                        ],
                        texto = "Introduce el nombre del género",
                        textoBoton="Introducir",
                        tipo = [[0]]
                    )
                    Preguntas.run()
                    nombre_genero = Preguntas.valores["valor_1"].text
                    insertar_genero(conexion, nombre_genero)

                elif ventana.valor == "Introduce editorial":
                    Preguntas = menuApp3(
                        title = "Introduce editorial",
                        tamañoVentana = (500, 330),
                        opciones =[
                            "Nombre"
                        ],
                        texto = "Introduce el nombre de la editorial",
                        textoBoton="Introducir",
                        tipo = [[0]]
                    )
                    Preguntas.run()
                    nombre_editorial = Preguntas.valores["valor_1"].text
                    insertar_editorial(conexion, nombre_editorial)
                    
                elif ventana.valor == "Consulta autores":
                    ver_autores(conexion)  # Llamar a la función para ver los autores

                elif ventana.valor == "Consulta géneros":
                    ver_generos(conexion)  # Llamar a la función para ver los géneros

                elif ventana.valor == "Consulta libros":
                    obtener_libros_y_autores(conexion)

                elif ventana.valor == "Consulta editoriales":
                    ver_editoriales(conexion)
                    
                elif ventana.valor == "Actualiza un libro":
                    cursor = conexion.cursor()
                    Lista_Libros = []
                    query = "SELECT id_libro, título FROM libros"
                    cursor.execute(query)
                    libros = cursor.fetchall()
                    libros.sort(key=lambda x: x[1])
                    for libro in libros:
                        Lista_Libros.append(f"{libro[0]} - {libro[1]}")
                    Seleccion = menuApp3(
                        title = "Selecciona un libro",
                        tamañoVentana = (500, 600),
                        opciones =[
                            "Libro"
                        ],
                        texto = "Selecciona un libro para actualizar",
                        textoBoton="Seleccionar",
                        tipo = [[1,Lista_Libros]]
                    )
                    Seleccion.run()
                    libro = Seleccion.valores["valor_1"].text
                    print(libro)
                    libroTexto = libro.split(" - ")[1]
                    # Buscamos el id del libro
                    query = "SELECT id_libro FROM libros WHERE id_libro = %s"
                    cursor.execute(query, (libro,))
                    libro = cursor.fetchone()
                    if libro:
                        id_libro = libro[0]
                    else:
                        id_libro = None                    
                    while True:
                        ventana = menuApp1(
                            title = f"Actualiza {libroTexto}",
                            tamañoVentana = (500, 270),
                            opciones = [
                                "Actualiza datos", "Actualiza autores asociados", "Actualiza géneros asociados", "Volver"
                            ],
                            colores = [
                                (0.4, 1, 0, 1), (0.4, 0, 1, 1), (0.5, 0.5, 0, 1), (0.4, 0.4, 0.4, 1)
                            ]
                        )
                        ventana.run()
                        if ventana.valor == "Actualiza datos":
                            # Actualizar detalles del libro
                            Lista_Idiomas = ["Castellano", "Catalán", "Inglés", "Francés", "Japonés", "Alemán", "Italiano", "Portugués", "Otros"]
                            Lista_tipología = ["Ficción", "No ficción"]
                            Lista_Editoriales = Crea_lista(conexion, "editorial", "nombre",2, 2)                          
                            Datos = menuApp3(
                                title = f"Actualiza {libroTexto}",
                                tamañoVentana = (500, 880),
                                opciones =[
                                    "Título",
                                    "Estantería",
                                    "Año",
                                    "Idioma",
                                    "Tipología",
                                    "Editorial"
                                ],
                                texto = "Deja en blanco para no actualizar un campo",
                                textoBoton="Introducir",
                                tipo = [[0],[0],[0],[1,Lista_Idiomas],[1,Lista_tipología],[1,Lista_Editoriales]]
                            )
                            Datos.run()
                            titulo = Datos.valores["valor_1"].text
                            estanteria = Datos.valores["valor_2"].text
                            año = Datos.valores["valor_3"].text
                            idioma = Datos.valores["valor_4"].text
                            tipologia = Datos.valores["valor_5"].text
                            Editorial = Datos.valores["valor_6"].text
                            if Editorial == "Despliega y escoge":
                                id_editorial = None
                            # Buscamos el id_editorial en la tabla editorial
                            else:
                                query = "SELECT id_editorial FROM editorial WHERE nombre = %s"
                                cursor.execute(query, (Editorial,))
                                editorial = cursor.fetchone()
                                id_editorial = editorial[0]
                            
                            query_update = """
                            UPDATE libros
                            SET 
                                idioma = CASE WHEN %s != 'Despliega y escoge' THEN %s ELSE idioma END,
                                año = CASE WHEN %s != '' THEN %s ELSE año END,
                                tipologia = CASE WHEN %s != 'Despliega y escoge' THEN %s ELSE tipologia END,
                                estantería = CASE WHEN %s != '' THEN %s ELSE estantería END,
                                título = CASE WHEN %s != '' THEN %s ELSE título END,
                                id_editorial = CASE
                                    WHEN %s IS NOT NULL THEN %s
                                    ELSE id_editorial
                                END
                            WHERE id_libro = %s
                            """
                            cursor = conexion.cursor()
                            ejecutar_Un_query(conexion,query_update, (idioma, idioma,
                                año, año,tipologia, tipologia,estanteria, estanteria, 
                                titulo, titulo,id_editorial, id_editorial,id_libro
                            ),
                                "Libro actualizado correctamente",
                                "Error al actualizar el libro")
                        elif ventana.valor == "Actualiza autores asociados":
                            cursor = conexion.cursor()
                            # Actualizar autores asociados
                            while True:
                                ventana = menuApp1(
                                    title = "Actualiza autores asociados",
                                    tamañoVentana = (500, 270),
                                    opciones = [
                                        "Añadir autor", "Eliminar autor", "Volver"
                                    ],
                                    colores = [
                                        (0.4, 1, 0, 1), (0.4, 0, 1, 1), (0.4, 0.4, 0.4, 1)
                                    ]
                                )
                                ventana.run()

                                if ventana.valor == "Añadir autor":
                                    cursor = conexion.cursor()
                                    Lista_Autores = Crea_lista(conexion, "autor", "id_autor, nombre, apellidos")         
                                    añadir = menuApp3(
                                        title = "Añadir autor",
                                        tamañoVentana = (500, 600),
                                        opciones =[ "Autor"],
                                        texto = "Selecciona un autor para añadir al libro",
                                        textoBoton="Añadir",
                                        tipo = [[1,Lista_Autores]]
                                    )
                                    añadir.run()
                                    autor = añadir.valores["valor_1"].text
                                    id_autor = int(autor.split(" ")[0])
                                    autor = autor.split(" - ")[1]
                                    # Mira si hay en la tabla libros_autores ya especificada la relación id_libro, id_autor
                                    query_verificar_autor = "SELECT id_libro, id_autor FROM libros_autores WHERE id_autor = %s"
                                    cursor.execute(query_verificar_autor, (id_libro,))
                                    revision = cursor.fetchall()
                                    # Miramos si el segundo valor de alguna lista de revision es igual a id_autor
                                    if id_autor in [x[1] for x in revision]:
                                            mensaje = menuApp4(
                                                tamañoVentana = (600, 200),
                                                texto = f"El autor {autor} ya está asociado al libro",
                                                boton = "Volver")
                                            mensaje.run()
                                            break
                                    query_verificar_autor = "SELECT id_autor FROM autor WHERE id_autor = %s"
                                    cursor.execute(query_verificar_autor, (id_autor,))  
                                    cursor.fetchall()                                
                                    query_insert_autor = "INSERT INTO libros_autores (id_libro, id_autor) VALUES (%s, %s)"
                                    ejecutar_Un_query(conexion,query_insert_autor, (id_libro, id_autor),
                                                      "Autor añadido correctamente",
                                                        "Error al añadir el autor")                                                       
                                elif ventana.valor == "Eliminar autor":
                                    query_autores = """
                                    SELECT autor.id_autor, autor.nombre, autor.apellidos
                                    FROM libros_autores
                                    JOIN autor ON libros_autores.id_autor = autor.id_autor
                                    WHERE libros_autores.id_libro = %s
                                    """
                                    cursor.execute(query_autores, (id_libro,))
                                    autoresLista = cursor.fetchall()
                                    autoresLista.sort(key=lambda x: x[2])
                                    autores = []
                                    for autor in autoresLista:
                                        autores.append(f"{autor[0]} - {autor[2]}, {autor[1]}")
                                        
                                    if autores:
                                        Cambio = menuApp3(
                                            title = "Eliminar autor",
                                            tamañoVentana = (500, 600),
                                            opciones =["Autor"],
                                            texto = "Selecciona un autor para eliminar del libro",
                                            textoBoton="Eliminar",
                                            tipo = [[1,autores]]
                                        )
                                        Cambio.run()
                                        autor = Cambio.valores["valor_1"].text
                                        id_autor = int(autor.split(" ")[0])
                                        autor = autor.split(" - ")[1]
                                        query_delete_autor = "DELETE FROM libros_autores WHERE id_libro = %s AND id_autor = %s"
                                        ejecutar_Un_query(conexion,query_delete_autor, (id_libro, id_autor),
                                                            "Autor eliminado correctamente",
                                                            "Error al eliminar el autor")
                                    else:
                                        mensaje = menuApp4(
                                            tamañoVentana = (600, 200),
                                            texto = "No hay autores asociados a este libro",
                                            boton = "Volver")
                                        mensaje.run()
                                
                                elif ventana.valor == "Volver":
                                    break

                        elif ventana.valor == "Actualiza géneros asociados":
                            cursor = conexion.cursor()
                            # Actualizar géneros asociados
                            while True:
                                ventana = menuApp1(
                                    title = "Actualiza géneros asociados",
                                    tamañoVentana = (500, 270),
                                    opciones = [
                                        "Añadir género", "Eliminar género", "Volver"
                                    ],
                                    colores = [
                                        (0.4, 1, 0, 1), (0.4, 0, 1, 1), (0.4, 0.4, 0.4, 1)
                                    ]
                                ) 
                                ventana.run()
                                if ventana.valor == "Añadir género":
                                    Lista_Generos = Crea_lista(conexion, "genero", "id_genero, nombre",1 , 1)
                                    añadir = menuApp3(
                                        title = "Añadir género",
                                        tamañoVentana = (500, 600),
                                        opciones =[ "Género"],
                                        texto = "Selecciona un género para añadir al libro",
                                        textoBoton="Añadir",
                                        tipo = [[1,Lista_Generos]]
                                    )
                                    añadir.run()
                                    genero = añadir.valores["valor_1"].text
                                    id_genero = int(genero.split(" ")[0])
                                    genero = genero.split(" - ")[1]
                                    # Mira si hay en la tabla libros_géneros ya especificada la relación id_libro, id_genero
                                    query_verificar_genero = "SELECT id_libro, id_genero FROM libros_géneros WHERE id_libro = %s"
                                    cursor.execute(query_verificar_genero, (id_libro,))
                                    revision = cursor.fetchall()
                                    if id_genero in [x[1] for x in revision]:
                                            mensaje = menuApp4(
                                                tamañoVentana = (600, 200),
                                                texto = f"El género {genero} ya está asociado al libro",
                                                boton = "Volver")
                                            mensaje.run()
                                            break
                                    query_insert_genero = "INSERT INTO libros_géneros (id_libro, id_genero) VALUES (%s, %s)"
                                    ejecutar_Un_query(conexion,query_insert_genero, (id_libro, id_genero),
                                                        "Género añadido correctamente",
                                                        "Error al añadir el género")
                                elif ventana.valor == "Eliminar género":
                                    query_generos = """
                                    SELECT genero.id_genero, genero.nombre
                                    FROM libros_géneros
                                    JOIN genero ON libros_géneros.id_genero = genero.id_genero
                                    WHERE libros_géneros.id_libro = %s
                                    """
                                    cursor.execute(query_generos, (id_libro,))
                                    generosLista = cursor.fetchall()
                                    generosLista.sort(key=lambda x: x[1])
                                    generos = []
                                    for genero in generosLista:
                                        generos.append(f"{genero[0]} - {genero[1]}")
                                        
                                    if generos:
                                        Cambio = menuApp3(
                                            title = "Eliminar género",
                                            tamañoVentana = (500, 600),
                                            opciones =["Género"],
                                            texto = "Selecciona un género para eliminar del libro",
                                            textoBoton="Eliminar",
                                            tipo = [[1,generos]]
                                        )
                                        Cambio.run()
                                        genero = Cambio.valores["valor_1"].text
                                        id_genero = int(genero.split(" ")[0])
                                        genero = genero.split(" - ")[1]                                       
                                        query_delete_genero = "DELETE FROM libros_géneros WHERE id_libro = %s AND id_genero = %s"
                                        ejecutar_Un_query(conexion,query_delete_genero, (id_libro, id_genero),
                                                        "Género eliminado correctamente",
                                                        "Error al eliminar el género")
                                    else:
                                        mensaje = menuApp4(
                                            tamañoVentana = (600, 200),
                                            texto = "No hay géneros asociados a este libro",
                                            boton = "Volver")
                                        mensaje.run()
                                
                                elif ventana.valor == "Volver":
                                    break
            
                        elif ventana.valor == "Volver":
                            break

                elif ventana.valor == "Actualiza un autor":
                    cursor = conexion.cursor()
                    Lista_Autores = Crea_lista(conexion, "autor", "id_autor, nombre, apellidos")
                    Pregunta = menuApp3(
                        title = "Actualiza un autor",
                        tamañoVentana = (500, 600),
                        opciones = ["Autor:"],
                        texto = "Busca el autor a actualizar",
                        textoBoton="Seleccionar",
                        tipo = [[1, Lista_Autores]]
                    )
                    Pregunta.run()
                    autor = Pregunta.valores["valor_1"].text
                    actualizar_autor(conexion, autor)

                elif ventana.valor == "Actualiza un género":
                    Lista_Generos = Crea_lista(conexion, "genero", "id_genero, nombre",1 , 1)
                    Dato = menuApp3(
                        title = "Actualiza género",
                        tamañoVentana = (500, 600),
                        opciones =[ "Nombre"],
                        texto = "Busca el género a actualizar",	
                        textoBoton="Seleccionar",
                        tipo = [[1,Lista_Generos]]
                    )
                    Dato.run()
                    genero = Dato.valores["valor_1"].text
                    actualizar_genero(conexion, genero)

                elif ventana.valor == "Actualiza una editorial":
                    Lista_Editoriales = Crea_lista(conexion, "editorial", "id_editorial, nombre",1, 1)
                    Dato = menuApp3(
                        title = "Actualiza editorial",
                        tamañoVentana = (500, 600),
                        opciones =[ "Nombre"],
                        texto = "Busca la editorial a actualizar",
                        textoBoton="Seleccionar",
                        tipo = [[1,Lista_Editoriales]]
                    )
                    Dato.run()
                    editorial = Dato.valores["valor_1"].text
                    actualizar_editorial(conexion, editorial)
                    
                elif ventana.valor == "Elimina un libro":
                    Lista_Libros = []
                    cursor = conexion.cursor()
                    query = "SELECT id_libro, título FROM libros"
                    cursor.execute(query)
                    libros = cursor.fetchall()
                    # Ordena libros por título
                    libros.sort(key=lambda x: x[1])
                    for libro in libros:
                        Lista_Libros.append(f"{libro[0]} - {libro[1]}")
                    Seleccion = menuApp3(
                        title = "Selecciona un libro",
                        tamañoVentana = (500, 600),
                        opciones =[
                            "Libro"
                        ],
                        texto = "Selecciona un libro para eliminar",
                        textoBoton="Eliminar",
                        tipo = [[1,Lista_Libros]]
                    )
                    Seleccion.run()
                    libro = Seleccion.valores["valor_1"].text
                    id_libro = int(libro.split(" ")[0])
                    libroTexto = libro.split(" - ")[1]
                    eliminar_libro(conexion, id_libro,libroTexto)

                elif ventana.valor == "Elimina un autor":
                    cursor = conexion.cursor()
                    Lista_Autores = Crea_lista(conexion, "autor", "id_autor, nombre, apellidos")
                    Seleccion = menuApp3(
                        title = "Selecciona un autor",
                        tamañoVentana = (500, 600),
                        opciones =[
                            "Autor"
                        ],
                        texto = "Selecciona un autor para eliminar",
                        textoBoton="Eliminar",
                        tipo = [[1,Lista_Autores]]
                    )
                    Seleccion.run()
                    escogido = Seleccion.valores["valor_1"].text
                    id_autor = int(escogido.split(" ")[0])
                    nombre = escogido.split(" - ")[1]
                    eliminar_autor(conexion, id_autor,nombre)

                elif ventana.valor == "Elimina un género":
                    Lista_Generos = Crea_lista(conexion, "genero", "id_genero, nombre",1 , 1)
                    Dato = menuApp3(
                        title = "Elimina género",
                        tamañoVentana = (500, 600),
                        opciones =[ "Nombre"],
                        texto = "Selecciona el género a eliminar",
                        textoBoton="Eliminar",
                        tipo = [[1,Lista_Generos]]
                    )
                    Dato.run()
                    valor = Dato.valores["valor_1"].text
                    id_genero = int(valor.split(" ")[0])
                    nombre = valor.split(" - ")[1]
                    eliminar_genero(conexion, id_genero, nombre)
                    
                elif ventana.valor == "Elimina una editorial":
                    Lista_Editoriales = Crea_lista(conexion, "editorial", "id_editorial, nombre",1, 1)
                    Dato = menuApp3(
                        title = "Elimina editorial",
                        tamañoVentana = (500, 600),
                        opciones =[ "Nombre"],
                        texto = "Selecciona la editorial a eliminar",
                        textoBoton="Eliminar",
                        tipo = [[1,Lista_Editoriales]]
                    )
                    Dato.run()
                    valor = Dato.valores["valor_1"].text
                    id_editorial = int(valor.split(" ")[0])
                    nombre = valor.split(" - ")[1]
                    eliminar_editorial(conexion, id_editorial, nombre)

if __name__ == "__main__":
    main()


