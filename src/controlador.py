import ast

class ControladorRelacion:
    """Controlador para gestionar la entrada del usuario y preparar los datos."""

    @staticmethod
    def procesar_conjunto(texto_conjunto: str) -> set:
        """Convierte un texto como '1, 2, 3' en un conjunto { '1', '2', '3' }."""
        elementos = texto_conjunto.split(',')
        return {elem.strip() for elem in elementos if elem.strip()}

    @staticmethod
    def procesar_pares(texto_pares: str) -> set:
        """Convierte un texto como '(1, 2)' en un conjunto de tuplas de texto."""
        if not texto_pares.strip():
            return set()
        
        try:
            # 1. Evalúa el texto (esto te da tuplas de números)
            tuplas_crudas = ast.literal_eval(f"[{texto_pares}]")
            
            # 2. Convierte cada elemento 'a' y 'b' de las tuplas a texto
            tuplas_texto = {(str(a), str(b)) for a, b in tuplas_crudas}
            
            return tuplas_texto
            
        except (SyntaxError, ValueError):
            raise ValueError("Formato inválido. Usa paréntesis y comas, ej: (1,2), (2,3)")