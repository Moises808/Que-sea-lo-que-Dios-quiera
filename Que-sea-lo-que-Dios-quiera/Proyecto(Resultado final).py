import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import os
import sys
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from PIL import Image

# ============================
# === CONFIGURACIÓN GLOBAL ===
# ============================
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# Mapeo de columnas de Álbumes a los Requisitos del Proyecto:
# Nombre = Album
# Categoría = Genero
# Precio = Ventas_numeric (millones)
# Stock = NumCanciones (simulado como stock)
# Proveedor = Artista (simulado como proveedor)
# Demanda = (Calculado en base a Ventas_numeric)
# + 5 Adicionales: Pais, Anio, Ventas (texto original), Codigo (id), Demanda

# Opciones de color para gráficos (Requisito 8: Personalización de colores)
COLOR_OPCIONES = {
    "Opción 1 (Azul/Naranja)": ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
    "Opción 2 (Verde/Rojo)": ['#2ca02c', '#d62728', '#9467bd', '#8c564b']
}
color_seleccionado = COLOR_OPCIONES["Opción 1 (Azul/Naranja)"]

# ============================
# === UTILIDADES ============
# ============================

def es_entero_valido(valor):
    try:
        return int(valor) >= 0
    except Exception:
        return False

# ============================
# === GESTIÓN DE USUARIOS ===
# ============================
archivo_usuarios = "usuarios.csv"

def cargar_usuarios():
    if os.path.exists(archivo_usuarios):
        usuarios_df = pd.read_csv(archivo_usuarios)
    else:
        usuarios_df = pd.DataFrame(columns=["usuario", "password"])
        usuarios_df.to_csv(archivo_usuarios, index=False)
    return usuarios_df

usuarios = cargar_usuarios()

def guardar_usuarios():
    usuarios.to_csv(archivo_usuarios, index=False)

# ============================
# === BASE DE DATOS DE ÁLBUMES ===
# ============================
conexion = sqlite3.connect("albums.db")
cursor = conexion.cursor()

