import streamlit as st
import pandas as pd
from src.controlador import ControladorRelacion
from src.modelo import Relacion
from src.visualizador import VisualizadorGrafos
from src.analizador import AnalizadorLattice

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera línea)
st.set_page_config(page_title="Analizador de Relaciones ", layout="wide", page_icon=":material/hub:")

def inicializar_estado():
    """Inicializa la memoria de la aplicación si está vacía con datos por defecto."""
    if 'conjunto_base' not in st.session_state:
        st.session_state.conjunto_base = {"1", "2", "3", "4", "5"}

    if 'pares' not in st.session_state:
        st.session_state.pares = {
            ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
            ("1", "2"), ("2", "1"), ("1", "3"), ("3", "1"), ("2", "3"), ("3", "2"),
            ("4", "5"), ("5", "4")
        }


# Configuración de la página
st.set_page_config(page_title="Analizador de Relaciones", layout="wide")
inicializar_estado()

# --- PANEL DE CONTROL (Barra Lateral) ---
st.sidebar.image("https://secreacademica.cs.buap.mx/images/logo_FCC.png", width=200)
st.sidebar.title("Panel de Control")
st.sidebar.title("⚙️ Configuración del Conjunto y Relación")

# --- Botones de Precarga ---
#col_p1, col_p2 = st.sidebar.columns(2)
if st.sidebar.button(":material/schema: Precargar Equivalencia"):
    st.session_state.conjunto_base = {"1", "2", "3", "4", "5"}
    st.session_state.pares = {
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
        ("1", "2"), ("2", "1"), ("1", "3"), ("3", "1"), ("2", "3"), ("3", "2"),
        ("4", "5"), ("5", "4")
    }
    st.rerun()

if st.sidebar.button(":material/polyline: Precargar Orden Parcial"):
    st.session_state.conjunto_base = {"1", "2", "3", "4", "6", "12"}
    st.session_state.pares = {
        ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("6", "6"), ("12", "12"),
        ("1", "2"), ("1", "3"), ("1", "4"), ("1", "6"), ("1", "12"),
        ("2", "4"), ("2", "6"), ("2", "12"),
        ("3", "6"), ("3", "12"),
        ("4", "12"), ("6", "12")
    }
    st.rerun()

st.sidebar.markdown("---")

# --- 1. Definición del Conjunto Base ---
st.sidebar.subheader("1. Conjunto Base A")
conjunto_texto = st.sidebar.text_input(
    "Elementos separados por coma (ej. 1, 2, 3):",
    value=", ".join(sorted(list(st.session_state.conjunto_base)))
)

if st.sidebar.button("💾 Actualizar Conjunto Base"):
    nuevos_elementos = {x.strip() for x in conjunto_texto.split(",") if x.strip()}
    if nuevos_elementos:
        st.session_state.conjunto_base = nuevos_elementos
        # Limpiar pares cuyas componentes ya no existan en el conjunto base
        st.session_state.pares = {
            (u, v) for u, v in st.session_state.pares 
            if u in nuevos_elementos and v in nuevos_elementos
        }
        st.sidebar.success("¡Conjunto base actualizado!")
        st.rerun()
    else:
        st.sidebar.error("El conjunto no puede estar vacío.")

st.sidebar.markdown("---")

# --- 2. Formulario para Agregar Par Ordenado (Estilo Imagen) ---
with st.sidebar.container():
    st.subheader("2. Agregar Par Ordenado")
    
    elementos_disp = sorted(list(st.session_state.conjunto_base))
    
    if elementos_disp:
        c1, c2 = st.columns(2)
        origen = c1.selectbox("Origen (a):", options=elementos_disp, key="sel_origen")
        destino = c2.selectbox("Destino (b):", options=elementos_disp, key="sel_destino")

        if st.button("➕ Agregar Par a la Relación", use_container_width=True):
            # Validar que pertenezcan al conjunto base
            if origen in st.session_state.conjunto_base and destino in st.session_state.conjunto_base:
                st.session_state.pares.add((origen, destino))
                st.success(f"Par ({origen}, {destino}) agregado.")
                st.rerun()
            else:
                st.error("Error: Los elementos deben pertenecer al conjunto base.")
    else:
        st.warning("Define primero un conjunto base.")

