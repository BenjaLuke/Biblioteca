from kivy.app import App                                    # Importar la clase que permite crear una aplicación
from kivy.uix.button import Button                          # Importar la clase que permite crear botones
from kivy.uix.label import Label                            # Importar la clase que permite crear etiquetas
from kivy.uix.boxlayout import BoxLayout                    # Importar la clase que permite crear layouts verticales u horizontales
from kivy.uix.scrollview import ScrollView                  # Importar la clase que permite crear layouts desplazables
from kivy.uix.gridlayout import GridLayout                  # Importar la clase que permite crear layouts en forma de parrilla
from kivy.core.window import Window                         # Importar la clase que permite acceder a las propiedades de la ventana
from kivy.uix.textinput import TextInput                    # Importar la clase que permite crear campos de texto editables
from kivy.uix.spinner import Spinner                        # Importar la clase que permite crear menús desplegables
from kivy.uix.checkbox import CheckBox                      # Importar la clase que permite crear casillas de verificación
from kivy.clock import Clock                                # Importar la clase que permite programar eventos diferidos
import platform                                             # Importar la librería que permite acceder a las propiedades del sistema

class menuApp1(App):                                        # Clase que crea un menú con botones

    def __init__(self, title,tamañoVentana,
                 opciones,colores,**kwargs):                # Constructor de la clase
        super(menuApp1, self).__init__(**kwargs)            # Inicialización de la clase padre
        self.title_menu = title                             # Título del menú
        self.tamañoVentana = tamañoVentana                  # Tamaño de la ventana
        self.opciones = opciones                            # Opciones del menú
        self.colores = colores                              # Colores de los botones
    
    def build(self):                                        # Método que crea la ventana
        Window.size = self.tamañoVentana                    # Tamaño de la ventana
        Window.title = 'Biblioteca'                         # Nombre de la ventana
        Window.clearcolor = (0.2, 0.4, 0.6, 1)              # Color de fondo de la ventana
        Window.top = 1                                      # Justifica la ventana en la parte superior
        self.valor = None                                   # Valor de retorno
        layout = BoxLayout(orientation='vertical',
                           padding = 20,
                           spacing = 10)                    # Layout principal
        self.botones = {}                                   # Diccionario para almacenar los botones
        titulo = Label(text=self.title_menu,            
                       size_hint=(1, None),
                       height=60,
                       font_size = 30,
                       color=(0.7, 0.48, 0.66, 1),
                       bold=True)                           # Crear un título para el menú
        layout.add_widget(titulo)                           # Agregar el título al layout
        for i, opcion in enumerate(self.opciones, start=1): # Crear un botón para cada opción
            button = Button(
                text=opcion,
                size_hint=(1, None),
                height=40, 
                background_color=self.colores[i-1],
                background_normal='',
                background_down='',
                color = (0,0,0,1),
                border = (0,0,30,30))                       # Crear un botón con el nombre de la opción
            self.botones[f"button_{i}"] = button            # Almacenar el botón con un nombre único
            button.bind(on_press=self.on_button_press)      # Vincular el evento de presionar el botón
            layout.add_widget(button)                       # Agregar el botón al layout
        return layout                                       # Retornar el layout

    def on_button_press(self, instance):                    # Método que se ejecuta al presionar un botón
        self.valor = instance.text                          # Obtener el nombre del botón presionado
        App.get_running_app().stop()                        # Detener la aplicación
        
    def on_stop(self):                                      # Método que se ejecuta al detener la aplicación
        return                                              # Retorno de la función

