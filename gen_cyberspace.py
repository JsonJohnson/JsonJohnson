"""Render jsonj.net's `cyberspace` theme as a static SVG.

Mirrors js/3d-themes.js initCyberspace(): floor grid (#ff2fd0) at y=0 and
ceiling grid (#2fe0ff) at y=14 over a 140-unit span / 70 divisions, wireframe
data towers on a 4.2-unit lattice with random HSL(h,1,.55) hues, additive
particle stream, THREE.Fog(0x000005, 4, 42), PerspectiveCamera(fov=75).
Real look-at + perspective projection with near-plane clipping, so the
geometry is genuinely the site's scene, not a hand-drawn approximation.
"""
import colorsys
import math
import random

BG = "#000005"
FOG_NEAR, FOG_FAR = 4.0, 42.0
NEAR = 0.12


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    m = math.sqrt(dot(a, a)) or 1.0
    return (a[0] / m, a[1] / m, a[2] / m)


class Camera:
    def __init__(self, eye, target, fov_deg, width, height, up=(0, 1, 0)):
        self.eye = eye
        self.width, self.height = width, height
        forward = norm(sub(target, eye))
        right = norm(cross(forward, up))
        true_up = cross(right, forward)
        self.basis = (right, true_up, forward)
        self.focal = 1.0 / math.tan(math.radians(fov_deg) / 2.0)
        self.aspect = width / height

    def to_camera_space(self, p):
        right, true_up, forward = self.basis
        d = sub(p, self.eye)
        # z is distance along the view direction (positive in front of camera)
        return (dot(d, right), dot(d, true_up), dot(d, forward))

    def project(self, cam_pt):
        x, y, z = cam_pt
        ndc_x = (self.focal / self.aspect) * x / z
        ndc_y = self.focal * y / z
        return ((ndc_x + 1) * 0.5 * self.width, (1 - ndc_y) * 0.5 * self.height)


def fog_alpha(distance):
    if distance <= FOG_NEAR:
        return 1.0
    if distance >= FOG_FAR:
        return 0.0
    return 1.0 - (distance - FOG_NEAR) / (FOG_FAR - FOG_NEAR)


def clip_near(a, b):
    """Clip a camera-space segment to the near plane; None if fully behind."""
    if a[2] <= NEAR and b[2] <= NEAR:
        return None
    if a[2] >= NEAR and b[2] >= NEAR:
        return a, b
    t = (NEAR - a[2]) / (b[2] - a[2])
    mid = tuple(a[i] + (b[i] - a[i]) * t for i in range(3))
    return (a, mid) if a[2] > NEAR else (mid, b)


def hsl_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


class Scene:
    """Collects world-space primitives, emits depth-sorted SVG."""

    def __init__(self, camera):
        self.camera = camera
        self.items = []

    def line(self, p0, p1, color, opacity=1.0, width=1.0, segments=None):
        # Subdivide so per-segment fog reads as a real gradient down the canyon.
        length = math.dist(p0, p1)
        n = segments or max(1, min(16, int(length / 3.0)))
        for i in range(n):
            t0, t1 = i / n, (i + 1) / n
            a = tuple(p0[k] + (p1[k] - p0[k]) * t0 for k in range(3))
            b = tuple(p0[k] + (p1[k] - p0[k]) * t1 for k in range(3))
            self._emit_segment(a, b, color, opacity, width)

    def _emit_segment(self, a, b, color, opacity, width):
        cam = self.camera
        ca, cb = cam.to_camera_space(a), cam.to_camera_space(b)
        clipped = clip_near(ca, cb)
        if clipped is None:
            return
        ca, cb = clipped
        depth = (ca[2] + cb[2]) * 0.5
        alpha = fog_alpha(depth) * opacity
        if alpha < 0.06:
            return
        x0, y0 = cam.project(ca)
        x1, y1 = cam.project(cb)
        if not all(map(math.isfinite, (x0, y0, x1, y1))):
            return
        span = max(abs(x0 - x1), abs(y0 - y1))
        if span > cam.width * 6:
            return
        self.items.append((depth, "line", (x0, y0, x1, y1, color, alpha, width)))

    def point(self, p, color, size, opacity=1.0):
        cam = self.camera
        cp = cam.to_camera_space(p)
        if cp[2] <= NEAR:
            return
        alpha = fog_alpha(cp[2]) * opacity
        if alpha < 0.05:
            return
        x, y = cam.project(cp)
        if not (-40 <= x <= cam.width + 40 and -40 <= y <= cam.height + 40):
            return
        r = max(0.45, size * cam.focal / cp[2] * cam.height * 0.5)
        self.items.append((cp[2], "point", (x, y, r, color, alpha)))

    def streak(self, p, length, color, size, opacity=1.0):
        """Motion-blurred particle: the data stream rushing the camera."""
        cam = self.camera
        cp = cam.to_camera_space(p)
        cq = cam.to_camera_space((p[0], p[1], p[2] + length))
        if cp[2] <= NEAR or cq[2] <= NEAR:
            return
        alpha = fog_alpha(cp[2]) * opacity
        if alpha < 0.05:
            return
        x0, y0 = cam.project(cp)
        x1, y1 = cam.project(cq)
        w = max(0.5, size * cam.focal / cp[2] * cam.height)
        self.items.append((cp[2], "streak", (x0, y0, x1, y1, color, alpha, w)))

    def render(self):
        out = []
        for depth, kind, d in sorted(self.items, key=lambda it: -it[0]):
            if kind == "line":
                x0, y0, x1, y1, color, alpha, width = d
                out.append(
                    '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-opacity="%.3f" stroke-width="%.2f"/>' % (x0, y0, x1, y1, color, alpha, width)
                )
            elif kind == "point":
                x, y, r, color, alpha = d
                out.append(
                    '<circle cx="%.1f" cy="%.1f" r="%.2f" fill="%s" fill-opacity="%.3f"/>'
                    % (x, y, r, color, alpha)
                )
            else:
                x0, y0, x1, y1, color, alpha, w = d
                out.append(
                    '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-opacity="%.3f" stroke-width="%.2f" stroke-linecap="round"/>'
                    % (x0, y0, x1, y1, color, alpha, w)
                )
        return "\n".join(out)


