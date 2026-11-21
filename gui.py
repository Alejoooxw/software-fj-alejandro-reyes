# Importo tkinter y messagebox para construir la interfaz grafica sin dependencias externas
import tkinter as tk
from tkinter import messagebox, ttk

# Importo las clases del modelo y las simulaciones para conectarlas a la ventana
from modelo.cliente import Cliente
from modelo.excepciones import ErrorSistema
from modelo.registro import guardar_error, guardar_evento
from modelo.reserva import Reserva
from modelo.servicios import AlquilerEquipo, Asesoria, ReservaSala
from simulaciones import ejecutar_simulaciones


class SoftwareFJApp:
    # Clase principal de la ventana Tkinter en ingles que consume el modelo orientado a objetos
    def __init__(self, root):
        # Guardo la ventana raiz y configuro titulo y tamano
        self.root = root
        self.root.title("Software FJ - Clients, Services & Bookings Manager")
        self.root.geometry("760x560")
        self.root.resizable(False, False)

        # Listas internas en memoria (sin base de datos)
        self.clientes = []
        self.servicios = []
        self.reservas = []

        # Cargo unos datos iniciales de ejemplo para poder probar reservas de inmediato
        self.cargar_datos_iniciales()
        # Construyo los paneles visuales de la aplicacion
        self.construir_interfaz()
        # Refresco las listas desplegables y el cuadro de estado
        self.actualizar_listas()

    def cargar_datos_iniciales(self):
        # Creo un cliente y los tres tipos de servicios por defecto al abrir la app
        try:
            c1 = Cliente("1023456789", "Carlos Mendoza", "carlos@softwarefj.com", "3104567890")
            s1 = ReservaSala("SALA-01", "North Meeting Room", 60000, capacidad_maxima=10)
            s2 = AlquilerEquipo("EQ-01", "Dell Precision Laptop", 25000, serial_equipo="DELL-9988")
            s3 = Asesoria("ASE-01", "Cloud & Python Consulting", 95000, especialidad="AWS & Python")
            self.clientes.append(c1)
            self.servicios.extend([s1, s2, s3])
        except ErrorSistema as err:
            guardar_error(err, origen="GUI.cargar_datos_iniciales")

    def construir_interfaz(self):
        # Titulo superior de la aplicacion
        lbl_titulo = tk.Label(
            self.root,
            text="Software FJ - Management System",
            font=("Segoe UI", 15, "bold"),
            pady=10,
        )
        lbl_titulo.pack()

        # Contenedor principal con dos columnas (izquierda: formularios, derecha: registros)
        frame_principal = tk.Frame(self.root, padx=15, pady=5)
        frame_principal.pack(fill="both", expand=True)

        # --- PANEL 1: REGISTER CLIENT ---
        frame_cliente = tk.LabelFrame(frame_principal, text="1. Register Client", padx=10, pady=8)
        frame_cliente.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        tk.Label(frame_cliente, text="Document ID:").grid(row=0, column=0, sticky="w")
        self.ent_doc = tk.Entry(frame_cliente, width=25)
        self.ent_doc.grid(row=0, column=1, pady=2)

        tk.Label(frame_cliente, text="Full Name:").grid(row=1, column=0, sticky="w")
        self.ent_nombre = tk.Entry(frame_cliente, width=25)
        self.ent_nombre.grid(row=1, column=1, pady=2)

        tk.Label(frame_cliente, text="Email:").grid(row=2, column=0, sticky="w")
        self.ent_correo = tk.Entry(frame_cliente, width=25)
        self.ent_correo.grid(row=2, column=1, pady=2)

        tk.Label(frame_cliente, text="Phone:").grid(row=3, column=0, sticky="w")
        self.ent_tel = tk.Entry(frame_cliente, width=25)
        self.ent_tel.grid(row=3, column=1, pady=2)

        btn_cliente = tk.Button(
            frame_cliente,
            text="Add Client",
            bg="#1f6aa5",
            fg="white",
            command=self.crear_cliente_gui,
        )
        btn_cliente.grid(row=4, column=0, columnspan=2, pady=6, sticky="ew")

        # --- PANEL 2: CREATE BOOKING ---
        frame_reserva = tk.LabelFrame(frame_principal, text="2. New Booking", padx=10, pady=8)
        frame_reserva.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        tk.Label(frame_reserva, text="Booking ID:").grid(row=0, column=0, sticky="w")
        self.ent_res_id = tk.Entry(frame_reserva, width=25)
        self.ent_res_id.insert(0, "RES-101")
        self.ent_res_id.grid(row=0, column=1, pady=2)

        tk.Label(frame_reserva, text="Select Client:").grid(row=1, column=0, sticky="w")
        self.cmb_cliente = ttk.Combobox(frame_reserva, state="readonly", width=22)
        self.cmb_cliente.grid(row=1, column=1, pady=2)

        tk.Label(frame_reserva, text="Select Service:").grid(row=2, column=0, sticky="w")
        self.cmb_servicio = ttk.Combobox(frame_reserva, state="readonly", width=22)
        self.cmb_servicio.grid(row=2, column=1, pady=2)

        tk.Label(frame_reserva, text="Hours:").grid(row=3, column=0, sticky="w")
        self.ent_horas = tk.Entry(frame_reserva, width=25)
        self.ent_horas.insert(0, "2")
        self.ent_horas.grid(row=3, column=1, pady=2)

        btn_reserva = tk.Button(
            frame_reserva,
            text="Create & Confirm Booking",
            bg="#2e7d32",
            fg="white",
            command=self.crear_reserva_gui,
        )
        btn_reserva.grid(row=4, column=0, columnspan=2, pady=6, sticky="ew")

        # --- PANEL 3: ACTIVE BOOKINGS & ACTIONS ---
        frame_lista = tk.LabelFrame(self.root, text="3. Bookings & System Activity", padx=10, pady=8)
        frame_lista.pack(fill="both", expand=True, padx=20, pady=5)

        self.txt_salida = tk.Text(frame_lista, height=11, width=85, state="disabled", bg="#f4f6f8")
        self.txt_salida.pack(pady=4)

        # Barra inferior con botones para procesar ultima reserva o correr las 12 simulaciones
        frame_botones = tk.Frame(frame_lista)
        frame_botones.pack(fill="x", pady=4)

        tk.Button(
            frame_botones,
            text="Process Last Booking",
            command=self.procesar_ultima_reserva,
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botones,
            text="Cancel Last Booking",
            command=self.cancelar_ultima_reserva,
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botones,
            text="Run 12 Simulations (Log Test)",
            bg="#455a64",
            fg="white",
            command=self.correr_simulaciones_gui,
        ).pack(side="right", padx=5)

    def escribir_consola_gui(self, texto):
        # Escribe un mensaje en el cuadro de texto inferior de la interfaz
        self.txt_salida.config(state="normal")
        self.txt_salida.insert(tk.END, texto + "\n")
        self.txt_salida.see(tk.END)
        self.txt_salida.config(state="disabled")

    def actualizar_listas(self):
        # Actualiza los desplegables con los clientes y servicios disponibles en memoria
        self.cmb_cliente["values"] = [f"{c.documento} - {c.nombre}" for c in self.clientes]
        if self.clientes:
            self.cmb_cliente.current(0)

        self.cmb_servicio["values"] = [f"{s.identificador} - {s.nombre}" for s in self.servicios]
        if self.servicios:
            self.cmb_servicio.current(0)

    def crear_cliente_gui(self):
        # Crea un nuevo cliente capturando cualquier error de validacion sin cerrar la ventana
        try:
            nuevo = Cliente(
                self.ent_doc.get(),
                self.ent_nombre.get(),
                self.ent_correo.get(),
                self.ent_tel.get(),
            )
            self.clientes.append(nuevo)
            self.actualizar_listas()
            self.escribir_consola_gui(f"[OK] Client added: {nuevo.describir()}")
            # Limpio los campos del formulario
            self.ent_doc.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_correo.delete(0, tk.END)
            self.ent_tel.delete(0, tk.END)
        except ErrorSistema as err:
            guardar_error(err, origen="GUI.crear_cliente")
            messagebox.showerror("Validation Error", str(err))
            self.escribir_consola_gui(f"[ERROR] {err}")

    def crear_reserva_gui(self):
        # Crea y confirma una reserva usando el cliente y servicio seleccionados
        try:
            idx_cliente = self.cmb_cliente.current()
            idx_servicio = self.cmb_servicio.current()
            if idx_cliente < 0 or idx_servicio < 0:
                raise ErrorSistema("Please select both a client and a service.")

            # Convierto las horas a float capturando ValueError si escriben letras
            try:
                horas = float(self.ent_horas.get())
            except ValueError as err_num:
                raise ErrorSistema("Hours must be a valid number.") from err_num

            reserva = Reserva(
                self.ent_res_id.get(),
                self.clientes[idx_cliente],
                self.servicios[idx_servicio],
                horas=horas,
            )
            reserva.confirmar()
            self.reservas.append(reserva)
            self.escribir_consola_gui(f"[BOOKING] {reserva.resumen()}")
            messagebox.showinfo("Success", f"Booking {reserva.id_reserva} confirmed!")
        except ErrorSistema as err:
            guardar_error(err, origen="GUI.crear_reserva")
            messagebox.showerror("Booking Error", str(err))
            self.escribir_consola_gui(f"[ERROR] {err}")

    def procesar_ultima_reserva(self):
        # Procesa la ultima reserva creada aplicando manejo de excepciones
        try:
            if not self.reservas:
                raise ErrorSistema("No bookings available to process.")
            ultima = self.reservas[-1]
            ultima.procesar()
            self.escribir_consola_gui(f"[PROCESSED] {ultima.resumen()}")
        except ErrorSistema as err:
            guardar_error(err, origen="GUI.procesar_reserva")
            messagebox.showerror("Process Error", str(err))
            self.escribir_consola_gui(f"[ERROR] {err}")

    def cancelar_ultima_reserva(self):
        # Cancela la ultima reserva si su estado lo permite
        try:
            if not self.reservas:
                raise ErrorSistema("No bookings available to cancel.")
            ultima = self.reservas[-1]
            ultima.cancelar()
            self.escribir_consola_gui(f"[CANCELLED] {ultima.resumen()}")
        except ErrorSistema as err:
            guardar_error(err, origen="GUI.cancelar_reserva")
            messagebox.showerror("Cancel Error", str(err))
            self.escribir_consola_gui(f"[ERROR] {err}")

    def correr_simulaciones_gui(self):
        # Ejecuta las 12 simulaciones desde la interfaz y avisa cuando terminan
        ejecutar_simulaciones()
        guardar_evento("Simulaciones ejecutadas desde la interfaz grafica Tkinter")
        self.escribir_consola_gui("[SIMULATIONS] 12 test cases executed. Check logs/sistema.log for details.")
        messagebox.showinfo("Simulations Done", "12 operations executed and saved to logs/sistema.log.")    