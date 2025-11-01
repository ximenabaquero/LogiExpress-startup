import os
import threading
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
from src.security.encrypted_env import load_secret              # gestor de API key cifrada
from src.graph.downloader import download_city_graph            # descarga/caché de OSMnx
from src.graph.builder import build_simple_graph                 # construye grafo simplificado (distance|duration)
from src.graph.visualizer import plot_route_explore_compliant    # renderer GeoPandas.explore compliant
from src.routing.compute_routes_async import (                    # cálculo asíncrono de ruta
    compute_route_async,
    RouteResult,
)
from src.algorithms.dijkstra import dijkstra                     # Dijkstra propio
from src.api.google_maps import (                                # geocoder Google + sanity check
    get_coordinates_from_address,
    google_key_sanity_check,
)


class RouteGUI:
    """Interfaz gráfica para construir grafo, calcular ruta y visualizarla."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("LogiExpress — City Routing GUI")

        # Estado interno
        self.google_api_key = None
        self.google_maps_api_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        self.G = None               # grafo OSMnx completo (MultiDiGraph)
        self.graph_simple = None    # grafo simplificado {u:[(v,weight),...]}
        self.last_result: RouteResult | None = None

        # —— UI principal ——
        container = ttk.Frame(root, padding=12)
        container.pack(fill="both", expand=True)

        # Fila 1: Ciudad + modo de peso + botones grafo/API key
        row1 = ttk.Frame(container)
        row1.pack(fill="x", pady=(0, 8))

        ttk.Label(row1, text="City / Place:").pack(side="left")
        self.place_var = tk.StringVar(value="Bogotá, Colombia")
        ttk.Entry(row1, textvariable=self.place_var, width=36).pack(side="left", padx=6)

        ttk.Label(row1, text="Weight:").pack(side="left", padx=(12, 0))
        self.weight_mode_var = tk.StringVar(value="distance")  # "distance" | "duration"
        ttk.OptionMenu(row1, self.weight_mode_var, "distance", "distance", "duration").pack(side="left")

        ttk.Button(row1, text="Load API Key", command=self._load_key).pack(side="right")
        ttk.Button(row1, text="Build/Load Graph", command=self.on_build_graph).pack(side="right", padx=(0, 8))

        # Estado visual de API key
        row_status = ttk.Frame(container)
        row_status.pack(fill="x", pady=(0, 8))
        self.api_status_var = tk.StringVar(value="API key: ❌ no cargada")
        ttk.Label(row_status, textvariable=self.api_status_var).pack(side="left")

        # Fila 2: Origen/Destino
        row2 = ttk.Frame(container)
        row2.pack(fill="x", pady=(0, 8))

        ttk.Label(row2, text="Origin:").grid(row=0, column=0, sticky="w")
        self.origin_var = tk.StringVar(value="Diagonal 81F # 72C-1, Bogotá, Colombia")
        ttk.Entry(row2, textvariable=self.origin_var, width=60).grid(row=0, column=1, padx=6)

        ttk.Label(row2, text="Destination:").grid(row=1, column=0, sticky="w", pady=(6, 0))
        self.dest_var = tk.StringVar(value="Diagonal 57C Sur # 62-60, Bogotá, Colombia")
        ttk.Entry(row2, textvariable=self.dest_var, width=60).grid(row=1, column=1, padx=6, pady=(6, 0))

        # Fila 3: Acciones
        row3 = ttk.Frame(container)
        row3.pack(fill="x", pady=(0, 8))
        self.btn_compute = ttk.Button(row3, text="Compute Route (Dijkstra)", command=self.on_compute_route)
        self.btn_compute.pack(side="left")
        ttk.Button(row3, text="Open Map", command=self.on_open_map).pack(side="left", padx=8)
        ttk.Button(row3, text="Save As...", command=self.on_save_as).pack(side="left")

        # Consola/Log
        ttk.Label(container, text="Log:").pack(anchor="w")
        self.log = tk.Text(container, height=14)
        self.log.pack(fill="both", expand=True)

        # Enlaces de estado dinámico
        self.weight_mode_var.trace_add("write", lambda *args: self._refresh_buttons())
        self._refresh_buttons()

        self._log("[INFO] Ready. Load API key, build graph, and compute route.")

    # ——— Helpers de UI ———
    def _log(self, msg: str):
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.root.update_idletasks()

    def _set_busy(self, busy: bool):
        self.root.config(cursor="watch" if busy else "")
        self.btn_compute.config(state=("disabled" if busy else "normal"))
        self.root.update_idletasks()

    def _refresh_buttons(self):
        """Habilita/deshabilita Compute según modo y key. Actualiza estado visual."""
        needs_key = (self.weight_mode_var.get() == "duration")
        has_key = bool(self.google_api_key)
        self.btn_compute.config(state=("normal" if (has_key or not needs_key) else "disabled"))
        self.api_status_var.set(f"API key: {'✅ cargada' if has_key else '❌ no cargada'}")

    def _run_async(self, target, *args, **kwargs):
        t = threading.Thread(target=target, args=args, kwargs=kwargs, daemon=True)
        t.start()

    # ——— Acciones ———
    def _load_key(self):
        """Carga/descifra la API key y realiza un sanity check contra Google."""
        try:
            # Usa tu esquema cifrado; si falta, pedirá input oculto y la guardará
            self.google_api_key = load_secret()

            # Sanity check para validar si la api key ya esta cargada
            ok = google_key_sanity_check(self.google_api_key)
            if not ok:
                self.google_api_key = None
                self.api_status_var.set("API key: ❌ inválida o sin permisos/billing")
                messagebox.showerror(
                    "API key inválida",
                    "La API key de Google no pasó el chequeo de geocodificación.\n"
                    "- Verifica que Geocoding/Places estén habilitadas\n"
                    "- Que el billing esté activo\n"
                    "- Y que las restricciones (IP/HTTP) no bloqueen este script."
                )
            else:
                self.api_status_var.set("API key: ✅ cargada")
                self._log("[INFO] API key validada con éxito.")

        except Exception as e:
            self.google_api_key = None
            self.api_status_var.set("API key: ❌ no cargada")
            messagebox.showerror("Error", f"No se pudo cargar la API key:\n{e}")
        finally:
            self._refresh_buttons()

    def on_build_graph(self):
        self._run_async(self._build_graph_async)

    def _build_graph_async(self):
        try:
            self._set_busy(True)
            place = self.place_var.get().strip()
            self._log(f"[INFO] Descargando/cargando grafo para: {place} ...")

            # Descarga con caché
            self.G = download_city_graph(place, network_type="drive", use_cache=True, max_age_days=30)
            self._log(f"[INFO] Grafo: {self.G.number_of_nodes():,} nodos, {self.G.number_of_edges():,} aristas")

            weight_mode = self.weight_mode_var.get()
            self._log(f"[INFO] Construyendo grafo simplificado (weight={weight_mode}) ...")

            # build_simple_graph soporta 'duration' (si pasa API) o 'distance'
            try:
                self.graph_simple = build_simple_graph(
                    google_maps_api_url=self.google_maps_api_url,
                    google_api_key=(self.google_api_key or ""),
                    G=self.G,
                    weight_type=weight_mode,
                    sample_ratio=0.001,  # limita llamadas a API si 'duration'
                )
            except TypeError:
                self.graph_simple = build_simple_graph(self.G, weight_type=weight_mode)

            self._log("[INFO] Grafo simplificado listo.")
        except Exception as e:
            self._log("[ERROR] Falló la construcción del grafo.")
            self._log(traceback.format_exc())
            messagebox.showerror("Error", str(e))
        finally:
            self._set_busy(False)
            self._refresh_buttons()

    def on_compute_route(self):
        self._run_async(self._compute_route_async)

    def _compute_route_async(self):
        if not self.G or not self.graph_simple:
            messagebox.showwarning("Atención", "Primero construye/carga el grafo.")
            return

        # Si no hay API key, avisar y abortar
        if not self.google_api_key:
            messagebox.showwarning(
                "API key requerida",
                "Debes cargar la Google API key (Load API Key)."
            )
            return

        try:
            self._set_busy(True)
            origin_text = self.origin_var.get().strip()
            dest_text = self.dest_var.get().strip()
            weight_mode = self.weight_mode_var.get()

            # Ejecuta el cómputo asíncrono en un event loop local (sin bloquear la UI)
            import asyncio
            result: RouteResult = asyncio.run(
                compute_route_async(
                    G=self.G,
                    graph_simple=self.graph_simple,
                    dijkstra_fn=dijkstra,
                    get_coordinates_from_address=get_coordinates_from_address,
                    origin_text=origin_text,
                    dest_text=dest_text,
                    google_api_key=(self.google_api_key or ""),
                    weight_type=weight_mode,
                    timeout_seconds=30,
                )
            )

            # Guardar estado y loguear
            self.last_result = result
            if result.weight_type == "distance":
                self._log(f"[RESULT] Distancia más corta: {result.total_cost:.2f} m — {len(result.path_nodes)} nodos")
            else:
                self._log(f"[RESULT] Ruta más rápida: {result.total_cost/60:.2f} min — {len(result.path_nodes)} nodos")

            # Render (GeoPandas.explore compliant, SIN fijar zoom por defecto)
            html_path = plot_route_explore_compliant(
                self.G,
                result.path_nodes,
                save_path="data/outputs/route_map.html",
                show_network=False,  # True si se quiere sombrear red alrededor del trayecto
            )
            self._log(f"[INFO] Mapa interactivo guardado en: {html_path}")

        except Exception as e:
            self._log("[ERROR] Falló el cálculo de ruta.")
            self._log(traceback.format_exc())
            messagebox.showerror("Error", str(e))
        finally:
            self._set_busy(False)

    def on_open_map(self):
        try:
            html_path = "data/outputs/route_map.html"
            if not os.path.exists(html_path):
                messagebox.showinfo("Info", "Primero calcula una ruta (no existe el HTML).")
                return
            webbrowser.open_new_tab(os.path.abspath(html_path))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_save_as(self):
        try:
            html_path = "data/outputs/route_map.html"
            if not os.path.exists(html_path):
                messagebox.showinfo("Info", "No hay mapa generado aún.")
                return
            dest = filedialog.asksaveasfilename(
                defaultextension=".html",
                filetypes=[("HTML", "*.html")],
                initialfile="route_map.html",
                title="Guardar mapa como"
            )
            if dest:
                with open(html_path, "rb") as src, open(dest, "wb") as dst:
                    dst.write(src.read())
                self._log(f"[INFO] Mapa guardado como: {dest}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def run_app():
    root = tk.Tk()
    # (Opcional) aplicar theme si lo tienes (p. ej., "azure.tcl")
    try:
        root.tk.call("source", "azure.tcl")
        ttk.Style().theme_use("azure")
    except Exception:
        pass
    RouteGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
