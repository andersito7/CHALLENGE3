import csv
import os
from domain.cliente import Cliente
from domain.administrador import Administrador


class UsuarioRepo:
    """
    Repositorio encargado de manejar la persistencia de usuarios (clientes y administradores)
    en el archivo CSV correspondiente.
    """

    def __init__(self, filepath="data/usuarios.csv"):
        self.filepath = filepath
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """
        Crea el archivo CSV con encabezados si no existe.
        Esto evita errores al intentar leer un archivo vacío o inexistente.
        """
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["nombres", "apellidos", "dui", "pin", "rol"])
                writer.writeheader()

    def cargar_todos(self):
        """
        Carga todos los usuarios desde el CSV.
        Según el campo 'rol', reconstruye un Cliente o un Administrador.
        """
        usuarios = []
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:

                # Si el rol es cliente → reconstruimos Cliente
                if row["rol"] == "cliente":
                    usuario = Cliente(row["nombres"], row["apellidos"], row["dui"], row["pin"])

                # Si el rol es admin → reconstruimos Administrador
                else:
                    usuario = Administrador(row["nombres"], row["apellidos"], row["dui"], row["pin"])

                usuarios.append(usuario)

        return usuarios

    def guardar_todos(self, usuarios):
        """
        Sobrescribe el archivo CSV con la lista completa de usuarios.
        """
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nombres", "apellidos", "dui", "pin", "rol"])
            writer.writeheader()

            # Cada usuario sabe convertirse a dict gracias a to_dict()
            for u in usuarios:
                writer.writerow(u.to_dict())

    def agregar(self, usuario):
        """
        Agrega un usuario al archivo sin borrar los existentes.
        """
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nombres", "apellidos", "dui", "pin", "rol"])
            writer.writerow(usuario.to_dict())

    def buscar_por_dui(self, dui):
        """
        Busca un usuario por su DUI (o username en caso de admin).
        """
        for u in self.cargar_todos():
            if u.dui == dui:
                return u
        return None