class menuApp2(App):                                        # Clase que crea una lista

    def __init__(self, title, tamañoVentana, lista, arquetipos="-", **kwargs):  # Constructor de la clase
        super(menuApp2, self).__init__(**kwargs)            # Inicialización de la clase padre
        self.title_menu = title                             # Título del menú
        self.tamañoVentana = tamañoVentana                  # Tamaño de la ventana
        self.lista = lista                                  # Lista de elementos
        self.Width = self.tamañoVentana[0] - 50             # Ancho de la ventana
        self.arquetipos = arquetipos                        # Arquetipos de la lista

        # Ajustes para macOS
        if platform.system() == "Darwin":
            Window.size = (1024, 768)                       # Tamaño más grande para macOS
            self.Width = self.tamañoVentana[0] - 100        # Ajusta el ancho en macOS
        else:
            Window.size = self.tamañoVentana                # Tamaño inicial de la ventana

    def build(self):                                        # Método que crea la ventana
        Window.title = 'Biblioteca'                         # Nombre de la ventana
        Window.clearcolor = (0.2, 0.4, 0.6, 1)              # Color de fondo de la ventana
        Window.top = 1                                      # Justifica la ventana en la parte superior

        layout = BoxLayout(orientation='vertical',          
                           padding=20, 
                           spacing=10)                     # Layout principal

        titulo = Label(
            text=self.title_menu,
            size_hint=(1, 0.1),                             # Usar tamaño relativo
            font_size='25sp',                               # Tamaño de fuente relativo a la pantalla
            color=(0.7, 0.48, 0.66, 1),
            bold=True
        )
        layout.add_widget(titulo)                           # Agregar el título al layout

        scroll_layout = ScrollView(size_hint=(1, 0.8))      # Crear un ScrollView para la lista
        grid = GridLayout(cols=1, size_hint_y=None,
                          spacing=0, 
                          padding=10)                      # Crear un GridLayout para la lista
        grid.bind(minimum_height=grid.setter('height'))     # Vincular la altura mínima del GridLayout

        for sublista in self.lista:                         # Crear una etiqueta para cada elemento de la lista
            fila = f"{sublista[0]} - {sublista[1]}"         # Aquí se combina el id con el Nombre
            if len(sublista) > 2:                           # Si hay más elementos en la sublista
                fila += (f" {self.arquetipos} " +
                         f" {self.arquetipos} ".join(
                             map(str, sublista[2:])))      # Agregar otros elementos de la sublista
            etiqueta = Label(
                text=f"[b]{fila}[/b]",
                markup=True,
                size_hint=(1, None),
                height=30,                                  # Aumentar la altura de la etiqueta
                text_size=(self.Width, None),               # Ajustar el ancho del texto al ancho de la ventana
                halign="left",
                valign="middle",
            )
            etiqueta.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
            grid.add_widget(etiqueta)                       # Agregar la etiqueta al GridLayout

        scroll_layout.add_widget(grid)                      # Agregar el GridLayout al ScrollView
        layout.add_widget(scroll_layout)                    # Agregar el ScrollView al layout

        cantidad = Label(
            text=f"Total de registros: {len(self.lista)}",
            size_hint=(1, 0.05),                            # Tamaño relativo
            text_size=(None, None),
            halign="center",
            valign="middle",
        )
        layout.add_widget(cantidad)                         # Agregar la etiqueta al layout

        boton_volver = Button(
            text="Volver al menú",
            size_hint=(1, 0.1),                             # Tamaño relativo
            background_color=(0.9, 0.4, 0.4, 1),
        )
        boton_volver.bind(on_press=self.on_button_press)    # Vincular el evento de presionar el botón
        layout.add_widget(boton_volver)                     # Agregar el botón al layout

        return layout                                       # Retornar el layout

    def on_button_press(self, instance):
        # Obtener el nombre del botón presionado
        self.valor = instance.text
        App.get_running_app().stop()
        
    def on_stop(self):
        return
    
