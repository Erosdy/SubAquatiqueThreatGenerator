import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import pygame
import sys
import threading
import math
import random

def compute_growth(progress, mode, exp_base, exp_switch, a, b, k):
    progress = max(0.0, min(progress, 1.0))

    if mode == "linear":
        return progress

    elif mode == "sigmoïdal":
        # Sigmoïde centrée en h = exp_switch, pente contrôlée par b
        h = exp_switch
        slope = b  # pente (plus grand = plus raide)

        sigmoid = 1 / (1 + math.exp(-slope * (progress - h)))

        sigmoid_min = 1 / (1 + math.exp(slope * h))
        sigmoid_max = 1 / (1 + math.exp(-slope * (1 - h)))

        normalized = (sigmoid - sigmoid_min) / (sigmoid_max - sigmoid_min)

        linear_weight = a  # poids linéaire (0 à 1)
        result = linear_weight * progress + (1 - linear_weight) * normalized + k

        return max(0.0, min(result, 1.0))

    elif mode == "power":
        exponent = max(b, 1.01)
        return progress ** exponent


def run_pygame(background_color, color_a, color_b, color_change_start, color_transition_duration,
               growth_duration, max_radius, shape_type, initial_radius, fullscreen,
               growth_mode, exp_base, exp_switch, exp_a, exp_b, exp_k,
               use_gradient_bg, gradient_color_start, gradient_color_end, show_animals,
               bulle_speed_min, bulle_speed_max,
               bulle_delay_min_s, bulle_delay_max_s,
               poisson_delay_min_s, poisson_delay_max_s,
               poisson_speed_min, poisson_speed_max):

    pygame.init()

    screen_size = (1920, 1280)
    flags = pygame.FULLSCREEN if fullscreen else 0
    screen = pygame.display.set_mode(screen_size, flags)
    pygame.display.set_caption("Croissance de forme symétrique")


    clock = pygame.time.Clock()
    FPS = 60
    total_frames = int(growth_duration * FPS)
    color_change_start_frames = int(color_change_start * FPS)
    color_transition_frames = int(color_transition_duration * FPS)
    pause_frames = int(1 * FPS)

    # Convertir délais (s) -> frames
    bulle_spawn_wait_range = (int(bulle_delay_min_s * FPS), int(bulle_delay_max_s * FPS))
    poisson_spawn_wait_range = (int(poisson_delay_min_s * FPS), int(poisson_delay_max_s * FPS))
    poisson_speed_min, poisson_speed_max = sorted((poisson_speed_min, poisson_speed_max))

    radius = initial_radius
    timer = 0
    growing = False
    shrinking = False
    paused = False
    pause_counter = 0
    color = color_a
    idle = True
    running = True
    
    # Cache animaux pendant la croissance
    animals_hidden_during_growth = False
    
    # Marqueur en haut-gauche (bulle fixe)
    show_marker = True

    # === Chargement des sprites (robuste) ===
    poisson_path = r"\\calebasse\coupeau234\Bureau\perso\Thèse\Predators\Looming contents\Poisson.png"
    bulle_path   = r"\\calebasse\coupeau234\Bureau\perso\Thèse\Predators\Looming contents\Bulle.png"

    def load_image_safe(path, fallback_kind="bubble"):
        try:
            img = pygame.image.load(path).convert_alpha()
            return img
        except Exception:
            # Placeholder simple si l'image n'est pas trouvée
            if fallback_kind == "fish":
                surf = pygame.Surface((80, 40), pygame.SRCALPHA)
                pygame.draw.ellipse(surf, (200, 120, 60), (0, 5, 60, 30))
                pygame.draw.polygon(surf, (200, 120, 60), [(60, 20), (78, 10), (78, 30)])
                pygame.draw.circle(surf, (20, 20, 20), (18, 20), 3)  # œil
                return surf
            else:
                surf = pygame.Surface((36, 36), pygame.SRCALPHA)
                pygame.draw.circle(surf, (220, 220, 255, 200), (18, 18), 16)
                pygame.draw.circle(surf, (255, 255, 255, 220), (12, 12), 4)
                return surf

    poisson_img  = load_image_safe(poisson_path, "fish")
    bulle_img    = load_image_safe(bulle_path,   "bubble")

    # Mise à l’échelle des bulles (une seule fois, pour les perfs)
    bulle_img_small = pygame.transform.scale(
        bulle_img,
        (max(1, int(bulle_img.get_width() / 3)),
         max(1, int(bulle_img.get_height() / 3)))
    )

    poisson_w = poisson_img.get_width()

    # === Dégradé pré-calculé (perf) ===
    def make_vertical_gradient(size, c1, c2):
        surf = pygame.Surface(size).convert()
        w, h = size
        for y in range(h):
            ratio = y / max(1, h - 1)
            r = int(c1[0] + ratio * (c2[0] - c1[0]))
            g = int(c1[1] + ratio * (c2[1] - c1[1]))
            b = int(c1[2] + ratio * (c2[2] - c1[2]))
            pygame.draw.line(surf, (r, g, b), (0, y), (w, y))
        return surf

    bg_grad = make_vertical_gradient(screen_size, gradient_color_start, gradient_color_end) if use_gradient_bg else None

    # ---------- SPAWN POISSON HORS-ÉCRAN ----------
    def make_poisson():
        dir_ = random.choice([-1, 1])  # -1: vers la gauche, 1: vers la droite
        if dir_ == 1:
            # Part de la GAUCHE, hors écran
            x0 = random.randint(-poisson_w - 60, -20)
        else:
            # Part de la DROITE, hors écran
            x0 = random.randint(screen_size[0] + 20, screen_size[0] + poisson_w + 60)
        return {
            "x": x0,
            "y": random.randint(100, screen_size[1] - 100),
            "dir": dir_,
            "speed": random.uniform(2, 3),  # vitesse du poisson (tu peux exposer aussi si tu veux)
            "osc_offset": random.uniform(0, 2 * math.pi)
        }

    # === Listes d’animaux ===
    poissons = [make_poisson()]  # 1 poisson au départ

    # Bulles indépendantes : chaque bulle a son état (alive/delay, vitesse, position)
    max_bulles = 3

    bulles = []
    for _ in range(max_bulles):
        # Démarrage échelonné : pas toutes visibles d’un coup
        bulles.append({
            "x": random.randint(100, screen_size[0] - 100),
            "y": screen_size[1],  # spawn depuis le bas
            "speed": random.uniform(bulle_speed_min, bulle_speed_max),
            "osc_offset": random.uniform(0, 2 * math.pi),
            "alive": False,  # certaines attendent avant d'apparaître
            "delay": random.randint(*bulle_spawn_wait_range)
        })

    # Poissons : délai de réapparition (en frames)
    max_poissons = 10
    poisson_spawn_delay = 0

    while running:
        # Fond
        if bg_grad is not None:
            screen.blit(bg_grad, (0, 0))
        else:
            screen.fill(background_color)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    growing = True
                    shrinking = False
                    paused = False
                    idle = False
                    radius = initial_radius
                    timer = 0
                    pause_counter = 0
                    animals_hidden_during_growth = True  # cache animaux pendant croissance
                    show_marker = False
                elif event.key == pygame.K_r:
                    growing = False
                    shrinking = False
                    paused = False
                    idle = True
                    radius = initial_radius
                    timer = 0
                    pause_counter = 0
                    color = color_a
                    animals_hidden_during_growth = False  # réaffiche si reset
                    show_marker = True

        # ======= ANIMAUX : MISE À JOUR (toujours) =======
        # --- POISSONS ---
        new_poissons = []
        for p in poissons:
            p["x"] += p["dir"] * p["speed"]
            p["y"] += math.sin(p["x"] * 0.05 + p["osc_offset"]) * 0.5

            # On garde tant que le poisson n'a pas complètement quitté l'écran
            if (-poisson_w <= p["x"] <= screen_size[0]):
                new_poissons.append(p)
            elif (screen_size[0] < p["x"] <= screen_size[0] + poisson_w) and p["dir"] == 1:
                new_poissons.append(p)
            elif (-poisson_w <= p["x"] < 0) and p["dir"] == -1:
                new_poissons.append(p)
            else:
                # sorti -> programme un respawn différé
                poisson_spawn_delay = random.randint(*poisson_spawn_wait_range)

        poissons = new_poissons

        if poisson_spawn_delay > 0:
            poisson_spawn_delay -= 1
        else:
            if len(poissons) < max_poissons:
                poissons.append(make_poisson())

        # --- BULLES (indépendantes) ---
        for b in bulles:
            if b["alive"]:
                # mouvement
                b["y"] -= b["speed"]
                b["x"] += math.sin(b["y"] * 0.03 + b["osc_offset"]) * 0.3

                # sortie par le haut -> passe en attente avec délai aléatoire
                if b["y"] < -50:
                    b["alive"] = False
                    b["delay"] = random.randint(*bulle_spawn_wait_range)
            else:
                # en attente : décrémente le timer
                if b["delay"] > 0:
                    b["delay"] -= 1
                else:
                    # respawn avec nouveaux paramètres
                    b["alive"] = True
                    b["x"] = random.randint(100, screen_size[0] - 100)
                    b["y"] = screen_size[1]
                    b["speed"] = random.uniform(bulle_speed_min, bulle_speed_max)
                    b["osc_offset"] = random.uniform(0, 2 * math.pi)

        # ======= AFFICHAGE DES ANIMAUX (seulement si autorisés) =======
        if show_animals and not animals_hidden_during_growth:
            # Affichage poissons
            for p in poissons:
                flipped = pygame.transform.flip(poisson_img, p["dir"] < 0, False)
                screen.blit(flipped, (int(p["x"]), int(p["y"])))

            # Affichage bulles (seulement les vivantes)
            for b in bulles:
                if b["alive"]:
                    screen.blit(bulle_img_small, (int(b["x"]), int(b["y"])))

        # ======= ANIMATION DE LA FORME =======
        if growing:
            if radius < max_radius:
                progress = timer / total_frames
                growth_factor = compute_growth(progress, growth_mode, exp_base, exp_switch, exp_a, exp_b, exp_k)
                radius = initial_radius + (max_radius - initial_radius) * growth_factor
            else:
                radius = max_radius
                growing = False
                paused = True
            if timer < color_change_start_frames:
                color = color_a
            elif timer < (color_change_start_frames + color_transition_frames):
                t = (timer - color_change_start_frames) / color_transition_frames
                color = tuple(int(color_a[i] + (color_b[i] - color_a[i]) * t) for i in range(3))
            else:
                color = color_b
            timer += 1
        elif paused:
            pause_counter += 1
            if pause_counter >= pause_frames:
                paused = False
                shrinking = True
                timer = total_frames
        elif shrinking:
            if radius > initial_radius:
                progress = timer / total_frames
                growth_factor = compute_growth(progress, growth_mode, exp_base, exp_switch, exp_a, exp_b, exp_k)
                radius = initial_radius + (max_radius - initial_radius) * growth_factor
            else:
                radius = initial_radius
                shrinking = False
                idle = True
                animals_hidden_during_growth = False  # réaffiche animaux quand fini
            if timer >= color_change_start_frames:
                color = color_b
            elif timer >= color_change_start_frames - color_transition_frames:
                t = (color_change_start_frames - timer) / color_transition_frames
                t = max(0.0, min(t, 1.0))
                color = tuple(int(color_b[i] + (color_a[i] - color_b[i]) * t) for i in range(3))
            else:
                color = color_a
            timer -= 1

        # Dessin de la forme
        if not idle:
            center = screen.get_rect().center   # ← au lieu d'utiliser screen_size
            if shape_type == "circle":
                pygame.draw.circle(screen, color, center, int(radius))
            elif shape_type == "square":
                side = int(radius) * 2
                rect = pygame.Rect(0, 0, side, side)
                rect.center = center
                pygame.draw.rect(screen, color, rect)
                
        # Marqueur haut-gauche (bulle fixe)
        if show_marker:
            marker_x = 10  # marge gauche
            marker_y = 10  # marge haut
            screen.blit(bulle_img_small, (marker_x, marker_y))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paramètres vidéo")
        self.fullscreen = tk.BooleanVar(value=False)

        self.bg_color = (200, 200, 200)
        self.use_gradient_bg = tk.BooleanVar(value=True)
        self.gradient_color_start = (242, 242, 242)
        self.gradient_color_end = (217, 217, 217)
        self.color_a = (255, 255, 255)
        self.color_b = (0, 0, 0)
        self.growth_duration = tk.DoubleVar(value=5.0)
        self.color_change_start = tk.DoubleVar(value=2.5)  # Quand la transition commence
        self.color_transition_duration = tk.DoubleVar(value=2.0)  # Combien de temps dure la transition
        self.max_radius = tk.IntVar(value=290)
        self.initial_radius = tk.IntVar(value=10)
        self.shape_type = tk.StringVar(value="circle")

        self.growth_mode = tk.StringVar(value="linear")
        self.exp_base = tk.DoubleVar(value=2.0)
        self.exp_switch = tk.DoubleVar(value=0.8)
        self.exp_a = tk.DoubleVar(value=0.3)
        self.exp_b = tk.DoubleVar(value=50.0)
        self.exp_k = tk.DoubleVar(value=0.0)
        
        self.show_animals = tk.BooleanVar(value=True)

        # --- Nouveaux paramètres exposés dans l'UI ---
        # Vitesses des bulles
        self.bulle_speed_min = tk.DoubleVar(value=3.0)
        self.bulle_speed_max = tk.DoubleVar(value=8.0)
        # Vitesses poissons (min/max)
        self.poisson_speed_min = tk.DoubleVar(value=2.0)
        self.poisson_speed_max = tk.DoubleVar(value=3.0)
        # Délais (en secondes) pour bulles et poissons
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
        self.color_a_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.color_a))
        self.color_b_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.color_b))
        
        add_color("Couleur du fond", self.choose_bg_color, self.bg_color_preview)
        add_color("Couleur A (départ)", self.choose_color_a, self.color_a_preview)
        add_color("Couleur B (finale)", self.choose_color_b, self.color_b_preview)
        
        tk.Checkbutton(self, text="Utiliser un fond dégradé", variable=self.use_gradient_bg).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        
        self.gradient_start_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.gradient_color_start))
        self.gradient_end_preview = tk.Canvas(self, width=20, height=20, bg=self.rgb_to_hex(self.gradient_color_end))
        
        add_color("Dégradé - Couleur 1", self.choose_gradient_start, self.gradient_start_preview)
        add_color("Dégradé - Couleur 2", self.choose_gradient_end, self.gradient_end_preview)

        add_entry("Début transition couleur (s)", self.color_change_start)
        add_entry("Durée transition couleur (s)", self.color_transition_duration)
        add_entry("Durée de croissance totale (s)", self.growth_duration)
        add_entry("Taille maximale", self.max_radius)
        add_entry("Taille initiale", self.initial_radius)

        tk.Label(self, text="Forme").grid(row=row, column=0, sticky="w")
        shape_menu = ttk.Combobox(self, textvariable=self.shape_type, values=["circle", "square"], state="readonly")
        shape_menu.grid(row=row, column=1)
        row += 1

        tk.Label(self, text="Mode de croissance").grid(row=row, column=0, sticky="w")
        mode_menu = ttk.Combobox(self, textvariable=self.growth_mode, values=["linear", "sigmoïdal", "power"], state="readonly")
        mode_menu.grid(row=row, column=1)
        row += 1

        add_entry("Poids linéaire (a)", self.exp_a)
        add_entry("Pente sigmoïde (b)", self.exp_b)
        add_entry("Position switch (h)", self.exp_switch)
        add_entry("Offset (k)", self.exp_k)

        tk.Checkbutton(self, text="Plein écran", variable=self.fullscreen).grid(row=row, column=0, columnspan=2, sticky="w")
        row += 1
        
        tk.Checkbutton(self, text="Afficher bulles et poissons", variable=self.show_animals).grid(row=row, column=0, columnspan=2)
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

        tk.Button(self, text="Lancer la vidéo", command=self.launch_pygame).grid(row=row, column=0, columnspan=3, pady=10)

        # Mise à jour de la courbe à chaque changement
        self.growth_mode.trace_add("write", lambda *args: self.draw_curve(self.exp_switch.get()))
        self.exp_a.trace_add("write", lambda *args: self.draw_curve(self.exp_switch.get()))
        self.exp_b.trace_add("write", lambda *args: self.draw_curve(self.exp_switch.get()))
        self.exp_k.trace_add("write", lambda *args: self.draw_curve(self.exp_switch.get()))
        self.exp_switch.trace_add("write", lambda *args: self.draw_curve(self.exp_switch.get()))

        self.draw_curve()

    def draw_curve(self, moving_point_progress=0.8, *args):
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
        mode = self.growth_mode.get()
        a = self.exp_a.get()
        b = self.exp_b.get()
        k = self.exp_k.get()
        h = self.exp_switch.get()
    
        steps = 100
        points = []
    
        for i in range(steps + 1):
            progress = i / steps
            y = compute_growth(progress, mode, 0, h, a, b, k)
            x_px = padding_left + progress * plot_width
            y_px = height - padding_bottom - y * plot_height
            points.append((x_px, y_px))
    
        # Tracer la courbe
        for i in range(len(points) - 1):
            self.curve_canvas.create_line(*points[i], *points[i + 1], fill="blue", width=2)
    
        # Tracer le point rouge mobile (optionnel)
        mp_x = padding_left + moving_point_progress * plot_width
        mp_y_val = compute_growth(moving_point_progress, mode, 0, h, a, b, k)
        mp_y = height - padding_bottom - mp_y_val * plot_height
        r = 4
        self.curve_canvas.create_oval(mp_x - r, mp_y - r, mp_x + r, mp_y + r, fill="red")
    
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
            self.curve_canvas.create_text(x, height - padding_bottom + 15, text=f"{i/10:.1f}", font=("Arial", 8))
    
        # Graduations Y (0 à 1)
        for i in range(0, 6):
            y = height - padding_bottom - i * plot_height / 5
            self.curve_canvas.create_line(padding_left - 5, y, padding_left, y)
            self.curve_canvas.create_text(padding_left - 10, y, text=f"{i/5:.1f}", font=("Arial", 8), anchor="e")

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
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.color_a))
        if color[0]:
            self.color_a = tuple(int(c) for c in color[0])
            self.color_a_preview.config(bg=self.rgb_to_hex(self.color_a))

    def choose_color_b(self):
        color = colorchooser.askcolor(initialcolor=self.rgb_to_hex(self.color_b))
        if color[0]:
            self.color_b = tuple(int(c) for c in color[0])
            self.color_b_preview.config(bg=self.rgb_to_hex(self.color_b))

    def launch_pygame(self):
        params = {
            "background_color": self.bg_color,
            "color_a": self.color_a,
            "color_b": self.color_b,
            "growth_duration": self.growth_duration.get(),
            "max_radius": self.max_radius.get(),
            "shape_type": self.shape_type.get(),
            "initial_radius": self.initial_radius.get(),
            "fullscreen": self.fullscreen.get(),
            "growth_mode": self.growth_mode.get(),
            "exp_base": self.exp_base.get(),
            "exp_switch": self.exp_switch.get(),
            "exp_a": self.exp_a.get(),
            "exp_b": self.exp_b.get(),
            "exp_k": self.exp_k.get(),
            "color_change_start": self.color_change_start.get(),
            "color_transition_duration": self.color_transition_duration.get(),
            "use_gradient_bg": self.use_gradient_bg.get(),
            "gradient_color_start": self.gradient_color_start,
            "gradient_color_end": self.gradient_color_end,
            "show_animals": self.show_animals.get(),

            # Nouveaux paramètres passés au moteur pygame :
            "bulle_speed_min": self.bulle_speed_min.get(),
            "bulle_speed_max": self.bulle_speed_max.get(),
            "bulle_delay_min_s": self.bulle_delay_min_s.get(),
            "bulle_delay_max_s": self.bulle_delay_max_s.get(),
            "poisson_delay_min_s": self.poisson_delay_min_s.get(),
            "poisson_delay_max_s": self.poisson_delay_max_s.get(),
            "poisson_speed_min": self.poisson_speed_min.get(),
            "poisson_speed_max": self.poisson_speed_max.get()
        }
        threading.Thread(target=run_pygame, kwargs=params, daemon=True).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
