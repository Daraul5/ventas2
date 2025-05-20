from abc import ABC, abstractmethod

class AuthInterface(ABC):
    
    @abstractmethod
    def validacion(self, usuario: str, contraseña: str) -> bool:
        """Valida los datos ingresados."""
        pass

    @abstractmethod
    def control1(self):
        """Cambia a la pantalla principal después de iniciar sesión o registrarse."""
        pass
    
    @abstractmethod
    def control2(self):
        """Cambia a la pantalla de registro o inicio de sesión según corresponda."""
        pass
    
class ModuleInterface(ABC):
    
    @abstractmethod
    def ventas(self):
        """Muestra el módulo de ventas."""
        pass
    
    @abstractmethod
    def inventario(self):
        """Muestra el módulo de inventario."""
        pass
    
    @abstractmethod
    def categorias(self):
        """Muestra el módulo de categorías."""
        pass
    
    @abstractmethod
    def proveedor(self):
        """Muestra el módulo de proveedores."""
        pass
    
    @abstractmethod
    def informacion(self):
        """Muestra la información del sistema."""
        pass
    
class Modulos(ABC):
    
    @abstractmethod
    def widgets(self):
        """Crea los widgets del módulo."""
        pass
    