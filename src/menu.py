import threading
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

from animation import run
from src.entities.threat import Shape
from src.growth_equation import compute_growth, GrowthMode


class Menu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paramètres vidéo")
        self.fullscreen = tk.BooleanVar(value=False)

        self.bg_color = (200, 200, 200)
        self.use_gradient_bg = tk.BooleanVar(value=True)
        self.gradient_color_start = (242, 242, 242)
        self.gradient_color_end = (217, 217, 217)
        self.color_begin = (255, 255, 255)
        self.color_end = (0, 0, 0)
        self.transition_begin = tk.DoubleVar(value=0.2)
        self.transition_end = tk.DoubleVar(value=0.8)
        self.max_radius = tk.IntVar(value=500)
        self.initial_radius = tk.IntVar(value=10)
        self.shape_type = tk.StringVar(value=Shape.CIRCLE.value)

        self.growth_mode = tk.StringVar(value="linear")
        self.end_growth = tk.DoubleVar(value=0.45)
        self.start_degrowth = tk.DoubleVar(value=0.55)
        self.animation_duration = tk.DoubleVar(value=3)

        self.show_animals = tk.BooleanVar(value=True)
        self.bulle_speed_min = tk.DoubleVar(value=3.0)
        self.bulle_speed_max = tk.DoubleVar(value=8.0)
        self.poisson_speed_min = tk.DoubleVar(value=2.0)
        self.poisson_speed_max = tk.DoubleVar(value=3.0)

        self.bulle_delay_min_s = tk.DoubleVar(value=0.25)
        self.bulle_delay_max_s = tk.DoubleVar(value=3.0)
        self.poisson_delay_min_s = tk.DoubleVar(value=0.5)
        self.poisson_delay_max_s = tk.DoubleVar(value=2.0)

        row = 0

        def add_entry(label, var):
            nonlocal row
            tk.Label(self, text=label).grid(row=row, column=0, sticky="w")
            tk.Entry(self, textvariable=var).grid(row=row, column=1)
            row += 1

        def add_color(label, command, preview):
            nonlocal row
            tk.Label(self, text=label).grid(row=row, column=0, sticky="w")
            tk.Button(self, text="Choisir", command=command).grid(row=row, column=1)
            preview.grid(row=row, column=2)
            row += 1

        self.bg_color_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.bg_color))
        self.color_a_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.color_begin))
        self.color_b_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.color_end))

        add_color("Couleur du fond", self.choose_bg_color, self.bg_color_preview)
        add_color("Couleur A (départ)", self.choose_color_a, self.color_a_preview)
        add_color("Couleur B (finale)", self.choose_color_b, self.color_b_preview)

        tk.Checkbutton(self, text="Utiliser un fond dégradé", variable=self.use_gradient_bg).grid(row=row, column=0,
                                                                                                  columnspan=2,
                                                                                                  sticky="w")
        row += 1

        self.gradient_start_preview = tk.Canvas(self, width=20, height=20,
                                                bg=self.rgb_to_hex(self.gradient_color_start))
        self.gradient_end_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.gradient_color_end))

        add_color("Dégradé - Couleur 1", self.choose_gradient_start, self.gradient_start_preview)
        add_color("Dégradé - Couleur 2", self.choose_gradient_end, self.gradient_end_preview)

        add_entry("Taille maximale", self.max_radius)
        add_entry("Taille initiale", self.initial_radius)

        tk.Label(self, text="Forme").grid(row=row, column=0, sticky="w")
        shape_menu = ttk.Combobox(self, textvariable=self.shape_type, values=[shape.value for shape in Shape],
                                  state="readonly")
        shape_menu.grid(row=row, column=1)
        row += 1

        tk.Label(self, text="Mode de croissance").grid(row=row, column=0, sticky="w")
        mode_menu = ttk.Combobox(self, textvariable=self.growth_mode, values=[mode.value for mode in GrowthMode],
                                 state="readonly")
        mode_menu.grid(row=row, column=1)
        row += 1

        add_entry("Fin de croissance (a)", self.end_growth)
        add_entry("Début de décroissance (b)", self.start_degrowth)
        add_entry("Durée de l'animation (en seconde)", self.animation_duration)
        add_entry("Début de la transition de couleur", self.transition_begin)
        add_entry("Fin de la transition de couleur", self.transition_end)


        tk.Checkbutton(self, text="Plein écran", variable=self.fullscreen).grid(row=row, column=0, columnspan=2,
                                                                                sticky="w")
        row += 1

        tk.Checkbutton(self, text="Afficher bulles et poissons", variable=self.show_animals).grid(row=row, column=0,
                                                                                                  columnspan=2)
        row += 1

        # --- Nouveaux réglages UI ---
        tk.Label(self, text="Vitesses bulles (min/max)").grid(row=row, column=0, sticky="w")
        tk.Entry(self, textvariable=self.bulle_speed_min, width=8).grid(row=row, column=1, sticky="w")
        tk.Entry(self, textvariable=self.bulle_speed_max, width=8).grid(row=row, column=2, sticky="w")
        row += 1

        tk.Label(self, text="Vitesse poissons (min/max)").grid(row=row, column=0, sticky="w")
        tk.Entry(self, textvariable=self.poisson_speed_min, width=8).grid(row=row, column=1, sticky="w")
        tk.Entry(self, textvariable=self.poisson_speed_max, width=8).grid(row=row, column=2, sticky="w")
        row += 1

        tk.Label(self, text="Délai bulles (min/max) en s").grid(row=row, column=0, sticky="w")
        tk.Entry(self, textvariable=self.bulle_delay_min_s, width=8).grid(row=row, column=1, sticky="w")
        tk.Entry(self, textvariable=self.bulle_delay_max_s, width=8).grid(row=row, column=2, sticky="w")
        row += 1

        tk.Label(self, text="Délai poissons (min/max) en s").grid(row=row, column=0, sticky="w")
        tk.Entry(self, textvariable=self.poisson_delay_min_s, width=8).grid(row=row, column=1, sticky="w")
        tk.Entry(self, textvariable=self.poisson_delay_max_s, width=8).grid(row=row, column=2, sticky="w")
        row += 1

        # Canvas pour affichage courbe
        self.curve_canvas = tk.Canvas(self, width=300, height=180, bg="white")
        self.curve_canvas.grid(row=row, column=0, columnspan=3, pady=10)
        row += 1

        tk.Button(self, text="Lancer la vidéo", command=self.launch_pygame).grid(row=row, column=0, columnspan=3,
                                                                                 pady=10)

        # Mise à jour de la courbe à chaque changement
        self.growth_mode.trace_add("write", self.draw_curve)
        self.end_growth.trace_add("write", self.draw_curve)
        self.start_degrowth.trace_add("write", self.draw_curve)
        self.transition_begin.trace_add("write", self.draw_curve)
        self.transition_end.trace_add("write", self.draw_curve)

        self.draw_curve()

    def draw_curve(self, *args):
        self.curve_canvas.delete("all")

        # Récupération des dimensions réelles du canvas
        width = int(self.curve_canvas["width"])
        height = int(self.curve_canvas["height"])

        # Marges
        padding_left = 40
        padding_right = 20
        padding_top = 20
        padding_bottom = 30

        # Zone de tracé réelle
        plot_width = width - padding_left - padding_right
        plot_height = height - padding_top - padding_bottom

        # Paramètres de la courbe
        mode = GrowthMode(self.growth_mode.get())
        a = self.end_growth.get()
        b = self.start_degrowth.get()
        transition_start = self.transition_begin.get()
        transition_end = self.transition_end.get()

        # Tracer les lignes horizontales
        y_transition_start = height - padding_bottom - transition_start * plot_height
        y_transition_end = height - padding_bottom - transition_end * plot_height


        steps = 100
        points = []
        last_x = None
        last_y = None

        for i in range(steps + 1):
            progress = i / steps
            y = compute_growth(progress, mode, a=a, b=b)
            x_px = padding_left + progress * plot_width
            y_px = height - padding_bottom - y * plot_height
            points.append((x_px, y_px))
        
            # Vérifier les intersections
            if last_y is not None:
                current_y_normalized = y
                last_y_normalized = last_y

                # Intersection avec transition_start
                if ((last_y_normalized - transition_start) * (current_y_normalized - transition_start) <= 0 and
                    last_y_normalized != current_y_normalized):
                    ratio = (transition_start - last_y_normalized) / (current_y_normalized - last_y_normalized)
                    x_intersect = last_x + (x_px - last_x) * ratio
                    self.curve_canvas.create_oval(
                        x_intersect - 4, y_transition_start - 4,
                        x_intersect + 4, y_transition_start + 4,
                        fill="red", outline="darkred"
                    )

                # Intersection avec transition_end
                if ((last_y_normalized - transition_end) * (current_y_normalized - transition_end) <= 0 and
                    last_y_normalized != current_y_normalized):
                    ratio = (transition_end - last_y_normalized) / (current_y_normalized - last_y_normalized)
                    x_intersect = last_x + (x_px - last_x) * ratio
                    self.curve_canvas.create_oval(
                        x_intersect - 4, y_transition_end - 4,
                        x_intersect + 4, y_transition_end + 4,
                        fill="red", outline="darkblue"
                    )

            last_x = x_px
            last_y = y

        # Tracer la courbe
        for i in range(len(points) - 1):
            self.curve_canvas.create_line(*points[i], *points[i + 1], fill="blue", width=2)

            # Axe X
            self.curve_canvas.create_line(
                padding_left, height - padding_bottom,
                width - padding_right, height - padding_bottom,
                arrow=tk.LAST
            )

            # Axe Y
            self.curve_canvas.create_line(
                padding_left, height - padding_bottom,
                padding_left, padding_top,
                arrow=tk.LAST
            )

            # Graduations X (0 à 1)
            for i in range(0, 11):
                x = padding_left + i * plot_width / 10
                self.curve_canvas.create_line(x, height - padding_bottom, x, height - padding_bottom + 5)
                self.curve_canvas.create_text(x, height - padding_bottom + 15, text=f"{i / 10:.1f}", font=("Arial", 8))

            # Graduations Y (0 à 1)
            for i in range(0, 6):
                y = height - padding_bottom - i * plot_height / 5
                self.curve_canvas.create_line(padding_left - 5, y, padding_left, y)
                self.curve_canvas.create_text(padding_left - 10, y, text=f"{i / 5:.1f}", font=("Arial", 8), anchor="e")

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

    def choose_bg_color(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.bg_color))
        if color[0]:
            self.bg_color = tuple(int(c) for c in color[0])
            self.bg_color_preview.config(bg=self.rgb_to_hex(self.bg_color))

    def choose_gradient_start(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.gradient_color_start))
        if color[0]:
            self.gradient_color_start = tuple(int(c) for c in color[0])
            self.gradient_start_preview.config(bg=self.rgb_to_hex(self.gradient_color_start))

    def choose_gradient_end(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.gradient_color_end))
        if color[0]:
            self.gradient_color_end = tuple(int(c) for c in color[0])
            self.gradient_end_preview.config(bg=self.rgb_to_hex(self.gradient_color_end))

    def choose_color_a(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.color_begin))
        if color[0]:
            self.color_begin = tuple(int(c) for c in color[0])
            self.color_a_preview.config(bg=self.rgb_to_hex(self.color_begin))

    def choose_color_b(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.color_end))
        if color[0]:
            self.color_end = tuple(int(c) for c in color[0])
            self.color_b_preview.config(bg=self.rgb_to_hex(self.color_end))

    def launch_pygame(self):
        params = {
            "background_color": self.bg_color,
            "color_begin": self.color_begin,
            "color_end": self.color_end,
            "max_radius": self.max_radius.get(),
            "shape_type": Shape(self.shape_type.get()),
            "initial_radius": self.initial_radius.get(),
            "fullscreen": self.fullscreen.get(),
            "growth_mode": GrowthMode(self.growth_mode.get()),
            "animation_duration": self.animation_duration.get(),
            "end_growth": self.end_growth.get(),
            "start_degrowth": self.start_degrowth.get(),
            "show_animals": self.show_animals.get(),
            "bulle_speed_min": self.bulle_speed_min.get(),
            "bulle_speed_max": self.bulle_speed_max.get(),
            "bulle_delay_min_s": self.bulle_delay_min_s.get(),
            "bulle_delay_max_s": self.bulle_delay_max_s.get(),
            "poisson_delay_min_s": self.poisson_delay_min_s.get(),
            "poisson_delay_max_s": self.poisson_delay_max_s.get(),
            "poisson_speed_min": self.poisson_speed_min.get(),
            "poisson_speed_max": self.poisson_speed_max.get()
        }
        threading.Thread(target=run, kwargs=params, daemon=True).start()