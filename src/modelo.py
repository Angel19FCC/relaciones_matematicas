class Relacion:

    def __init__(self, conjunto_base: set, pares: set):
        self.conjunto_base = conjunto_base
        self.pares = pares
        self.validar_pertenencia()

    def validar_pertenencia(self):
        """Verifica que todos los elementos de los pares pertenezcan al conjunto base."""
        for a, b in self.pares:
            if a not in self.conjunto_base or b not in self.conjunto_base:
                raise ValueError(
                    f"El par ({a}, {b}) contiene elementos fuera del conjunto base."
                )

    def es_reflexiva(self) -> bool:
        """ Evalúa si la relación es reflexiva: ∀x ∈ A, (x, x) ∈ R """
        for x in self.conjunto_base:
            if (x, x) not in self.pares:
                return False  # Si falta al menos un par (x, x), no es reflexiva ❌
        return True  # Si todos están presentes, es reflexiva ✅

    def es_simetrica(self) -> bool:
        """ Evalúa si la relación es simétrica: ∀(x, y) ∈ R ⇒ (y, x) ∈ R """
        for x, y in self.pares:
            if (y, x) not in self.pares:
                return False  # Si falta el inverso de algún par, no es simétrica ❌
        return True  # Si todos tienen su inverso, es simétrica ✅

    def es_antirreflexiva(self) -> bool:
        """ Evalúa si la relación es antirreflexiva: ∀x ∈ A, (x, x) ∉ R """
        for x in self.conjunto_base:
            if (x, x) in self.pares:
                return False  # Si existe al menos un (x, x), no es antirreflexiva ❌
        return True  # Si ningún elemento se relaciona consigo mismo, es antirreflexiva ✅

    def es_asimetrica(self) -> bool:
        """ Evalúa si la relación es asimétrica: ∀(x, y) ∈ R ⇒ (y, x) ∉ R """
        for x, y in self.pares:
            if (y, x) in self.pares:
                return False  # Si existe el par inverso (o si es de la forma (x, x)), no es asimétrica ❌
        return True  # Si ningún par tiene su inverso, es asimétrica ✅

    def es_antisimetrica(self):
        for x, y in self.pares:
            # Si existe su inversa Y NO son la misma variable -> Violación de antisimetría
            if (y, x) in self.pares and x != y:
                return False
                
        return True
    
    def es_transitiva(self) -> bool:
        for x, y in self.pares:
            # Buscamos un par (y2, z) donde el primer elemento (y2) sea igual al segundo elemento (y) del primer par
            for y2, z in self.pares:
                if y == y2:
                    # Existe la cadena: (x, y) y (y, z)
                    # Verificamos si el par directo (x, z) NO está en la relación
                    if (x, z) not in self.pares:
                        return False
                        
        return True

    def es_relacion_equivalencia(self) -> bool:
        """Una relación es de equivalencia si es Reflexiva, Simétrica y Transitiva."""
        return self.es_reflexiva() and self.es_simetrica() and self.es_transitiva()

    def es_orden_parcial(self) -> bool:
        """Una relación es de orden parcial si es Reflexiva, Antisimétrica y Transitiva."""
        return self.es_reflexiva() and self.es_antisimetrica() and self.es_transitiva()

    def analizar(self):
        """Imprime un resumen completo del análisis de la relación."""
        print(f"\n--- Análisis de la Relación ---")
        print(f"Conjunto A: {self.conjunto_base}")
        print(f"Relación R: {self.pares}")
        print(f"• Reflexiva:      {self.es_reflexiva()}")
        print(f"• Simétrica:      {self.es_simetrica()}")
        print(f"• Antisimétrica:  {self.es_antisimetrica()}")
        print(f"• Transitiva:     {self.es_transitiva()}")
        print(f"➔ ¿Es de Equivalencia?: {self.es_relacion_equivalencia()}")
        print(f"➔ ¿Es de Orden Parcial?: {self.es_orden_parcial()}")

    def generar_matriz(self) -> list:
        """Genera la matriz booleana de la relación."""
        elementos = sorted(self.conjunto_base)
        matriz = []
        
        for x in elementos:
            fila = []
            for y in elementos:
                if (x, y) in self.pares:
                    fila.append(1)
                else:
                    fila.append(0)
            matriz.append(fila)
            
        return matriz

    def generar_particiones(self) -> list:
        """Genera las clases de equivalencia (particiones) de la relación."""
        particiones = []
        for x in self.conjunto_base:
            # Aplicamos exactamente la lógica que describiste
            clase_x = {y for y in self.conjunto_base if (x, y) in self.pares}
            
            # Solo la guardamos si no la hemos registrado antes
            if clase_x not in particiones:
                particiones.append(clase_x)
                
        return particiones