class menuApp3(App):                                        # Clase que crea un menú con campos de texto editables y menús desplegables
    def __init__(self, title, tamañoVentana, 
                 opciones, texto, textoBoton,
                 tipo, **kwargs):                           # Constructor de la clase
        super(menuApp3, self).__init__(**kwargs)            # Inicialización de la clase padre
        self.title_menu = title                             # Título del menú
        self.tamañoVentana = tamañoVentana                  # Tamaño de la ventana
        self.opciones = opciones                            # Opciones del menú
        self.texto = texto                                  # Texto de aviso
        self.textoBoton = textoBoton                        # Texto del botón
        self.Width = self.tamañoVentana[0] - 50             # Ancho de la ventana
        self.valores = {}                                   # Diccionario para almacenar los valores de los campos
        self.tipo = tipo                                    # Tipo de campo (0: TextInput, 1: Spinner)
        
    def build(self):                                        # Método que crea la ventana
        Window.size = self.tamañoVentana                    # Tamaño de la ventana
        Window.title = 'Biblioteca'                         # Nombre de la ventana
        Window.clearcolor = (0.2, 0.4, 0.6, 1)              # Color de fondo de la ventana
        Window.top = 1                                      # Justifica la ventana en la parte superior
        layout = BoxLayout(orientation='vertical',
                           padding=20, 
                           spacing=10)                      # Layout principal
        titulo = Label(text=self.title_menu,    
                       size_hint=(1, None),
                       height=60,
                       font_size=30,
                       color=(0.7, 0.48, 0.66, 1),
                       bold=True)                           # Crear un título para el menú
        layout.add_widget(titulo)                           # Agregar el título al layout
        inputs = []                                         # Lista para almacenar los widgets
        primer_textinput = None                             # Primer widget de la lista
        for i, opcion in enumerate(self.opciones, start=1): # Crear un campo para cada opción
            etiqueta = Label(
                text=f"{opcion}:",
                markup=True,
                size_hint=(1, None),
                height=20,
                text_size=(None, None),
                halign="left",
                valign="middle",
            )                                               # Crear una etiqueta con el nombre de la opción
            if self.tipo[i - 1][0] == 0:                    # Si el tipo es TextInput
                intro = TextInput(
                    size_hint=(1, None),
                    height=40,
                    background_color=(0.9, 0.4, 0.4, 1),
                    multiline=False,
                )                                           # Crear un campo de texto editable
                layout.add_widget(etiqueta)                 # Agregar la etiqueta al layout
                layout.add_widget(intro)                    # Agregar el campo al layout
                if primer_textinput is None:                # Si es el primer campo
                    primer_textinput = intro                # Almacenar el campo
            elif self.tipo[i - 1][0] == 1:                  # Si el tipo es Spinner
                intro = Spinner(
                    text="Despliega y escoge",
                    values=self.tipo[i - 1][1],
                    size_hint=(1, None),
                    height=40,
                    background_color=(1, 0.6, 0.6, 1),
                )                                           # Crear un menú desplegable
                intro.original_values = self.tipo[i - 1][1] # Almacenar los valores originales
                layout.add_widget(etiqueta)                 # Agregar la etiqueta al layout
                layout.add_widget(intro)                    # Agregar el menú al layout
                text_input_overlay = TextInput(
                    size_hint=(1, None),
                    height=40,
                    multiline=False,
                    background_color=(1, 1, 1, 0.5), 
                    hint_text="Escribe para filtrar...",
                    foreground_color=(0, 0, 0, 1),
                )                                           # Crear un campo de texto editable
                text_input_overlay.bind(on_text_validate=
                                        lambda instance,
                                        spinner=intro: 
                                        self.update_spinner(
                                        instance, spinner)) # Vincular el evento de validación del texto
                layout.add_widget(text_input_overlay)       # Agregar el campo al layout
                if primer_textinput is None:                # Si es el primer campo
                    primer_textinput = text_input_overlay   # Almacenar el campo
            self.valores[f"valor_{i}"] = intro              # Almacenar el widget con un nombre único
            if self.tipo[i - 1][0] == 0:                    # Si el tipo es TextInput
                inputs.append(intro)                        # Almacenar el widget en una lista
            elif self.tipo[i - 1][0] == 1:                  # Si el tipo es Spinner
                inputs.append(text_input_overlay)           # Almacenar el widget en una lista
        for i in range(len(inputs) - 1):                    # Vincular los eventos de validación de los campos
            inputs[i].bind(on_text_validate=lambda instance,
                           next_input=inputs[i + 1]:
                               self.focus_next(
                                   instance, next_input))   # Vincular el evento de validación del texto
        if primer_textinput:                                # Si hay un primer campo
            primer_textinput.focus = True                   # Establecer el foco en el primer campo
        aviso = Label(
            text=self.texto,
            size_hint=(1, None),
            height=20,
            text_size=(None, None),
            halign="left",
            valign="middle",
        )                                                   # Crear una etiqueta con un aviso
        layout.add_widget(aviso)                            # Agregar el aviso al layout
        boton_volver = Button(
            text=self.textoBoton,
            size_hint=(1, None),
            height=50,
            background_color=(0.9, 0.4, 0.4, 1),
        )                                                   # Crear un botón para volver al menú principal
        boton_volver.bind(on_press=self.on_button_press)    # Vincular el evento de presionar el botón
        layout.add_widget(boton_volver)                     # Agregar el botón al layout
        return layout                                       # Retornar el layout
    
    def update_spinner(self, text_input, spinner):          # Método que actualiza el menú desplegable
        if not text_input.text:                             # Si el campo está vacío
            spinner.values = spinner.original_values        # Restaurar los valores originales
            spinner.text = "Despliega y escoge"             # Restaurar el texto del menú
            spinner.background_color = (1, 0.6, 0.6, 1)     # Restaurar el color de fondo
            return                                          # Retorno de la función
        filter_text = text_input.text.lower()               # Obtener el texto del campo
        filtered_values = [value for 
                           value in 
                           spinner.values if 
                           filter_text in 
                           value.lower()]                   # Filtrar los valores del menú
        if filtered_values:                                 # Si hay valores filtrados
            spinner.values = filtered_values                # Actualizar los valores del menú
            spinner.text = filtered_values[0]               # Establecer el primer valor
            spinner.background_color = (1, 0.6, 0.6, 1)     # Establecer el color de fondo
        else:                                               # Si no hay valores filtrados
            spinner.values = [text_input.text]              # Deja un sólo valor
            spinner.text = text_input.text                  # Establecer el valor del campo
            spinner.background_color = (0, 0, 1, 1)         # Establecer el color de fondo
    def focus_next(self, current_input, next_input):        # Método que establece el foco en el siguiente campo
        next_input.focus = True                             # Establecer el foco en el siguiente campo
    def on_button_press(self, instance):                    # Método que se ejecuta al presionar un botón
        self.valor = instance.text                          # Obtener el nombre del botón presionado
        App.get_running_app().stop()                        # Detener la aplicación
    def on_stop(self):                                      # Método que se ejecuta al detener la aplicación
        return                                              # Retorno de la función

