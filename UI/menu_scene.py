"""Animated nature background for the main menu."""
import math
import random
import pygame

# --- Sky palette (soft afternoon) ---
_SKY_TOP   = (80, 125, 195)
_SKY_MID   = (148, 192, 232)
_SKY_HORIZ = (228, 212, 182)

# (scroll_rate, rgb, wave_amp_frac, wave_freq, wave_phase, base_y_frac)
_HILL_DEFS = [
    (0.04, (104, 144, 104), 0.055, 0.0022, 0.0,  0.67),
    (0.10, (78,  118,  78), 0.060, 0.0032, 1.9,  0.74),
    (0.18, (57,   96,  57), 0.065, 0.0048, 3.7,  0.80),
    (0.28, (42,   75,  42), 0.050, 0.0070, 5.3,  0.87),
]

_PETAL_COLORS = [
    (178, 218, 142),
    (230, 202, 138),
    (218, 172, 128),
    (240, 196, 175),
]

_MENU_SPECIES = [
    "robin", "sparrow", "blue_jay", "cardinal",
    "swallow", "crane", "heron", "eagle",
]
_BIRD_COUNT = 9


def _lerp_color(a, b, t):
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )


class _MenuBird:
    """Minimal bird stand-in for menu background animation."""
    IS_GROUND = False

    def __init__(self, x, y, species_cls):
        self.x   = float(x)
        self.y   = float(y)
        self.vx  = random.uniform(28, 65)
        self.state       = "flying"
        self._wing_phase = random.uniform(0, math.pi * 2)
        self.facing      = 1
        self.SPECIES      = species_cls.SPECIES
        self.BODY_COLOR   = species_cls.BODY_COLOR
        self.WING_COLOR   = species_cls.WING_COLOR
        self.BEAK_COLOR   = species_cls.BEAK_COLOR
        self.HEAD_COLOR   = species_cls.HEAD_COLOR
        self.ACCENT_COLOR = species_cls.ACCENT_COLOR
        self.W = species_cls.W
        self.H = species_cls.H


