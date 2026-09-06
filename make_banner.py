import sys
from gen_cyberspace import Camera, build_scene, BG

W, H = 1200, 300
cam = Camera(eye=(0.0, 4.3, 20.0), target=(0.6, 5.3, -14.0), fov_deg=40, width=W, height=H)
scene = build_scene(cam, seed=int(sys.argv[1]) if len(sys.argv) > 1 else 7)

TPL = '''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Jay Johnson - Full-Stack Engineer and Systems Integrator">
  <defs>
    <radialGradient id="vig" cx="0.5" cy="0.5" r="0.78">
      <stop offset="55%" stop-color="#000005" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000005" stop-opacity=".85"/>
    </radialGradient>
    <linearGradient id="plate" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000005" stop-opacity=".88"/>
      <stop offset="62%" stop-color="#000005" stop-opacity=".66"/>
      <stop offset="100%" stop-color="#000005" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-40%" y="-60%" width="180%" height="220%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="9" result="blur"/>
      <feFlood flood-color="#ff2fd0" flood-opacity=".55" result="tint"/>
      <feComposite in="tint" in2="blur" operator="in" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow" x="-40%" y="-80%" width="180%" height="260%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
      <feFlood flood-color="#2fe0ff" flood-opacity=".7" result="tint"/>
      <feComposite in="tint" in2="blur" operator="in" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="{BG}"/>
  <g fill="none">
{SCENE}
  </g>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
  <rect width="660" height="{H}" fill="url(#plate)"/>

  <g font-family="'Space Grotesk','Segoe UI',Inter,system-ui,-apple-system,sans-serif">
    <text x="64" y="132" font-size="62" font-weight="700" fill="#f5f0ff" filter="url(#glow)" letter-spacing="-1">Jay Johnson<tspan fill="#ff2fd0">.</tspan></text>
    <text x="66" y="172" font-size="21" font-weight="500" fill="#d8ccf0" letter-spacing=".6">Full-Stack Engineer &amp; Systems Integrator</text>
  </g>
  <g font-family="'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">
    <text x="66" y="209" font-size="13.5" fill="#2fe0ff" letter-spacing="3.4" filter="url(#softglow)">JSONJ.NET/ABOUT</text>
    <text x="242" y="209" font-size="13.5" fill="#a89fc0" letter-spacing="3.4">&#183;  REMOTE-ONLY</text>
  </g>
  <rect x="64" y="228" width="118" height="2" fill="#ff2fd0" opacity=".85"/>
  <rect x="186" y="228" width="42" height="2" fill="#2fe0ff" opacity=".6"/>
</svg>
'''

open('banner.svg', 'w').write(TPL.format(W=W, H=H, BG=BG, SCENE=scene.render()))
print('segments:', len(scene.items))
