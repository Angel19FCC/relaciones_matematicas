from src.modelo import Relacion
import itertools

class AnalizadorLattice:
    """Clase para analizar si un Orden Parcial es una Retícula (Lattice)."""

    def __init__(self, relacion: Relacion):
        if not relacion.es_orden_parcial():
            raise ValueError("El análisis de retículas exige una relación de orden parcial.")
        self.relacion = relacion
        self.pares = relacion.pares
        self.conjunto = relacion.conjunto_base

    def obtener_cotas_superiores(self, subconjunto) -> set:
        """Encuentra todos los elementos 'c' tales que x <= c para todo 'x' en el subconjunto."""
        if not subconjunto:
            return set()
        return {
            c
            for c in self.conjunto
            if all((x, c) in self.pares for x in subconjunto)
        }

    def obtener_cotas_inferiores(self, subconjunto) -> set:
        """Encuentra todos los elementos 'c' tales que c <= x para todo 'x' en el subconjunto."""
        if not subconjunto:
            return set()
        return {
            c
            for c in self.conjunto
            if all((c, x) in self.pares for x in subconjunto)
        }

    def obtener_supremo(self, subconjunto):
        """Encuentra el supremo (menor cota superior). Retorna None si no existe."""
        cotas_sup = self.obtener_cotas_superiores(subconjunto)
        for s in cotas_sup:
            if all((s, c) in self.pares for c in cotas_sup):
                return s
        return None

    def obtener_infimo(self, subconjunto):
        """Encuentra el ínfimo (mayor cota inferior). Retorna None si no existe."""
        cotas_inf = self.obtener_cotas_inferiores(subconjunto)
        for i in cotas_inf:
            if all((c, i) in self.pares for c in cotas_inf):
                return i
        return None

    def es_lattice(self) -> bool:
        """Determina si la relación de orden parcial es una retícula.
        Verifica que todo par de elementos tenga un supremo y un ínfimo.
        """
        if len(self.conjunto) < 2:
            return True

        # Generamos todos los pares posibles (a, b)
        for a, b in itertools.combinations(self.conjunto, 2):
            par = {a, b}  # Convertimos a conjunto para pasarlo como 1 solo argumento

            supremo = self.obtener_supremo(par)
            infimo = self.obtener_infimo(par)

            # Si a algún par le falta supremo o ínfimo, no es retícula
            if supremo is None or infimo is None:
                return False

        return True

    