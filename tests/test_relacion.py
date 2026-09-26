import unittest
from src.modelo import Relacion


class TestRelacion(unittest.TestCase):

    def setUp(self):
        """Conjunto base de prueba A = {1, 2, 3}"""
        self.conjunto_A = {1, 2, 3}

    # 1. Validación de Errores ⚠️
    def test_validacion_pertenencia(self):
        # El elemento 4 no pertenece al conjunto base A
        R_invalida = {(1, 2), (2, 4)}
        with self.assertRaises(ValueError):
            Relacion(self.conjunto_A, R_invalida)

    # 2. Propiedad Reflexiva 🪞
    def test_reflexiva(self):
        R_pos = {(1, 1), (2, 2), (3, 3), (1, 2)}
        R_neg = {(1, 1), (2, 2)}  # Falta (3,3)
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_reflexiva())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_reflexiva())

    # 3. Propiedad Antirreflexiva 🚫
    def test_antirreflexiva(self):
        R_pos = {(1, 2), (2, 3)}
        R_neg = {(1, 1), (2, 3)}  # Contiene (1,1)
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_antirreflexiva())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_antirreflexiva())

    # 4. Propiedad Simétrica 🔄
    def test_simetrica(self):
        R_pos = {(1, 1), (1, 2), (2, 1)}
        R_neg = {(1, 2)}  # Falta (2,1)
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_simetrica())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_simetrica())

    # 5. Propiedad Asimétrica ⚖️
    def test_asimetrica(self):
        R_pos = {(1, 2), (2, 3)}
        R_neg = {(1, 2), (2, 1)}  # Tiene su inverso
        R_neg_diagonal = {(1, 1)}  # Las diagonales no se permiten en asimétricas
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_asimetrica())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_asimetrica())
        self.assertFalse(Relacion(self.conjunto_A, R_neg_diagonal).es_asimetrica())

    # 6. Propiedad Antisimétrica 🛡️
    def test_antisimetrica(self):
        R_pos = {(1, 1), (1, 2), (2, 3)}  # (1,1) está permitido
        R_neg = {(1, 2), (2, 1)}  # Pares espejo distintos
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_antisimetrica())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_antisimetrica())

    # 7. Propiedad Transitiva 🔗
    def test_transitiva(self):
        R_pos = {(1, 2), (2, 3), (1, 3)}
        R_neg = {(1, 2), (2, 3)}  # Falta (1,3)
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_transitiva())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_transitiva())

    # 8. Relación de Equivalencia 🌟 (Reflexiva + Simétrica + Transitiva)
    def test_equivalencia(self):
        R_pos = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}
        R_neg = {(1, 1), (2, 2), (3, 3), (1, 2)}  # No es simétrica
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_relacion_equivalencia())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_relacion_equivalencia())

    # 9. Relación de Orden Parcial 📐 (Reflexiva + Antisimétrica + Transitiva)
    def test_orden_parcial(self):
        R_pos = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 3), (1, 3)}
        R_neg = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}  # No es antisimétrica
        self.assertTrue(Relacion(self.conjunto_A, R_pos).es_orden_parcial())
        self.assertFalse(Relacion(self.conjunto_A, R_neg).es_orden_parcial())


if __name__ == "__main__":
    unittest.main()