class MenuScene:
    def __init__(self, W, H):
        self.W = W
        self.H = H
        self._scroll = 0.0

        # Pre-render sky gradient
        self._sky = pygame.Surface((W, H))
        horizon = int(H * 0.62)
        for y in range(H):
            if y <= horizon:
                col = _lerp_color(_SKY_TOP, _SKY_MID, y / max(horizon, 1))
            else:
                col = _lerp_color(_SKY_MID, _SKY_HORIZ, (y - horizon) / max(H - horizon, 1))
            pygame.draw.line(self._sky, col, (0, y), (W, y))

        # Sun position (fixed, painted over sky)
        self._sun_x = int(W * 0.74)
        self._sun_y = int(H * 0.56)
        self._sun_glow = self._build_sun_glow()

        # Clouds — pre-rendered surfaces
        self._clouds = [self._new_cloud(random.uniform(0, W)) for _ in range(12)]

        # Wind particles
        self._particles = [self._new_particle(random.uniform(0, W)) for _ in range(50)]

        # Birds
        try:
            from birds import ALL_SPECIES as _all
            self._bird_classes = [c for c in _all if c.SPECIES in _MENU_SPECIES]
        except Exception:
            self._bird_classes = []
        self._birds = []
        for _ in range(_BIRD_COUNT):
            self._spawn_bird(random.uniform(0, W))

    # ------------------------------------------------------------------

    def _build_sun_glow(self):
        size = 180
        surf = pygame.Surface((size, size), pygame.SRCALPHA)
        cx = size // 2
        for r in range(90, 0, -6):
            a = int(22 * (1 - r / 90))
            pygame.draw.circle(surf, (255, 230, 150, a), (cx, cx), r)
        pygame.draw.circle(surf, (255, 242, 198), (cx, cx), 18)
        pygame.draw.circle(surf, (255, 255, 232), (cx, cx), 10)
        return surf

    def _new_cloud(self, x):
        w = random.randint(90, 230)
        h = max(w // 3, 22)
        speed = random.uniform(6, 24)
        y = random.uniform(self.H * 0.05, self.H * 0.38)
        alpha = random.randint(128, 205)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        c = (248, 252, 255)
        pygame.draw.ellipse(surf, (*c, alpha),      (0,     h // 3, w,       h * 2 // 3))
        pygame.draw.ellipse(surf, (*c, alpha - 22), (w // 5, 0,     w * 3 // 5, h * 3 // 4))
        if w > 140:
            pygame.draw.ellipse(surf, (*c, alpha - 38), (w // 2, h // 8, w * 2 // 5, h * 2 // 3))
        return {"x": float(x), "y": float(y), "surf": surf, "speed": speed, "w": w}

    def _new_particle(self, x):
        return {
            "x":      float(x),
            "y":      random.uniform(self.H * 0.35, self.H * 0.82),
            "vx":     random.uniform(12, 40),
            "vy":     random.uniform(-5, 5),
            "size":   random.choice([2, 2, 3, 3, 4]),
            "color":  random.choice(_PETAL_COLORS),
            "phase":  random.uniform(0, math.pi * 2),
            "life":   random.uniform(4, 14),
        }

    def _spawn_bird(self, x):
        if not self._bird_classes:
            return
        cls = random.choice(self._bird_classes)
        y = random.uniform(self.H * 0.06, self.H * 0.44)
        b = _MenuBird(x, y, cls)
        b.vx = random.uniform(30, 72)
        self._birds.append(b)

    # ------------------------------------------------------------------

    def update(self, dt):
        self._scroll += dt * 18

        for c in self._clouds:
            c["x"] += c["speed"] * dt
            if c["x"] > self.W + c["w"]:
                c["x"] = float(-c["w"] - random.randint(10, 90))

        for p in self._particles:
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt + math.sin(p["phase"]) * 0.35
            p["phase"] += dt * 1.8
            p["life"]  -= dt
            if p["life"] <= 0 or p["x"] > self.W + 10:
                p.update(self._new_particle(-8.0))

        for b in self._birds:
            b.x += b.vx * dt
            b._wing_phase += dt * 9

        self._birds = [b for b in self._birds if b.x < self.W + 60]
        while len(self._birds) < _BIRD_COUNT:
            self._spawn_bird(random.uniform(-120, -20))

    def draw(self, surf):
        surf.blit(self._sky, (0, 0))

        # Sun
        gw = self._sun_glow.get_width()
        surf.blit(self._sun_glow, (self._sun_x - gw // 2, self._sun_y - gw // 2))

        # Clouds
        for c in self._clouds:
            surf.blit(c["surf"], (int(c["x"]), int(c["y"])))

        # Hills — back to front with parallax
        for speed, color, amp, freq, phase, base_frac in _HILL_DEFS:
            scroll  = self._scroll * speed
            base_y  = int(self.H * base_frac)
            pts = [(0, self.H)]
            for px in range(0, self.W + 6, 6):
                py = base_y + int(math.sin((px + scroll) * freq + phase) * amp * self.H)
                pts.append((px, py))
            pts.append((self.W, self.H))
            pygame.draw.polygon(surf, color, pts)
            # Soft highlight along the ridgeline
            ridge = [p for p in pts[1:-1]]
            if len(ridge) >= 2:
                r, g, b = color
                pygame.draw.lines(surf, (min(r + 28, 255), min(g + 28, 255), min(b + 18, 255)),
                                  False, ridge, 1)

        # Wind particles — drawn directly for speed
        for p in self._particles:
            pygame.draw.circle(surf, p["color"], (int(p["x"]), int(p["y"])), p["size"])

        # Birds
        try:
            from Render.birds import draw_birds
            draw_birds(surf, 0, 0, self._birds)
        except Exception:
            pass
