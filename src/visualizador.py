import networkx as nx
import plotly.graph_objects as go
from src.modelo import Relacion


class VisualizadorGrafos:
    """Clase encargada de la generación gráfica interactiva con Plotly."""

    @staticmethod
    def generar_grafo_dirigido(relacion: Relacion, color_nodo="#D3D3D3"):
        """Genera un gráfico interactivo con Plotly forzando la representación visual de bucles reflexivos."""
        import numpy as np

        G = nx.DiGraph()
        G.add_nodes_from(relacion.conjunto_base)
        G.add_edges_from(relacion.pares)

        # Calculamos posiciones distribuidas
        pos = nx.spring_layout(G, k=1.5, seed=42)

        data_traces = []
        annotations = []

        aristas_normales = [(u, v) for u, v in G.edges() if u != v]
        aristas_reflexivas = [u for u, v in G.edges() if u == v]

        # 1. Dibujar flechas entre nodos distintos
        for u, v in aristas_normales:
            x0, y0 = pos[u]
            x1, y1 = pos[v]

            dx, dy = x1 - x0, y1 - y0
            dist = np.sqrt(dx**2 + dy**2)

            if dist > 0:
                # Recorte para no tapar el centro del nodo
                offset = 0.08
                x1_adj = x1 - (dx / dist) * offset
                y1_adj = y1 - (dy / dist) * offset
            else:
                x1_adj, y1_adj = x1, y1

            annotations.append(
                dict(
                    x=x1_adj,
                    y=y1_adj,
                    ax=x0,
                    ay=y0,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.2,
                    arrowwidth=1.2,
                    arrowcolor="#718096",
                )
            )

        # 2. Dibujar bucles reflexivos (arcos visibles sobre cada nodo)
        for u in aristas_reflexivas:
            x, y = pos[u]

            # Parámetros del bucle circular sobre el nodo
            r = 0.08  # Radio de la oreja/bucle
            theta = np.linspace(0, 2 * np.pi, 30)
            loop_x = x + r * np.cos(theta)
            loop_y = y + 0.1 + r * np.sin(theta)  # Desplazado hacia arriba del nodo

            # Trazado continuo del bucle en Plotly
            data_traces.append(
                go.Scatter(
                    x=loop_x,
                    y=loop_y,
                    mode="lines",
                    line=dict(color="#4A5568", width=1.5),
                    hoverinfo="none",
                    showlegend=False,
                )
            )

            # Flecha indicadora de sentido en la punta del bucle
            annotations.append(
                dict(
                    x=x - 0.01,
                    y=y + 0.08,
                    ax=x,
                    ay=y + 0.09,
                    xref="x",
                    yref="y",
                    axref="x",
                    ayref="y",
                    showarrow=True,
                    arrowhead=3,
                    arrowsize=1.0,
                    arrowcolor="#4A5568",
                )
            )

        # 3. Dibujar nodos
        node_x = [pos[node][0] for node in G.nodes()]
        node_y = [pos[node][1] for node in G.nodes()]
        node_text = [str(node) for node in G.nodes()]

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="middle center",
            hoverinfo="text",
            marker=dict(
                size=40,
                color=color_nodo,
                line=dict(width=0),
            ),
            textfont=dict(size=12, color="#2D3748", family="Arial"),
            showlegend=False,
        )

        data_traces.append(node_trace)

        # 4. Ensamblar figura
        fig = go.Figure(
            data=data_traces,
            layout=go.Layout(
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=20, r=20, t=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                annotations=annotations,
                height=550,
            ),
        )

        return fig

    @staticmethod
    def generar_diagrama_hasse(relacion: Relacion, elementos_destacados=None):
        """Genera el Diagrama de Hasse con distribución jerárquica estricta (de abajo hacia arriba)."""
        if not relacion.es_orden_parcial():
            raise ValueError(
                "La relación debe ser un Orden Parcial para generar un Diagrama de Hasse."
            )

        G = nx.DiGraph()
        G.add_nodes_from(relacion.conjunto_base)

        # 1. Omitir bucles reflexivos
        pares_sin_bucles = [(x, y) for x, y in relacion.pares if x != y]
        G.add_edges_from(pares_sin_bucles)

        # 2. Reducción transitiva para obtener solo las aristas directas de Hasse
        H = nx.transitive_reduction(G)

        # 3. Calcular niveles jerárquicos (Coordenada Y de abajo hacia arriba)
        niveles = {}
        for nodo in H.nodes():
            # El nivel de un nodo es la longitud del camino más largo desde cualquier nodo raíz/mínimo
            caminos = [len(c) - 1 for min_node in H.nodes() if H.in_degree(min_node) == 0 for c in nx.all_simple_paths(H, min_node, nodo)]
            niveles[nodo] = max(caminos) if caminos else 0

        # Agrupar nodos por nivel para distribuir la coordenada X uniformemente
        nodos_por_nivel = {}
        for nodo, lvl in niveles.items():
            nodos_por_nivel.setdefault(lvl, []).append(nodo)

        pos = {}
        for lvl, nodos in nodos_por_nivel.items():
            n = len(nodos)
            for i, nodo in enumerate(sorted(nodos, key=str)):
                # Coordenada X centrada para cada capa
                x = (i + 1) / (n + 1)
                # Coordenada Y basada en el nivel jerárquico
                y = lvl
                pos[nodo] = (x, y)

        # 4. Trazar aristas (líneas entre capas)
        edge_x = []
        edge_y = []
        for edge in H.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=1.5, color="#718096"),
            hoverinfo="none",
            mode="lines",
        )

        # 5. Colorear nodos según cotas, supremo e ínfimo
        destacados = elementos_destacados or {}
        supremo = destacados.get('supremo')
        infimo = destacados.get('infimo')
        cotas_sup = destacados.get('cotas_superiores', set())
        cotas_inf = destacados.get('cotas_inferiores', set())

        node_x = []
        node_y = []
        node_text = []
        node_colors = []

        for node in H.nodes():
            node_x.append(pos[node][0])
            node_y.append(pos[node][1])
            node_text.append(str(node))

            if node == supremo:
                node_colors.append("#FF5722")      # 🔴 Supremo
            elif node == infimo:
                node_colors.append("#00BCD4")     # 🔵 Ínfimo
            elif node in cotas_sup:
                node_colors.append("#FFC107")    # 🟡 Cota Superior
            elif node in cotas_inf:
                node_colors.append("#8BC34A")    # 🟢 Cota Inferior
            else:
                node_colors.append("#D3D3D3")    # ⚪ Gris base

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            text=node_text,
            textposition="middle center",
            hoverinfo="text",
            marker=dict(
                size=42,
                color=node_colors,
                line=dict(width=0),
            ),
            textfont=dict(size=12, color="#2D3748", family="Arial", weight="bold"),
        )

        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode="closest",
                margin=dict(b=20, l=20, r=20, t=20),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=550,
            ),
        )

        return fig