import sys
from gen_cyberspace import Camera, build_scene, BG

W = H = 500
cam = Camera(eye=(0.0, 4.6, 15.0), target=(0.0, 5.4, -12.0), fov_deg=75, width=W, height=H)
scene = build_scene(cam, seed=int(sys.argv[1]) if len(sys.argv) > 1 else 3)

TPL = '''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="JJ - jsonj.net">
  <defs>
    <radialGradient id="vig" cx="0.5" cy="0.5" r="0.72">
      <stop offset="30%" stop-color="#000005" stop-opacity=".55"/>
      <stop offset="62%" stop-color="#000005" stop-opacity=".18"/>
      <stop offset="100%" stop-color="#000005" stop-opacity=".9"/>
    </radialGradient>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="14" result="blur"/>
      <feFlood flood-color="#ff2fd0" flood-opacity=".6" result="tint"/>
      <feComposite in="tint" in2="blur" operator="in" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow" x="-60%" y="-90%" width="220%" height="280%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="blur"/>
      <feFlood flood-color="#2fe0ff" flood-opacity=".75" result="tint"/>
      <feComposite in="tint" in2="blur" operator="in" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g fill="none">
{SCENE}
  </g>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>

  <text x="238" y="268" text-anchor="middle" font-family="'Space Grotesk','Segoe UI',Inter,system-ui,-apple-system,sans-serif" font-weight="700" font-size="158" letter-spacing="-6" fill="#f5f0ff" filter="url(#glow)">JJ<tspan fill="#ff2fd0" dx="-26">.</tspan></text>
  <text x="250" y="356" text-anchor="middle" font-family="'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="19" letter-spacing="7.5" fill="#2fe0ff" filter="url(#softglow)">JSONJ.NET</text>
</svg>
'''

open('avatar.svg', 'w').write(TPL.format(W=W, H=H, BG=BG, SCENE=scene.render()))
print('segments:', len(scene.items))
