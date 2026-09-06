import sys
from gen_cyberspace import Camera, build_scene, BG

# GitHub social-preview / og:image spec.
W, H = 1280, 640
cam = Camera(eye=(0.0, 4.6, 17.0), target=(0.4, 5.6, -13.0), fov_deg=58, width=W, height=H)
scene = build_scene(cam, seed=int(sys.argv[1]) if len(sys.argv) > 1 else 11)

TPL = '''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Jay Johnson - Full-Stack Engineer and Systems Integrator - jsonj.net">
  <defs>
    <radialGradient id="vig" cx="0.5" cy="0.46" r="0.76">
      <stop offset="38%" stop-color="#000005" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000005" stop-opacity=".9"/>
    </radialGradient>
    <linearGradient id="plate" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0%" stop-color="#000005" stop-opacity=".93"/>
      <stop offset="58%" stop-color="#000005" stop-opacity=".72"/>
      <stop offset="100%" stop-color="#000005" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-40%" y="-70%" width="180%" height="240%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="12" result="blur"/>
      <feFlood flood-color="#ff2fd0" flood-opacity=".55" result="tint"/>
      <feComposite in="tint" in2="blur" operator="in" result="halo"/>
      <feMerge><feMergeNode in="halo"/><feMergeNode in="halo"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="softglow" x="-40%" y="-90%" width="180%" height="280%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4.5" result="blur"/>
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
  <rect x="0" y="330" width="{W}" height="310" fill="url(#plate)"/>

  <g font-family="'Space Grotesk','Segoe UI',Inter,system-ui,-apple-system,sans-serif" text-anchor="middle">
    <text x="640" y="486" font-size="88" font-weight="700" letter-spacing="-2" fill="#f5f0ff" filter="url(#glow)">Jay Johnson<tspan fill="#ff2fd0">.</tspan></text>
    <text x="640" y="536" font-size="27" font-weight="500" letter-spacing=".8" fill="#d8ccf0">Full-Stack Engineer &amp; Systems Integrator</text>
  </g>
  <g font-family="'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" text-anchor="middle">
    <text x="640" y="580" font-size="16" letter-spacing="5"><tspan fill="#2fe0ff" filter="url(#softglow)">JSONJ.NET</tspan><tspan fill="#a89fc0">&#160;&#160;&#183;&#160;&#160;REMOTE-ONLY</tspan></text>
  </g>
  <rect x="556" y="600" width="120" height="2" fill="#ff2fd0" opacity=".85"/>
  <rect x="680" y="600" width="44" height="2" fill="#2fe0ff" opacity=".6"/>
</svg>
'''

open('social-banner.svg', 'w').write(TPL.format(W=W, H=H, BG=BG, SCENE=scene.render()))
print('segments:', len(scene.items))