def inicializar_db_y_cargar_df():
    """Crea la tabla si no existe y carga/actualiza el DataFrame global."""
    global albums_df
    
    # 1. Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Artista TEXT,
        Pais TEXT,
        Album TEXT,
        Anio INTEGER,
        Ventas TEXT,
        Genero TEXT,
        NumCanciones INTEGER)
    """)
    conexion.commit()

    # 2. Verificar si hay datos, si no, inserta los datos de ejemplo
    cursor.execute("SELECT COUNT(*) FROM Albums")
    if cursor.fetchone()[0] == 0:
        datos = [
            ("Michael Jackson", "Estados Unidos", "Thriller", 1982, "70 millones", "Pop", 9),
            ("AC/DC", "Australia", "Back In Black", 1980, "50 millones", "Rock", 10),
            ("Meat Loaf", "Estados Unidos", "Bat Out Of Hell", 1977, "50 millones", "Rock", 7),
            ("Pink Floyd", "Reino Unido", "The Dark Side Of The Moon", 1973, "45 millones", "Rock", 10),
            ("Whitney Houston / Varios artistas", "Estados Unidos", "The Bodyguard", 1992, "45 millones", "Varios Géneros", 12),
            ("Eagles", "Estados Unidos", "Their Greatest Hits (1971–1975)", 1976, "42 millones", "Rock", 10),
            ("Fleetwood Mac", "Reino Unido", "Rumours", 1977, "40 millones", "Pop", 11),
            ("Bee Gees / Varios artistas", "Reino Unido / Australia", "Saturday Night Fever", 1977, "40 millones", "Varios Géneros", 21),
            ("Andrew Lloyd Webber", "Reino Unido", "El Fantasma De La Ópera", 1986, "40 millones", "Opera", 14),
            ("Shania Twain", "Canadá", "Come On Over", 1997, "40 millones", "Pop", 16),
            ("John Travolta y Olivia Newton-John", "Estados Unidos y Reino Unido", "Grease", 1978, "38 millones", "Pop", 24),
            ("Led Zeppelin", "Reino Unido", "Led Zeppelin IV", 1971, "37 millones", "Rock", 8),
            ("Michael Jackson", "Estados Unidos", "Bad", 1987, "35 millones", "Pop", 11),
            ("Pink Floyd", "Reino Unido", "The Wall", 1979, "33 millones", "Rock", 26),
            ("Alanis Morissette", "Canadá", "Jagged Little Pill", 1995, "33 millones", "Pop", 13),
            ("The Beatles", "Reino Unido", "Sgt. Pepper's Lonely Hearts Club Band", 1967, "32 millones", "Rock", 13),
            ("Eagles", "Estados Unidos", "Hotel California", 1976, "32 millones", "Rock", 9),
            ("Varios Artistas", "Estados Unidos", "Dirty Dancing", 1987, "32 millones", "Varios Géneros", 12),
            ("Michael Jackson", "Estados Unidos", "Dangerous", 1991, "32 millones", "Pop", 14),
            ("Mariah Carey", "Estados Unidos", "Music Box", 1993, "32 millones", "Pop", 11),
            ("Céline Dion", "Canadá", "Falling Into You", 1996, "32 millones", "Pop", 16),
            ("Adele", "Reino Unido", "21", 2011, "31 millones", "Pop", 11),
            ("Elton John", "Reino Unido", "Goodbye Yellow Brick Road", 1973, "31 millones", "Rock", 17),
            ("Céline Dion", "Canadá", "Let's Talk About Love", 1997, "31 millones", "Pop", 16),
            ("The Beatles", "Reino Unido", "1", 2000, "31 millones", "Rock", 27),
            ("The Beatles", "Reino Unido", "Abbey Road", 1969, "30 millones", "Rock", 17),
            ("Bee Gees", "Reino Unido", "Spirits Having Flown", 1979, "30 millones", "Pop", 10),
            ("Bruce Springsteen", "Estados Unidos", "Born In The U.S.A.", 1984, "30 millones", "Rock", 12),
            ("Dire Straits", "Reino Unido", "Brothers In Arms", 1985, "30 millones", "Rock", 9),
            ("Guns N' Roses", "Estados Unidos", "Appetite For Destruction", 1987, "30 millones", "Rock", 12),
            ("Madonna", "Estados Unidos", "The Immaculate Collection", 1990, "30 millones", "Pop", 17),
            ("Metallica", "Estados Unidos", "Metallica", 1991, "30 millones", "Metal", 12),
            ("Nirvana", "Estados Unidos", "Nevermind", 1991, "30 millones", "Rock", 13),
            ("Backstreet Boys", "Estados Unidos", "Backstreet Boys / Backstreet Boys", 1996, "30 millones", "Pop", 13),
            ("James Horner", "Estados Unidos", "Titanic", 1997, "30 millones", "Instrumental", 57),
            ("Britney Spears", "Estados Unidos", "...Baby One More Time", 1999, "30 millones", "Pop", 16),
            ("Linkin Park", "Estados Unidos", "Hybrid Theory", 2000, "30 millones", "Rock", 12),
            ("Santana", "Estados Unidos y México", "Supernatural", 1999, "30 millones", "Pop", 14),
            ("Backstreet Boys", "Estados Unidos", "Millennium", 1999, "30 millones", "Pop", 12),
            ("Bon Jovi", "Estados Unidos", "Slippery When Wet", 1986, "28 millones", "Rock", 10),
            ("ABBA", "Suecia", "ABBA Gold: Greatest Hits", 1992, "28 millones", "Pop", 19),
            ("Spice Girls", "Reino Unido", "Spice", 1996, "28 millones", "Pop", 10),
            ("Backstreet Boys", "Estados Unidos", "Backstreet's Back", 1997, "28 millones", "Pop", 11),
            ("Norah Jones", "Estados Unidos", "Come Away With Me", 2002, "26 millones", "Pop", 44),
            ("Eric Clapton", "Reino Unido", "Unplugged", 1992, "26 millones", "Rock", 20),
            ("Iron Butterfly", "Estados Unidos", "In-A-Gadda-Da-Vida", 1968, "25 millones", "Rock", 6),
            ("Simon & Garfunkel", "Estados Unidos", "Bridge Over Troubled Water", 1970, "25 millones", "Country", 11),
            ("Carole King", "Estados Unidos", "Tapestry", 1971, "25 millones", "Rock", 12),
            ("Queen", "Reino Unido", "Greatest Hits", 1981, "25 millones", "Rock", 17),
            ("Bob Marley & The Wailers", "Jamaica", "Legend", 1984, "25 millones", "Pop", 29),
            ("Madonna", "Estados Unidos", "Like A Virgin", 1984, "25 millones", "Pop", 11),
            ("Whitney Houston", "Estados Unidos", "Whitney Houston", 1985, "25 millones", "Pop", 10),
            ("Madonna", "Estados Unidos", "True Blue", 1986, "25 millones", "Pop", 11),
            ("U2", "Irlanda", "The Joshua Tree", 1987, "25 millones", "Rock", 11),
            ("Whitney Houston", "Estados Unidos", "Whitney", 1987, "25 millones", "Pop", 11),
            ("Mariah Carey", "Estados Unidos", "Daydream", 1995, "25 millones", "Pop", 12),
            ("Backstreet Boys", "Estados Unidos", "Black & Blue", 2000, "24 millones", "Pop", 13),
            ("Ace Of Base", "Suecia", "Happy Nation", 1993, "23 millones", "Pop", 14),
            ("Green Day", "Estados Unidos", "American Idiot", 2004, "23 millones", "Rock", 9),
            ("TLC", "Estados Unidos", "CrazySexyCool", 1994, "23 millones", "Pop", 16),
            ("Oasis", "Reino Unido", "(What's The Story) Morning Glory?", 1995, "22 millones", "Rock", 40),
            ("Ricky Martin", "Puerto Rico", "Ricky Martin", 1999, "22 millones", "Pop", 14),
            ("Adele", "Reino Unido", "25", 2015, "22 millones", "Pop", 11),
            ("Bon Jovi", "Estados Unidos", "Cross Road", 1994, "21 millones", "Rock", 14),
            ("Dido", "Reino Unido", "No Angel", 1999, "21 millones", "Pop", 14),
            ("Eminem", "Estados Unidos", "The Marshall Mathers LP", 2000, "21 millones", "Hip-Hop", 18),
            ("Boston", "Estados Unidos", "Boston", 1976, "20 millones", "Rock", 8),
            ("Blondie", "Estados Unidos", "Parallel Lines", 1978, "20 millones", "Rock", 12),
            ("Supertramp", "Reino Unido", "Breakfast In America", 1979, "20 millones", "Rock", 22),
            ("Michael Jackson", "Estados Unidos", "Off The Wall", 1979, "20 millones", "Pop", 10),
            ("Barbra Streisand", "Estados Unidos", "Guilty", 1980, "20 millones", "Pop", 9),
            ("Lionel Richie", "Estados Unidos", "Can't Slow Down", 1983, "20 millones", "Pop", 8),
            ("Tina Turner", "Estados Unidos", "Private Dancer", 1984, "20 millones", "Pop", 18),
            ("Prince & The Revolution", "Estados Unidos", "Purple Rain", 1984, "20 millones", "Funk", 9),
            ("Phil Collins", "Reino Unido", "No Jacket Required", 1985, "20 millones", "Rock", 11),
            ("Def Leppard", "Reino Unido", "Hysteria", 1987, "20 millones", "Rock", 12),
            ("George Michael", "Reino Unido", "Faith", 1987, "20 millones", "Pop", 10),
            ("Billy Ray Cyrus", "Estados Unidos", "Some Gave All", 1992, "20 millones", "Rock", 10),
            ("Janet Jackson", "Estados Unidos", "Janet", 1993, "20 millones", "Pop", 28),
            ("Céline Dion", "Canadá", "The Colour Of My Love", 1993, "20 millones", "Pop", 15),
            ("Green Day", "Estados Unidos", "Dookie", 1994, "20 millones", "Rock", 15),
            ("Shania Twain", "Canadá", "The Woman In Me", 1995, "20 millones", "Pop", 12),
            ("Michael Jackson", "Estados Unidos", "HIStory: Past, Present and Future, Book I", 1995, "20 millones", "Pop", 30),
            ("Queen", "Reino Unido", "Made In Heaven", 1995, "20 millones", "Rock", 13),
            ("Andrea Bocelli", "Italia", "Romanza", 1997, "20 millones", "Opera", 15),
            ("Spice Girls", "Reino Unido", "Spiceworld", 1997, "20 millones", "Pop", 10),
            ("Madonna", "Estados Unidos", "Ray Of Light", 1998, "20 millones", "Pop", 13),
            ("Cher", "Estados Unidos", "Believe", 1998, "20 millones", "Pop", 10),
            ("Britney Spears", "Estados Unidos", "Oops!... I Did It Again", 2000, "20 millones", "Pop", 12),
            ("Usher", "Estados Unidos", "Confessions", 2004, "20 millones", "Pop", 21),
            ("SSS", "Colombia", "Goodbye Red Brick Building", 2024, "38 millones", "Rock", 17),
            ("SSS", "Colombia", "(Not) A Single Man", 2025, "30 millones", "Rock", 16),
            ("SSS", "Colombia", "Riding In The Street", 2023, "37 millones", "Rock", 12),
            ("SSS", "Colombia", "So Sad The Life", 2025, "40 millones", "Rock", 9)
        ]
        cursor.executemany("""
        INSERT INTO Albums (Artista, Pais, Album, Anio, Ventas, Genero, NumCanciones)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, datos)
        conexion.commit()

    # 3. Leer la BD a DataFrame
    albums_df = pd.read_sql_query("SELECT * FROM Albums", conexion)

    # 4. Normalizar la columna Ventas -> Ventas_numeric (float, millones)
    albums_df['Ventas_numeric'] = (
        albums_df['Ventas']
        .astype(str)
        .str.replace(' millones', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '', regex=False)
        .str.strip()
    )
    albums_df['Ventas_numeric'] = pd.to_numeric(albums_df['Ventas_numeric'], errors='coerce').astype(float)

    # 5. Columna de Demanda (simulada)
    ventas_media = albums_df['Ventas_numeric'].mean()
    albums_df['Demanda'] = 'Bajo'
    albums_df.loc[albums_df['Ventas_numeric'] > ventas_media * 1.5, 'Demanda'] = 'Alto'
    albums_df.loc[(albums_df['Ventas_numeric'] > ventas_media) & (albums_df['Ventas_numeric'] <= ventas_media * 1.5), 'Demanda'] = 'Medio'
    
    # 6. Renombrar ID a Codigo (Requisito 1.g: Columna adicional Codigo)
    albums_df.rename(columns={'id': 'Codigo'}, inplace=True)

    return albums_df