class menuApp4(App):                                        # Clase que crea un menú con un aviso y un botón de retorno

    def __init__(self, tamañoVentana, 
                 texto,boton,**kwargs):                     # Constructor de la clase
        super(menuApp4, self).__init__(**kwargs)            # Inicialización de la clase padre
        self.tamañoVentana = tamañoVentana                  # Tamaño de la ventana
        self.texto = texto                                  # Texto de aviso
        self.boton = boton                                  # Texto del botón
        
    def build(self):                                        # Método que crea la ventana
        Window.size = self.tamañoVentana                    # Tamaño de la ventana
        Window.title = 'Biblioteca'                         # Nombre de la ventana
        Window.clearcolor = (0.2, 0.4, 0.6, 1)              # Color de fondo de la ventana
        Window.top = 1                                      # Justifica la ventana en la parte superior
        layout = BoxLayout(orientation='vertical', 
                           padding = 20, 
                           spacing = 10)                    # Layout principal
        titulo = Label(text=self.texto,
                       size_hint=(1, None),
                       height=60,
                       font_size = 30,
                       color=(0.7, 0.48, 0.66, 1),
                       bold=True)                           # Crear un título para el menú
        layout.add_widget(titulo)                           # Agregar el título al layout
        boton = Button(
            text=self.boton,
            size_hint=(1, None),
            height=50,
            background_color=(0.9, 0.4, 0.4, 1),
        )                                                   # Crear un botón para volver al menú principal
        boton.bind(on_press=self.on_button_press)           # Vincular el evento de presionar el botón
        layout.add_widget(boton)                            # Agregar el botón al layout
        return layout                                       # Retornar el layout
    
    def on_button_press(self,instance):                     # Método que se ejecuta al presionar un botón
        self.valor = instance.text                          # Obtener el nombre del botón presionado
        App.get_running_app().stop()                        # Detener la aplicación
        
    def on_stop(self):                                      # Método que se ejecuta al detener la aplicación
        return                                              # Retorno de la función
    
