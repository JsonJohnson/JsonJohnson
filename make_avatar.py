import sys
from gen_cyberspace import Camera, build_scene, BG

# Avatar variant, tuned for the sizes GitHub actually renders one at:
# 32-48px in comments and PRs, not the 260px profile page. The wordmark is
# gone, the JJ lockup fills the circle-crop, and the tower field is thinned
# to a few thick wireframes so it reads as a canyon rather than as noise.
W = H = 500
cam = Camera(eye=(0.0, 4.8, 13.0), target=(0.0, 5.8, -12.0), fov_deg=72, width=W, height=H)
scene = build_scene(
    cam,
    seed=int(sys.argv[1]) if len(sys.argv) > 1 else 5,
    tower_density=0.34,
    particles=170,
    grid_step=4.0,
    grid_stroke=1.9,
    tower_stroke=2.6,
    particle_size=0.03,
    min_tower_height=4.5,
    tower_height_range=10.0,
    floor_sub="#a32a86",
    ceil_sub="#2683a0",
    tower_lightness=0.62,
)

TPL = '''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="JJ - Jay Johnson">
  <defs>
    <radialGradient id="vig" cx="0.5" cy="0.5" r="0.7">
      <stop offset="26%" stop-color="#000005" stop-opacity=".42"/>
      <stop offset="60%" stop-color="#000005" stop-opacity=".08"/>
      <stop offset="100%" stop-color="#000005" stop-opacity=".92"/>
    </radialGradient>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="16" result="blur"/>
      <feFlood flood-color="#ff2fd0" flood-opacity=".75" result="tint"/>
      <feComposite in="tint" in2="blur" operator="in" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="halo"/><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g fill="none">
{SCENE}
  </g>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>

  <text x="272" y="327" text-anchor="middle" font-family="'Space Grotesk','Segoe UI',Inter,system-ui,-apple-system,sans-serif" font-weight="700" font-size="288" letter-spacing="-16" fill="#f7f3ff" filter="url(#glow)">JJ</text>
</svg>
'''

open('avatar.svg', 'w').write(TPL.format(W=W, H=H, BG=BG, SCENE=scene.render()))
print('segments:', len(scene.items))