st.sidebar.markdown("---")

# --- 3. Formulario para Eliminar Par Ordenado ---
with st.sidebar.container():
    st.subheader("3. Eliminar Par Ordenado")
    
    pares_ordenados = sorted([f"({u}, {v})" for u, v in st.session_state.pares])
    
    if pares_ordenados:
        par_a_eliminar = st.selectbox("Selecciona el par a eliminar:", options=pares_ordenados)
        
        if st.button("❌ Eliminar Par", use_container_width=True):
            # Parsear tupla desde "(a, b)"
            u, v = par_a_eliminar.strip("()").replace(" ", "").split(",")
            st.session_state.pares.remove((u, v))
            st.success(f"Par ({u}, {v}) eliminado.")
            st.rerun()
    else:
        st.info("La relación no tiene pares registrados.")

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Vaciar Relación Completamente"):
    st.session_state.pares = set()
    st.rerun()



st.markdown("##### ANGEL SANCHEZ CABRERA")
st.markdown("##### Maestría en Ciencias de la Computación-BUAP")
# --- PANEL PRINCIPAL ---
st.title("Análisis de Relaciones Matemáticas :material/hub:")

# Verificamos que existan datos en memoria antes de evaluar
if st.session_state.conjunto_base and st.session_state.pares:
    
    # Instanciamos el objeto Relacion con los datos vigentes de session_state
    relacion = Relacion(st.session_state.conjunto_base, st.session_state.pares)

    # Muestra del estado actual en el cuerpo de la aplicación
    st.markdown(f"**Conjunto Base A:** `{sorted(list(relacion.conjunto_base))}`")
    st.markdown(f"**Pares de R ({len(relacion.pares)}):** `{sorted(list(relacion.pares))}`")
    
    st.subheader("1. Propiedades Básicas")

    # --- Reflexiva ---
    if relacion.es_reflexiva():
        st.write("Reflexiva: ✅")
    else:
        faltantes = relacion.obtener_fallas_reflexiva()
        st.write(f"Reflexiva: ❌ *(No es reflexiva porque le faltan los pares: `{sorted(faltantes)}`)*")

    # --- Antirreflexiva ---
    if relacion.es_antirreflexiva():
        st.write("Antirreflexiva: ✅")
    else:
        violaciones = relacion.obtener_fallas_antirreflexiva()
        st.write(f"Antirreflexiva: ❌ *(No es antirreflexiva porque contiene los pares diagonales: `{sorted(violaciones)}`)*")

    # --- Simétrica ---
    if relacion.es_simetrica():
        st.write("Simétrica: ✅")
    else:
        faltantes = relacion.obtener_fallas_simetrica()
        st.write(f"Simétrica: ❌ *(No es simétrica porque le faltan los pares inversos: `{sorted(faltantes)}`)*")

    # --- Asimétrica ---
    if relacion.es_asimetrica():
        st.write("Asimétrica: ✅")
    else:
        violaciones = relacion.obtener_fallas_asimetrica()
        st.write(f"Asimétrica: ❌ *(No es asimétrica porque contiene pares simétricos o diagonales: `{sorted(violaciones)}`)*")

    # --- Antisimétrica ---
    if relacion.es_antisimetrica():
        st.write("Antisimétrica: ✅")
    else:
        violaciones = relacion.obtener_fallas_antisimetrica()
        st.write(f"Antisimétrica: ❌ *(No es antisimétrica porque contiene pares bidireccionales con elementos distintos: `{sorted(violaciones)}`)*")

    # --- Transitiva ---
    if relacion.es_transitiva():
        st.write("Transitiva: ✅")
    else:
        faltantes = relacion.obtener_fallas_transitiva()
        st.write(f"Transitiva: ❌ *(No es transitiva porque le faltan los enlaces por encadenamiento: `{sorted(faltantes)}`)*")
    
    st.subheader("2. Clasificación y Gráficos")
    
    if relacion.es_relacion_equivalencia():
        st.success("¡Es una Relación de Equivalencia! 🌟")
        
        # Dividimos la pantalla
        col_izq, col_der = st.columns(2)
        
        with col_izq:
            st.markdown("### 📦 Clases de Equivalencia")
            particiones = relacion.generar_particiones()
            for i, clase in enumerate(particiones):
                #st.write(f"**Clase {i+1}:** {', '.join(clase)}")
                st.write(f"**Clase {i+1}:** {{{', '.join(clase)}}}")
            st.subheader("🧮 Matriz Booleana")
            # Ordenamos los elementos para que la tabla se vea limpia (1, 2, 3, 4, 5)
            elementos = sorted(list(relacion.conjunto_base))
            
            # Creamos un DataFrame asignándole las filas (index) y columnas
            matriz_df = pd.DataFrame(
                relacion.generar_matriz(), 
                index=elementos, 
                columns=elementos
            )
            
            # Mostramos la tabla con los encabezados correctos
            st.dataframe(matriz_df)
                        # 🎨 Selector de color (por defecto en gris claro como tu imagen)
            # 🎨 Selector de color dinámico
            #color_nodo = st.color_picker("Elige el color de los nodos", "#D3D3D3")

            st.subheader("🕸️ Grafo Dirigido de la Relación")
            visualizador = VisualizadorGrafos()

            figura = visualizador.generar_grafo_dirigido(relacion)#color_nodo

            # Renderizado interactivo con Plotly adaptado a la pantalla completa
            st.plotly_chart(figura, use_container_width=True)

            
        
            
    elif relacion.es_orden_parcial():
        st.info("¡Es una Relación de Orden Parcial! 🪜")

        analizador = AnalizadorLattice(relacion)

        col_izq, col_der = st.columns([1, 1])

        with col_izq:
            st.markdown("### 📊 Propiedades del Orden")

            # Ahora sí coinciden las llamadas
            if analizador.es_lattice():
                st.success("✅ ¡El orden parcial forma una Retícula (Lattice)!")
            else:
                st.warning("❌ No es una Retícula.")

            st.markdown("---")
            st.markdown("### 🎯 Análisis de Subconjunto")

            elementos_ordenados = sorted(list(relacion.conjunto_base))
            subconjunto_sel = st.multiselect(
                "Selecciona un subconjunto B:",
                options=elementos_ordenados,
                default=elementos_ordenados[:2] if len(elementos_ordenados) >= 2 else elementos_ordenados
            )

        destacados = {}
        if subconjunto_sel:
            sub_set = set(subconjunto_sel)
            
            # Pasamos directamente el subconjunto seleccionado
            cotas_sup = analizador.obtener_cotas_superiores(sub_set)
            cotas_inf = analizador.obtener_cotas_inferiores(sub_set)
            supremo = analizador.obtener_supremo(sub_set)
            infimo = analizador.obtener_infimo(sub_set)

            destacados = {
                'supremo': supremo,
                'infimo': infimo,
                'cotas_superiores': cotas_sup,
                'cotas_inferiores': cotas_inf
            }

            with col_der:
                st.markdown("### 📝 Resultados para B = {" + ", ".join(subconjunto_sel) + "}")
                st.write(f"🟡 **Cotas Superiores:** {sorted(list(cotas_sup)) if cotas_sup else 'Ninguna'}")
                st.write(f"🔴 **Supremo (LUB):** {supremo if supremo else 'No existe'}")
                st.write(f"🟢 **Cotas Inferiores:** {sorted(list(cotas_inf)) if cotas_inf else 'Ninguna'}")
                st.write(f"🔵 **Ínfimo (GLB):** {infimo if infimo else 'No existe'}")

        st.markdown("---")

        st.markdown("### 🕸️ Diagrama de Hasse")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown("🔴 **Supremo**")
        col2.markdown("🔵 **Ínfimo**")
        col3.markdown("🟡 **Cota Superior**")
        col4.markdown("🟢 **Cota Inferior**")

        visualizador = VisualizadorGrafos()
        figura_hasse = visualizador.generar_diagrama_hasse(relacion, elementos_destacados=destacados)
        st.plotly_chart(figura_hasse, use_container_width=True)

    else:
        st.warning("No es de Equivalencia ni de Orden Parcial.")

else:
    st.warning("⚠️ El conjunto base o la relación están vacíos. Agrega elementos o utiliza un botón de precarga en la barra lateral.")