class menuApp5(App):                                        # Clase que crea una lista con casillas de verificación
    
    def __init__(self, título, tamañoVentana,
                 texto, textoBoton, 
                 ListaDeOpciones, **kwargs):                # Constructor de la clase
        super(menuApp5, self).__init__(**kwargs)            # Inicialización de la clase padre
        self.título = título                                # Título de la lista
        self.tamañoVentana = tamañoVentana                  # Tamaño de la ventana
        self.texto = texto                                  # Texto de aviso
        self.boton = textoBoton                             # Texto del botón
        self.ListaDeOpciones = ListaDeOpciones              # Lista de opciones
        self.selected_options = []                          # Lista de opciones seleccionadas

    def build(self):                                        # Método que crea la ventana
        Window.size = self.tamañoVentana                    # Tamaño de la ventana
        Window.title = 'Biblioteca'                         # Nombre de la ventana
        Window.clearcolor = (0.2, 0.4, 0.6, 1)              # Color de fondo de la ventana
        Window.top = 1                                      # Justifica la ventana en la parte superior
        layout = BoxLayout(orientation='vertical', 
                           padding=20, 
                           spacing=10)                      # Layout principal
        self.cabecera = Label(
            text=str(self.título),
            size_hint=(1, None),
            height=60,
            font_size=30,
            color=(0.7, 0.48, 0.66, 1),
            bold=True)                                      # Crear un título para la lista
        layout.add_widget(self.cabecera)                    # Agregar el título al layout
        self.search_input = TextInput(
            hint_text="Busca una opción...",
            size_hint=(1, None),
            height=40,
            multiline=False,
            background_color=(1, 1, 1, 1),
        )                                                   # Crear un campo de texto editable
        self.search_input.bind(text=self.on_search_text)    # Vincular el evento de cambio de texto
        layout.add_widget(self.search_input)                # Agregar el campo al layout
        self.search_input.focus = True                      # Establecer el foco en el campo
        scroll_view = ScrollView(
            size_hint=(1, None), 
            height=self.tamañoVentana[1] - 200
            )                                               # Crear un ScrollView para la lista
        self.scroll_layout = BoxLayout(
            orientation='vertical', size_hint_y=None,
            spacing=10, padding=10
            )                                               # Crear un BoxLayout para la lista
        self.scroll_layout.bind(
            minimum_height = 
            self.scroll_layout.setter('height')
            )                                               # Vincular la altura mínima del BoxLayout
        self.checkboxes = []                                # Lista para almacenar las casillas de verificación
        for opcion in self.ListaDeOpciones:
            row = BoxLayout(orientation='horizontal', 
                            size_hint_y=None, 
                            height=40)                      # Crear un BoxLayout para cada opción
            label = Label(
                text=opcion,
                size_hint_x=0.8,
                halign="left",
                valign="middle",
                text_size=(None, None),
            )                                               # Crear una etiqueta con el nombre de la opción
            label.bind(size=lambda instance, 
                       value: setattr(instance,
                                      "text_size",
                                      value))               # Vincular el tamaño de la etiqueta
            checkbox = CheckBox(size_hint_x=0.2)            # Crear una casilla de verificación
            checkbox.bind(active=self.on_checkbox_active)   # Vincular el evento de cambio de estado
            row.add_widget(checkbox)                        # Agregar la casilla al BoxLayout
            row.add_widget(label)                           # Agregar la etiqueta al BoxLayout
            self.scroll_layout.add_widget(row)              # Agregar el BoxLayout al ScrollView
            self.checkboxes.append((opcion, checkbox))      # Almacenar la opción y la casilla
        scroll_view.add_widget(self.scroll_layout)          # Agregar el BoxLayout al ScrollView
        layout.add_widget(scroll_view)                      # Agregar el ScrollView al layout
        boton = Button(
            text=self.boton,
            size_hint=(1, None),
            height=50,
            background_color=(0.9, 0.4, 0.4, 1),
        )                                                   # Crear un botón para volver al menú principal
        boton.bind(on_press=self.on_button_press)           # Vincular el evento de presionar el botón
        layout.add_widget(boton)                            # Agregar el botón al layout
        return layout                                       # Retornar el layout
    
    def on_search_text(self, instance, value):              # Método que se ejecuta al cambiar el texto del campo
        validacion = False
        for opcion, widget in self.checkboxes:              # Recorrer las casillas de verificación
            if value.lower() in opcion.lower():             # Si el texto coincide con la opción
                self.scroll_layout.parent.scroll_to(widget) # Desplazar la lista hasta la opción
                # la textinput se pone de color original
                self.search_input.background_color = (1, 1, 1, 1)
                validacion = True
                break                                       # Salir del bucle
        if not validacion:                                  # Si no se encuentra la opción
            # la textinput se pone de color rojo
            self.search_input.background_color = (1, 0, 0, 1)
                
    def on_checkbox_active(self, checkbox, value):          # Método que se ejecuta al cambiar el estado de la casilla
        for opcion, cb in self.checkboxes:                  # Recorrer las casillas de verificación
            if cb == checkbox:                              # Si la casilla coincide
                if (value and 
                    opcion not in self.selected_options):   # Si está activada y no está seleccionada
                    self.selected_options.append(opcion)    # Agregar la opción a la lista
                    self.search_input.text = ""             # Limpiar el TextInput
                    Clock.schedule_once(
                        lambda dt: setattr(
                            self.search_input, "focus", True
                            ), 0
                        )                                   # Establecer el foco en el TextInput
                elif (not value and
                      opcion in self.selected_options):     # Si está desactivada y está seleccionada
                    self.selected_options.remove(opcion)    # Eliminar la opción de la lista

    def on_button_press(self, instance):                    # Método que se ejecuta al presionar un botón
        self.valor = instance.text                          # Obtener el nombre del botón presionado
        App.get_running_app().stop()                        # Detener la aplicación

    def on_stop(self):                                      # Método que se ejecuta al detener la aplicación
        return                                              # Retorno de la función