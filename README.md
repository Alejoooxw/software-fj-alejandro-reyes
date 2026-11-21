# Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Proyecto correspondiente al **Componente Práctico - Fase 4** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD).

## Integrante y Participación
* **Luis Alejandro Reyes Díaz** (`@Alejoooxw`) — Desarrollo integral del sistema (arquitectura orientada a objetos, manejo avanzado de excepciones, bitácora de eventos, simulaciones y GUI en Tkinter).  
*(Nota: Ante la falta de participación e interacción de los demás integrantes asignados al grupo hasta la fecha de cierre, se asumió el desarrollo completo de forma individual dejando constancia previa en el foro colaborativo).*

## Estructura del Repositorio
```text
software-fj-alejandro-reyes/
├── main.py                # Punto de entrada principal de la aplicación
├── gui.py                 # Interfaz gráfica en Tkinter (en inglés)
├── simulaciones.py        # Ejecución de 12 escenarios (válidos e inválidos)
├── modelo/
│   ├── __init__.py
│   ├── excepciones.py     # Jerarquía de excepciones personalizadas (ErrorSistema y derivadas)
│   ├── registro.py        # Configuración de logging hacia logs/sistema.log
│   ├── entidad.py         # Clase abstracta base Entidad (ABC)
│   ├── cliente.py         # Clase Cliente con encapsulación (@property) y validaciones
│   ├── servicios.py       # Clase abstracta Servicio + ReservaSala, AlquilerEquipo, Asesoria
│   └── reserva.py         # Clase Reserva (confirmar, cancelar, procesar)
├── logs/
│   └── sistema.log        # Archivo de registro generado durante la ejecución
└── docs/
    └── capturas/          # Evidencias visuales del funcionamiento