def grid(scene, y, color_main, color_sub, half=44, step=2.0, center_every=10, stroke=1.0):
    lo = -half
    n = int(half * 2 / step)
    for i in range(n + 1):
        v = lo + i * step
        color = color_main if i % center_every == 0 else color_sub
        opacity = 1.0 if i % center_every == 0 else 0.7
        scene.line((v, y, -half), (v, y, half), color, opacity, stroke, segments=18)
        scene.line((-half, y, v), (half, y, v), color, opacity, stroke, segments=6)


def box_wireframe(scene, cx, cy, cz, sx, sy, sz, color, opacity, width=1.15):
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    corners = [
        (cx + dx * hx, cy + dy * hy, cz + dz * hz)
        for dx in (-1, 1)
        for dy in (-1, 1)
        for dz in (-1, 1)
    ]
    # index = (dx,dy,dz) bits in that order
    edges = [
        (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
        (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
    ]
    for a, b in edges:
        scene.line(corners[a], corners[b], color, opacity, width)


def build_scene(camera, seed, tower_density=0.55, particles=900, grid_step=2.0,
                grid_stroke=1.0, tower_stroke=1.15, particle_size=0.011,
                min_tower_height=2.0, tower_height_range=11.0,
                floor_sub="#5c1a4d", ceil_sub="#134c5c", tower_lightness=0.55,
                tower_opacity=0.85):
    rng = random.Random(seed)
    scene = Scene(camera)

    grid(scene, 0.0, "#ff2fd0", floor_sub, step=grid_step, stroke=grid_stroke)
    grid(scene, 14.0, "#2fe0ff", ceil_sub, step=grid_step, stroke=grid_stroke)

    half_span, spacing = 30, 4.2
    gx = -half_span
    while gx <= half_span:
        gz = -half_span
        while gz <= half_span:
            if abs(gx) < 3 and abs(gz) < 3:
                gz += spacing
                continue
            if rng.random() > tower_density:
                gz += spacing
                continue
            h = min_tower_height + rng.random() * tower_height_range
            color = hsl_hex(rng.random(), 1.0, tower_lightness)
            fx = gx + (rng.random() - 0.5) * 1.4
            fz = gz + (rng.random() - 0.5) * 1.4
            w = 0.9 + rng.random() * 0.6
            d = 0.9 + rng.random() * 0.6
            box_wireframe(scene, fx, h / 2, fz, w, h, d, color, tower_opacity, tower_stroke)
            gz += spacing
        gx += spacing

    for _ in range(particles):
        p = (
            (rng.random() - 0.5) * 40,
            rng.random() * 13,
            (rng.random() - 0.5) * 60,
        )
        color = hsl_hex(rng.random(), 1.0, 0.6)
        scene.streak(p, 0.35 + rng.random() * 0.65, color, particle_size, 0.8)

    return scene