albums_df = inicializar_db_y_cargar_df()

# ============================
# === CLASE PRINCIPAL DE LA APLICACIÓN ===
# ============================

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Álbumes (Proyecto UAM)")
        self.geometry("900x650")
        self.minsize(700, 550) 
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Cargar imagen (si existe)
        self.logo_img = self.cargar_imagen("Guitarra.jpg", size=(550, 350))
        
        # Inicializar y posicionar todas las páginas
        self.paginas = {}
        for F in (PaginaLogin, PaginaRegistro, PaginaMenuPrincipal, PaginaAgregar, PaginaConsultar, PaginaFiltros, PaginaEstadisticas):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.paginas[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_pagina("PaginaLogin")
    
    def cargar_imagen(self, nombre, size):
        # Evitar usar __file__ porque no siempre está definido (ej. entornos especiales)
        BASE = os.path.dirname(os.path.abspath(sys.argv[0])) if getattr(sys, 'argv', None) else os.getcwd()
        ruta_imagen = os.path.join(BASE, nombre)
        try:
            imagen_original = Image.open(ruta_imagen)
            return customtkinter.CTkImage(imagen_original, size=size)
        except Exception:
            return None

    def mostrar_pagina(self, page_name):
        frame = self.paginas[page_name]
        frame.tkraise()

    def get_color_opciones(self):
        return COLOR_OPCIONES

    def set_color_seleccionado(self, key):
        global color_seleccionado
        color_seleccionado = COLOR_OPCIONES[key]
        messagebox.showinfo("Color Actualizado", f"Esquema de color cambiado a: {key}")

    def get_color_seleccionado(self):
        return color_seleccionado
    
    def actualizar_dataframe(self):
        """Función para recargar el DF desde la BD después de una modificación."""
        global albums_df
        albums_df = inicializar_db_y_cargar_df()
        
        # Recargar datos en las páginas que lo necesiten
        self.paginas["PaginaFiltros"].actualizar_comboboxes()

# ============================
# === LOGIN Y REGISTRO ======
# ============================

class PaginaLogin(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Frame centralizado
        frame1 = customtkinter.CTkFrame(master=self)
        frame1.pack(pady=60, padx=60, fill="both", expand=True)

        customtkinter.CTkLabel(master=frame1, text="Iniciar Sesión", text_color="cyan",font=("Arial", 60)).pack(pady=30)

        customtkinter.CTkLabel(master=frame1, text="Usuario:", font=("Arial", 30)).pack(pady=(30, 0))
        self.login_usuario = customtkinter.CTkEntry(master=frame1, placeholder_text="usuario")
        self.login_usuario.pack(pady=(10, 10))

        customtkinter.CTkLabel(master=frame1, text="Contraseña:", font=("Arial", 30)).pack(pady=(30, 0))
        self.login_password = customtkinter.CTkEntry(master=frame1, show="*", placeholder_text="contraseña")
        self.login_password.pack(pady=(10, 10))

        customtkinter.CTkButton(master=frame1, text="Entrar", width=200, command=self.iniciar_sesion).pack(pady=10)
        customtkinter.CTkButton(master=frame1, text="Crear Cuenta", width=200, command=lambda: controller.mostrar_pagina("PaginaRegistro")).pack()

    def iniciar_sesion(self):
        global usuarios
        usuario = self.login_usuario.get().strip()
        password = self.login_password.get().strip()
        
        if usuario == "" or password == "":
            messagebox.showerror("Error", "Completa todos los campos.")
            return

        # Comprobar existencia y credenciales
        if usuario in usuarios["usuario"].astype(str).tolist():
            pass_series = usuarios.loc[usuarios["usuario"] == usuario, "password"]
            if len(pass_series) > 0:
                pass_correcta = str(pass_series.values[0])
                if password == pass_correcta:
                    self.controller.paginas["PaginaMenuPrincipal"].configurar_bienvenida(usuario)
                    self.controller.mostrar_pagina("PaginaMenuPrincipal")
                    self.login_usuario.delete(0, tk.END)
                    self.login_password.delete(0, tk.END)
                    return
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

class PaginaRegistro(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        customtkinter.CTkLabel(self, text="Crear Cuenta", font=("Arial", 60)).pack(pady=30)
        
        frame_registro = customtkinter.CTkFrame(self)
        frame_registro.pack(pady=30, padx=20, fill = "both", expand = True)

        customtkinter.CTkLabel(frame_registro, text="Nuevo usuario:", font=("Arial", 30)).pack(pady=(30, 0))
        self.reg_usuario = customtkinter.CTkEntry(frame_registro, placeholder_text="nuevo usuario", width=200)
        self.reg_usuario.pack(pady=(10, 40))
        
        customtkinter.CTkLabel(frame_registro, text="Contraseña:", font=("Arial", 30)).pack(pady=(10, 0))
        self.reg_password = customtkinter.CTkEntry(frame_registro, show="*", placeholder_text="contraseña", width=200)
        self.reg_password.pack(pady=(10, 40))

        customtkinter.CTkButton(frame_registro, text="Registrar", width=200, command=self.registrar_usuario).pack(pady=10)
        customtkinter.CTkButton(frame_registro, text="Volver al Login", width=200, command=lambda: controller.mostrar_pagina("PaginaLogin")).pack()

    def registrar_usuario(self):
        global usuarios

        usuario = self.reg_usuario.get().strip()
        password = self.reg_password.get().strip()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Llena todos los campos.")
            return
            
        if usuario in usuarios["usuario"].astype(str).tolist():
            messagebox.showerror("Error", "Ese usuario ya existe.")
            return

        # Añadir y guardar
        nuevo_registro = pd.DataFrame([{"usuario": usuario, "password": password}])
        usuarios = pd.concat([usuarios, nuevo_registro], ignore_index=True)
        guardar_usuarios()
        messagebox.showinfo("Éxito", "Cuenta creada correctamente.")
        
        # limpiar y volver al login
        self.reg_usuario.delete(0, tk.END)
        self.reg_password.delete(0, tk.END)
        self.controller.mostrar_pagina("PaginaLogin")

# ============================
# === 4. MENÚ PRINCIPAL ======
# ============================

class PaginaMenuPrincipal(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # Título y Bienvenida
        self.label_bienvenida = customtkinter.CTkLabel(self, text="Bienvenido(a)", font=("Arial", 26, "bold"))
        self.label_bienvenida.grid(row=0, column=0, pady=(50, 10), sticky="s")
        
        # Imagen Alusiva
        if controller.logo_img:
            logo_label = customtkinter.CTkLabel(self, text="", image=controller.logo_img)
            logo_label.grid(row=1, column=0, pady=5, sticky="n")
        
        # Contenedor para botones
        button_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, sticky="n", pady=10)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        # Botones de Navegación (Funcionalidades principales)
        customtkinter.CTkButton(button_frame, text="1. Agregar Álbum", width=250, height=50, command=lambda: controller.mostrar_pagina("PaginaAgregar")).grid(row=0, column=0, padx=20, pady=10)
        customtkinter.CTkButton(button_frame, text="2. Consultar/Modificar Álbum", width=250, height=50, command=lambda: controller.mostrar_pagina("PaginaConsultar")).grid(row=0, column=1, padx=20, pady=10)
        customtkinter.CTkButton(button_frame, text="3. Aplicar Filtros (Gráficos Dinámicos)", width=250, height=50, command=lambda: controller.mostrar_pagina("PaginaFiltros")).grid(row=1, column=0, padx=20, pady=10)
        customtkinter.CTkButton(button_frame, text="4. Visualizar Estadísticas (Gráficos Fijos)", width=250, height=50, command=lambda: controller.mostrar_pagina("PaginaEstadisticas")).grid(row=1, column=1, padx=20, pady=10)
        
        # Botón para cerrar sesión
        customtkinter.CTkButton(self, text="Cerrar Sesión", width=150, fg_color="red", hover_color="darkred", command=lambda: controller.mostrar_pagina("PaginaLogin")).grid(row=3, column=0, pady=(10, 20), sticky="n")

    def configurar_bienvenida(self, usuario):
        self.label_bienvenida.configure(text=f"Bienvenido(a) {usuario}")

# ============================
# === 5. ADICIÓN DE UN ÁLBUM ==
# ============================

class PaginaAgregar(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        customtkinter.CTkLabel(self, text="Agregar Nuevo Álbum",text_color="cyan", font=("Arial", 60, "bold")).pack(pady=20)

        input_frame = customtkinter.CTkScrollableFrame(self, label_text="Datos del Álbum",label_text_color="crimson", width=500, label_font=("Arial", 25, "bold"))
        input_frame.pack(padx=20, pady=10, fill="y", expand=True)

        self.campos = {}

        campos_layout = [
            ("Artista (Proveedor)", "Artista", "entry"),
            ("País", "Pais", "entry"), # Columna Adicional 1
            ("Nombre del Álbum", "Album", "entry"),
            ("Año", "Anio", "entry"),
            ("Ventas", "Ventas", "entry"), # Columna Adicional 3
            ("Género (Categoría)", "Genero", "combobox", albums_df['Genero'].unique().tolist()),
            ("No. Canciones (Stock)", "NumCanciones", "entry"),
        ]

        for i, (label_text, key, tipo, *opciones) in enumerate(campos_layout):
            row = i
            customtkinter.CTkLabel(input_frame, text=f"{label_text}:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            if tipo == "entry":
                self.campos[key] = customtkinter.CTkEntry(input_frame, width=250)
                self.campos[key].grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            elif tipo == "combobox":
                self.campos[key] = customtkinter.CTkComboBox(input_frame, values=opciones[0], width=250)
                self.campos[key].grid(row=row, column=1, padx=10, pady=5, sticky="ew")

        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        customtkinter.CTkButton(btn_frame, text="Guardar Álbum", width=200, command=self.guardar_album).pack(side="left", padx=10)
        customtkinter.CTkButton(btn_frame, text="Volver al Menú", width=200, command=lambda: controller.mostrar_pagina("PaginaMenuPrincipal")).pack(side="left", padx=10)

    def guardar_album(self):
        """Valida y guarda el nuevo álbum en la BD y recarga el DataFrame."""
        datos = {key: entry.get().strip() for key, entry in self.campos.items()}

        # 1. Validación de campos requeridos
        if not all(datos.get(key) for key in ["Artista", "Album", "Ventas", "Genero", "NumCanciones"]):
            messagebox.showerror("Error", "Completa los campos Artista, Álbum, Ventas, Género y No. Canciones.")
            return
        
        # 2. Validación de campos numéricos (simulación de Stock y Adicional)
        if not (es_entero_valido(datos.get("NumCanciones")) and es_entero_valido(datos.get("Anio"))):
            messagebox.showerror("Error", "No. Canciones y Año deben ser números enteros positivos válidos.")
            return

        # 3. Insertar en la base de datos
        try:
            cursor.execute("""
            INSERT INTO Albums (Artista, Pais, Album, Anio, Ventas, Genero, NumCanciones)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datos.get("Artista"),
                datos.get("Pais"),
                datos.get("Album"),
                int(datos.get("Anio")),
                datos.get("Ventas"),
                datos.get("Genero"),
                int(datos.get("NumCanciones"))
            ))
            conexion.commit()
            self.controller.actualizar_dataframe() # Recargar DF con el nuevo registro
            
            messagebox.showinfo("Éxito", "Álbum agregado y guardado correctamente.")

            # Limpiar campos
            for entry in self.campos.values():
                try:
                    entry.delete(0, tk.END)
                except Exception:
                    try:
                        entry.set("")
                    except Exception:
                        pass
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar en la base de datos: {e}")

# ============================
# === 6. CONSULTA Y MODIFICACIÓN ===
# ============================

class PaginaConsultar(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.current_codigo = None

        customtkinter.CTkLabel(self, text="Consultar y Modificar Álbum", font=("Arial", 24, "bold")).pack(pady=20)
        
        # Búsqueda por Código (ID)
        search_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        search_frame.pack(padx=20, pady=10)
        customtkinter.CTkLabel(search_frame, text="Código de Álbum (ID):").pack(side="left", padx=5)
        self.entry_codigo = customtkinter.CTkEntry(search_frame, width=150)
        self.entry_codigo.pack(side="left", padx=5)
        customtkinter.CTkButton(search_frame, text="Buscar", command=self.buscar_album).pack(side="left", padx=5)

        # Edición
        self.edit_frame = customtkinter.CTkScrollableFrame(self, label_text="Datos del Álbum (Edición)", width=600)
        self.edit_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.campos_edit = {}
        self.crear_campos_edicion()
        
        # Botones de acción (UN SOLO BLOQUE)
        btn_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        self.btn_guardar = customtkinter.CTkButton(btn_frame, text="Actualizar Álbum", width=200, state="disabled", command=self.actualizar_album)
        self.btn_guardar.pack(side="left", padx=10)
        customtkinter.CTkButton(btn_frame, text="Volver al Menú", width=200, command=lambda: controller.mostrar_pagina("PaginaMenuPrincipal")).pack(side="left", padx=10)

        # La llamada inicial debe deshabilitar los campos
        self.habilitar_edicion(False)

    def crear_campos_edicion(self):
        # Campos a mostrar para edición (incluye los mapeos y adicionales)
        campos_layout = [
            ("Código (ID)", "Codigo", "entry"), 
            ("Artista (Proveedor)", "Artista", "entry"),
            ("País", "Pais", "entry"),
            ("Nombre Álbum (Nombre)", "Album", "entry"),
            ("Año (Adicional)", "Anio", "entry"),
            ("Ventas (Texto Original)", "Ventas", "entry"),
            ("Género (Categoría)", "Genero", "combobox", albums_df['Genero'].unique().tolist()),
            ("No. Canciones (Stock)", "NumCanciones", "entry"),
        ]

        for i, (label_text, key, tipo, *opciones) in enumerate(campos_layout):
            row = i
            customtkinter.CTkLabel(self.edit_frame, text=f"{label_text}:").grid(row=row, column=0, padx=10, pady=5, sticky="w")
            
            if tipo == "entry":
                self.campos_edit[key] = customtkinter.CTkEntry(self.edit_frame, width=250, state="disabled")
                self.campos_edit[key].grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            elif tipo == "combobox":
                self.campos_edit[key] = customtkinter.CTkComboBox(self.edit_frame, values=opciones[0], width=250, state="disabled")
                self.campos_edit[key].grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        
        # Código no editable
        try:
            self.campos_edit["Codigo"].configure(state="disabled")
        except Exception:
            pass

    def habilitar_edicion(self, enabled):
        estado = "normal" if enabled else "disabled"
        btn_estado = "normal" if enabled else "disabled"
        
        for key, entry in self.campos_edit.items():
            if key != "Codigo":
                 entry.configure(state=estado)
        
        self.btn_guardar.configure(state=btn_estado)
        
    def limpiar_campos(self):
        for entry in self.campos_edit.values():
            try:
                entry.configure(state="normal")
                entry.delete(0, tk.END)
                if isinstance(entry, customtkinter.CTkComboBox):
                    entry.set("")
                entry.configure(state="disabled")
            except Exception:
                pass
        self.current_codigo = None

    def buscar_album(self):
        self.limpiar_campos()
        self.habilitar_edicion(False)

        codigo_str = self.entry_codigo.get().strip()
        if not codigo_str or not es_entero_valido(codigo_str):
            messagebox.showerror("Error", "Ingresa un Código de Álbum (ID) válido.")
            return

        codigo = int(codigo_str)
        
        try:
            album = albums_df[albums_df['Codigo'] == codigo].iloc[0]
            self.current_codigo = codigo

            self.habilitar_edicion(True)
            for key, entry in self.campos_edit.items():
                valor = str(album.get(key, ""))
                entry.configure(state="normal")
                try:
                    entry.delete(0, tk.END)
                    entry.insert(0, valor)
                except Exception:
                    try:
                        entry.set(valor)
                    except Exception:
                        pass
                entry.configure(state="normal" if key != "Codigo" else "disabled")
            
            messagebox.showinfo("Éxito", f"Álbum con código {codigo} encontrado.")

        except IndexError:
            messagebox.showwarning("No Encontrado", f"No se encontró el Álbum con el código {codigo}.")
            if messagebox.askyesno("Agregar Álbum", "¿Desea agregarlo ahora?"):
                self.controller.mostrar_pagina("PaginaAgregar")

    def actualizar_album(self):
        if self.current_codigo is None:
            messagebox.showerror("Error", "No hay álbum seleccionado para actualizar.")
            return

        datos_actualizados = {key: (entry.get().strip() if hasattr(entry, 'get') else '') for key, entry in self.campos_edit.items()}

        if not es_entero_valido(datos_actualizados.get("NumCanciones")) or not es_entero_valido(datos_actualizados.get("Anio")):
            messagebox.showerror("Error", "No. Canciones y Año deben ser números enteros válidos.")
            return

        # 1. Actualizar la base de datos (SQLITE)
        try:
            cursor.execute("""
            UPDATE Albums SET Artista=?, Pais=?, Album=?, Anio=?, Ventas=?, Genero=?, NumCanciones=?
            WHERE id=?
            """, (
                datos_actualizados.get("Artista"),
                datos_actualizados.get("Pais"),
                datos_actualizados.get("Album"),
                int(datos_actualizados.get("Anio")),
                datos_actualizados.get("Ventas"),
                datos_actualizados.get("Genero"),
                int(datos_actualizados.get("NumCanciones")),
                self.current_codigo
            ))
            conexion.commit()
            
            # 2. Recargar el DataFrame para reflejar los cambios en el resto de la app
            self.controller.actualizar_dataframe()

            messagebox.showinfo("Éxito", f"Álbum actualizado correctamente.")
            
            self.limpiar_campos()
            self.habilitar_edicion(False)
            self.entry_codigo.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error de Actualización", f"No se pudo actualizar el álbum: {e}")

# ============================
# === 2, 7 & 8. FILTROS Y GRÁFICOS DINÁMICOS ===
# ============================

class PaginaFiltros(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.resultados_df = albums_df.copy()
        self.current_chart_func = self.mostrar_grafico_dispersion # Gráfico por defecto

        customtkinter.CTkLabel(self, text="Filtros Interactivos y Gráficos Dinámicos", font=("Arial", 24, "bold")).pack(pady=10)

        # 1. Panel de Control (Filtros y Colores)
        control_frame = customtkinter.CTkFrame(self)
        control_frame.pack(padx=20, pady=5, fill="x")
        
        # Personalización de Colores (Requisito 8)
        color_opciones_keys = list(controller.get_color_opciones().keys())
        self.color_var = tk.StringVar(value=color_opciones_keys[0])
        customtkinter.CTkLabel(control_frame, text="Esquema de Color:").pack(side="left", padx=10)
        self.color_combo = customtkinter.CTkComboBox(control_frame, values=color_opciones_keys, command=self.cambiar_color_y_actualizar)
        self.color_combo.set(color_opciones_keys[0])
        self.color_combo.pack(side="left", padx=10)

        # Contenedor para Checkboxes y ComboBoxes de filtro
        self.filtros_frame = customtkinter.CTkFrame(self)
        self.filtros_frame.pack(padx=20, pady=5, fill="x")
        self.crear_controles_filtros()
        
        customtkinter.CTkButton(self.filtros_frame, text="Aplicar Filtros", command=self.aplicar_filtros_combinados).grid(row=0, column=3, rowspan=2, padx=10, pady=5, sticky="nsew")

        # 2. Área de Visualización (Tabla y Gráficos)
        main_view_frame = customtkinter.CTkFrame(self)
        main_view_frame.pack(padx=20, pady=10, fill="both", expand=True)
        main_view_frame.grid_rowconfigure(1, weight=1)
        main_view_frame.grid_columnconfigure((0, 1), weight=1)

        # Botones de Gráficos
        btn_graf_frame = customtkinter.CTkFrame(main_view_frame, fg_color="transparent")
        btn_graf_frame.grid(row=0, column=0, columnspan=2, pady=5)
        customtkinter.CTkButton(btn_graf_frame, text="Dispersión (Ventas vs Año)", command=self.set_chart_func(self.mostrar_grafico_dispersion)).pack(side="left", padx=5)
        customtkinter.CTkButton(btn_graf_frame, text="Boxplot (Ventas x Género)", command=self.set_chart_func(self.mostrar_grafico_boxplot)).pack(side="left", padx=5)
        customtkinter.CTkButton(btn_graf_frame, text="Histograma (Stock/Canciones)", command=self.set_chart_func(self.mostrar_grafico_histograma)).pack(side="left", padx=5)

        # Tabla de Resultados
        self.tabla_frame = customtkinter.CTkFrame(main_view_frame)  # CTkFrame no acepta label_text
        self.tabla_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.treeview = self.crear_tabla(self.tabla_frame)
        self.actualizar_tabla(albums_df.head(10))

        # Contenedor de Gráfico
        self.grafico_frame = customtkinter.CTkFrame(main_view_frame)  # CTkFrame no acepta label_text
        self.grafico_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.grafico_frame.grid_rowconfigure(0, weight=1)
        self.grafico_frame.grid_columnconfigure(0, weight=1)
        self.canvas_widget = None

        customtkinter.CTkButton(self, text="Volver al Menú", width=200, command=lambda: controller.mostrar_pagina("PaginaMenuPrincipal")).pack(pady=10)

    def cambiar_color_y_actualizar(self, key):
        """Actualiza el color global y fuerza la actualización del gráfico actual."""
        self.controller.set_color_seleccionado(key)
        if self.canvas_widget and self.current_chart_func:
            self.current_chart_func()

    def set_chart_func(self, func):
        """Función para asignar el gráfico actual y ejecutarlo."""
        def handler():
            self.current_chart_func = func
            func()
        return handler
    
    def actualizar_comboboxes(self):
        """Actualiza los valores de los ComboBoxes con los datos actuales del DF."""
        # Se llama desde App.actualizar_dataframe()
        generos = sorted(albums_df['Genero'].unique().tolist())
        try:
            self.filtro_genero_combo.configure(values=["Todos"] + generos)
        except Exception:
            pass
        
        paises = sorted(albums_df['Pais'].unique().tolist())
        try:
            self.filtro_pais_combo.configure(values=["Todos"] + paises)
        except Exception:
            pass

    def crear_controles_filtros(self):
        """Crea los widgets interactivos para aplicar filtros."""
        
        # Filtros básicos (Checkboxes)
        self.filtro_precio_promedio = tk.BooleanVar()
        customtkinter.CTkCheckBox(self.filtros_frame, text="Ventas > Promedio", variable=self.filtro_precio_promedio).grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.filtro_stock_bajo = tk.BooleanVar()
        customtkinter.CTkCheckBox(self.filtros_frame, text="Stock Bajo (Canciones < 10)", variable=self.filtro_stock_bajo).grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.filtro_alta_demanda = tk.BooleanVar()
        customtkinter.CTkCheckBox(self.filtros_frame, text="Demanda='Alto' & Stock > 15", variable=self.filtro_alta_demanda).grid(row=0, column=2, padx=10, pady=5, sticky="w")

        # Filtro por Categoría (Género)
        generos = sorted(albums_df['Genero'].unique().tolist())
        self.categoria_var = tk.StringVar(value="Todos")
        customtkinter.CTkLabel(self.filtros_frame, text="Género:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.filtro_genero_combo = customtkinter.CTkComboBox(self.filtros_frame, values=["Todos"] + generos)
        self.filtro_genero_combo.set("Todos")
        self.filtro_genero_combo.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Filtro Adicional 1: País
        paises = sorted(albums_df['Pais'].unique().tolist())
        self.filtro_pais_var = tk.StringVar(value="Todos")
        customtkinter.CTkLabel(self.filtros_frame, text="País:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.filtro_pais_combo = customtkinter.CTkComboBox(self.filtros_frame, values=["Todos"] + paises)
        self.filtro_pais_combo.set("Todos")
        self.filtro_pais_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Filtro Adicional 2: Año (>=)
        self.filtro_anio_var = tk.StringVar(value="")
        customtkinter.CTkLabel(self.filtros_frame, text="Año >=:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        customtkinter.CTkEntry(self.filtros_frame, width=100, textvariable=self.filtro_anio_var).grid(row=2, column=3, padx=10, pady=5, sticky="w")

    def aplicar_filtros_combinados(self):
        df_filtrado = albums_df.copy()

        # 1. Filtro Básico: Ventas Superior al Promedio
        if self.filtro_precio_promedio.get() and not df_filtrado.empty and df_filtrado['Ventas_numeric'].mean() > 0:
            ventas_promedio = df_filtrado['Ventas_numeric'].mean()
            df_filtrado = df_filtrado[df_filtrado['Ventas_numeric'] > ventas_promedio]
        
        # 2. Filtro Básico: Stock Bajo (No. Canciones < 10)
        if self.filtro_stock_bajo.get():
            df_filtrado = df_filtrado[df_filtrado['NumCanciones'] < 10]

        # 3. Filtro Básico: Alta Demanda y Stock > 15
        if self.filtro_alta_demanda.get():
            df_filtrado = df_filtrado[(df_filtrado['Demanda'] == 'Alto') & (df_filtrado['NumCanciones'] > 15)]

        # 4. Filtro por Género (Categoría)
        genero_seleccionado = self.filtro_genero_combo.get()
        if genero_seleccionado and genero_seleccionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Genero'] == genero_seleccionado]

        # 5. Filtro Adicional 1: País
        pais_seleccionado = self.filtro_pais_combo.get()
        if pais_seleccionado and pais_seleccionado != "Todos":
            df_filtrado = df_filtrado[df_filtrado['Pais'] == pais_seleccionado]

        # 6. Filtro Adicional 2: Año
        anio_str = self.filtro_anio_var.get().strip()
        if anio_str and es_entero_valido(anio_str):
            anio = int(anio_str)
            df_filtrado = df_filtrado[df_filtrado['Anio'] >= anio]

        self.resultados_df = df_filtrado
        self.actualizar_tabla(self.resultados_df)
        messagebox.showinfo("Filtros Aplicados", f"Se encontraron {len(self.resultados_df)} resultados.")
        
        # Actualizar gráfico dinámico
        if self.canvas_widget and self.current_chart_func:
            self.current_chart_func()

    def crear_tabla(self, master):
        """Crea la Treeview para mostrar el DataFrame (Requisito: Mostrar resultados)."""
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        
        # Muestra solo las columnas relevantes
        columnas_visibles = ['Codigo', 'Album', 'Genero', 'Ventas_numeric', 'NumCanciones', 'Artista', 'Demanda', 'Pais', 'Anio']
        columnas_encabezado = ['Código', 'Álbum', 'Género', 'Ventas (M)', 'Canciones', 'Artista', 'Demanda', 'País', 'Año']
        
        tree = ttk.Treeview(master, columns=columnas_visibles, show='headings')

        for col, head in zip(columnas_visibles, columnas_encabezado):
            tree.heading(col, text=head, anchor='center')
            tree.column(col, anchor='center', width=100)

        # Scrollbars
        vsb = ttk.Scrollbar(master, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y", padx=5)
        tree.configure(yscrollcommand=vsb.set)
        
        hsb = ttk.Scrollbar(master, orient="horizontal", command=tree.xview)
        hsb.pack(side="bottom", fill="x", pady=5)
        tree.configure(xscrollcommand=hsb.set)

        tree.pack(side="left", fill="both", expand=True)
        return tree

    def actualizar_tabla(self, df):
        try:
            self.treeview.delete(*self.treeview.get_children())
        except Exception:
            pass
        
        columnas_visibles = ['Codigo', 'Album', 'Genero', 'Ventas_numeric', 'NumCanciones', 'Artista', 'Demanda', 'Pais', 'Anio']
        
        for index, row in df.iterrows():
            valores = [row.get(col, '') for col in columnas_visibles]
            try:
                self.treeview.insert("", "end", values=valores)
            except Exception:
                pass
            
    def limpiar_grafico(self):
        if self.canvas_widget:
            try:
                self.canvas_widget.destroy()
            except Exception:
                pass
            self.canvas_widget = None

    # --- Funciones de Gráficos Dinámicos (Requisito 7) ---

    def mostrar_grafico_dispersion(self):
        self.limpiar_grafico()
        
        df = self.resultados_df.copy().dropna(subset=['Ventas_numeric', 'Anio'])
        if df.empty:
            messagebox.showwarning("Gráfico", "No hay datos válidos para graficar.")
            return

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100) 
        color = self.controller.get_color_seleccionado()[0]
        ax.scatter(df['Anio'], df['Ventas_numeric'], color=color, alpha=0.7)
        ax.set_title('Dispersión: Ventas (M) vs Año')
        ax.set_xlabel('Año de Lanzamiento')
        ax.set_ylabel('Ventas (Millones)')
        ax.grid(True)
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


    def mostrar_grafico_boxplot(self):
        self.limpiar_grafico()

        df = self.resultados_df.copy().dropna(subset=['Ventas_numeric', 'Genero'])
        if df.empty:
             messagebox.showwarning("Gráfico", "No hay datos válidos (Ventas y Género) para graficar.")
             return
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        
        # Mostrar solo los 5 géneros más comunes
        top_generos = df['Genero'].value_counts().head(5).index
        df_filtrado = df[df['Genero'].isin(top_generos)]

        datos_boxplot = [df_filtrado[df_filtrado['Genero'] == gen]['Ventas_numeric'] for gen in top_generos]
        
        color_esquema = self.controller.get_color_seleccionado()

        bp = ax.boxplot(datos_boxplot, patch_artist=True, labels=top_generos)
        
        # Aplicar colores (Requisito 8)
        for i, box in enumerate(bp['boxes']):
            try:
                box.set(color=color_esquema[0], linewidth=1.5)
                box.set(facecolor=color_esquema[1])
            except Exception:
                pass
                
        ax.set_title('Boxplot de Ventas (M) por Género (Top 5)')
        ax.set_ylabel('Ventas (Millones)')
        ax.grid(axis='y')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


    def mostrar_grafico_histograma(self):
        self.limpiar_grafico()

        df = self.resultados_df.copy().dropna(subset=['NumCanciones'])
        if df.empty:
            messagebox.showwarning("Gráfico", "No hay datos de Número de Canciones para graficar.")
            return

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        color = self.controller.get_color_seleccionado()[0]
        
        ax.hist(df['NumCanciones'], bins=10, edgecolor='black', color=color)
        ax.set_title('Distribución de No. de Canciones (Stock)')
        ax.set_xlabel('Número de Canciones')
        ax.set_ylabel('Frecuencia de Álbumes')
        ax.grid(True)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# ============================
# === 9. ESTADÍSTICAS AVANZADAS (Gráficos Fijos) ===
# ============================

class PaginaEstadisticas(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        customtkinter.CTkLabel(self, text="Estadísticas Avanzadas de Álbumes", font=("Arial", 24, "bold")).pack(pady=20)

        main_frame = customtkinter.CTkFrame(self)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        btn_frame = customtkinter.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        # Botones para 3 Estadísticas Relevantes (con gráficos diferentes)
        customtkinter.CTkButton(btn_frame, text="1. Ventas Promedio por Género (Barras)", command=lambda: self.mostrar_estadistica('barras')).pack(side="left", padx=10)
        customtkinter.CTkButton(btn_frame, text="2. Tendencia de Lanzamientos (Líneas)", command=lambda: self.mostrar_estadistica('lineas')).pack(side="left", padx=10)
        customtkinter.CTkButton(btn_frame, text="3. Distribución por Demanda (Pastel)", command=lambda: self.mostrar_estadistica('pastel')).pack(side="left", padx=10)

        self.grafico_contenedor = customtkinter.CTkFrame(main_frame)
        self.grafico_contenedor.pack(padx=10, pady=10, fill="both", expand=True)
        self.grafico_contenedor.grid_rowconfigure(0, weight=1)
        self.grafico_contenedor.grid_columnconfigure(0, weight=1)
        self.canvas_widget = None

        customtkinter.CTkButton(self, text="Volver al Menú", width=200, command=lambda: controller.mostrar_pagina("PaginaMenuPrincipal")).pack(pady=10)
    
    def limpiar_grafico(self):
        if self.canvas_widget:
            try:
                self.canvas_widget.destroy()
            except Exception:
                pass
            self.canvas_widget = None

    def mostrar_estadistica(self, tipo_grafico):
        self.limpiar_grafico()

        if albums_df.empty:
            messagebox.showwarning("Estadística", "No hay datos para generar estadísticas.")
            return

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        color_esquema = self.controller.get_color_seleccionado()

        if tipo_grafico == 'barras':
            # Estadística 1: Ventas Promedio por Género (Barras)
            ventas_promedio = albums_df.groupby('Genero')['Ventas_numeric'].mean().sort_values(ascending=False)
            ventas_promedio.plot(kind='bar', ax=ax, color=color_esquema[0])
            ax.set_title('Ventas Promedio por Género')
            ax.set_xlabel('Género')
            ax.set_ylabel('Ventas Promedio (Millones)')
            ax.grid(axis='y')
            plt.xticks(rotation=45, ha='right')
        
        elif tipo_grafico == 'lineas':
            # Estadística 2: Tendencia de Lanzamiento por Año (Líneas)
            conteo_por_anio = albums_df.groupby('Anio')['Codigo'].count().sort_index()
            
            if conteo_por_anio.empty:
                 messagebox.showwarning("Estadística", "No hay suficientes datos de Año para graficar la tendencia.")
                 return
            
            conteo_por_anio.plot(kind='line', ax=ax, marker='o', color=color_esquema[0])
            ax.set_title('Tendencia de Lanzamientos de Álbumes por Año')
            ax.set_xlabel('Año de Lanzamiento')
            ax.set_ylabel('Álbumes Lanzados')
            ax.grid(True)

        elif tipo_grafico == 'pastel':
            # Estadística 3: Distribución por Nivel de Demanda (Pastel)
            conteo_demanda = albums_df['Demanda'].value_counts()
            
            if conteo_demanda.empty:
                messagebox.showwarning("Estadística", "No hay datos de Demanda para generar el gráfico de pastel.")
                return

            colores_pastel = color_esquema[:len(conteo_demanda)] 
            
            ax.pie(conteo_demanda, labels=conteo_demanda.index, autopct='%1.1f%%', startangle=90, colors=colores_pastel)
            ax.set_title('Distribución de Álbumes por Nivel de Demanda')
            ax.axis('equal')
        
        # Mostrar el gráfico en la interfaz
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_contenedor)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


# ============================
# === INICIAR APLICACIÓN ===
# ============================
if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    # Cerrar conexión al salir
    try:
        conexion.close()
    except Exception:
        pass
