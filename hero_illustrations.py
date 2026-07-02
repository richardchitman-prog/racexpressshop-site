# Fixed hero illustrations, keyed by topics.json "category".
# Kept out of the LLM's hands entirely so a bad generation can never break the page layout.
# Add a new category here (and in topics.json) any time you want a new visual variant.

HERO_SVGS = {

    "stats": """<svg class="hero-illo" viewBox="0 0 380 300" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="190" cy="278" rx="150" ry="12" fill="#000" opacity="0.06"/>
      <g transform="translate(60 40)">
        <line x1="0" y1="180" x2="260" y2="180" stroke="#c9bf9e" stroke-width="1.5"/>
        <rect x="20" y="90" width="44" height="90" fill="#a63a2e" rx="3"/>
        <rect x="108" y="50" width="44" height="130" fill="#2f6e62" rx="3"/>
        <rect x="196" y="120" width="44" height="60" fill="#202a3a" rx="3"/>
        <text x="42" y="82" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="11" font-weight="700" fill="#822c22">B</text>
        <text x="130" y="42" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="11" font-weight="700" fill="#234f46">M</text>
        <text x="218" y="112" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="11" font-weight="700" fill="#202a3a">K</text>
      </g>
      <g transform="translate(150 8) rotate(-8)">
        <circle cx="0" cy="0" r="20" fill="none" stroke="#a63a2e" stroke-width="2.5"/>
        <text x="0" y="4" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="8" font-weight="700" fill="#a63a2e">DATA</text>
      </g>
    </svg>""",

    "explainer": """<svg class="hero-illo" viewBox="0 0 380 300" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="190" cy="278" rx="150" ry="12" fill="#000" opacity="0.06"/>
      <g transform="translate(160 40)">
        <rect x="0" y="0" width="62" height="120" rx="12" fill="#202a3a"/>
        <rect x="6" y="11" width="50" height="88" rx="3" fill="#f8f5ea"/>
        <circle cx="31" cy="110" r="4.5" fill="#4a5468"/>
      </g>
      <g transform="translate(55 190)">
        <path d="M0 10 L46 10 L43 38 Q43 42 38 42 L8 42 Q3 42 3 38 Z" fill="#f2ede0" stroke="#202a3a" stroke-width="2"/>
        <path d="M0 10 L9 3 L37 3 L46 10 Z" fill="#e4dcc4" stroke="#202a3a" stroke-width="2"/>
        <text x="23" y="30" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="7" fill="#4a5468">FTC</text>
      </g>
      <g transform="translate(155 190)">
        <path d="M0 10 L46 10 L43 38 Q43 42 38 42 L8 42 Q3 42 3 38 Z" fill="#f2ede0" stroke="#202a3a" stroke-width="2"/>
        <path d="M0 10 L9 3 L37 3 L46 10 Z" fill="#e4dcc4" stroke="#202a3a" stroke-width="2"/>
        <text x="23" y="30" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="7" fill="#4a5468">FCC</text>
      </g>
      <g transform="translate(255 190)">
        <path d="M0 10 L46 10 L43 38 Q43 42 38 42 L8 42 Q3 42 3 38 Z" fill="#f2ede0" stroke="#202a3a" stroke-width="2"/>
        <path d="M0 10 L9 3 L37 3 L46 10 Z" fill="#e4dcc4" stroke="#202a3a" stroke-width="2"/>
        <text x="23" y="30" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="6.5" fill="#4a5468">FBI IC3</text>
      </g>
      <path d="M191 160 L78 195" stroke="#2f6e62" stroke-width="2" stroke-dasharray="3 4" fill="none"/>
      <path d="M191 160 L178 195" stroke="#2f6e62" stroke-width="2" stroke-dasharray="3 4" fill="none"/>
      <path d="M191 160 L278 195" stroke="#2f6e62" stroke-width="2" stroke-dasharray="3 4" fill="none"/>
    </svg>""",

    "warning": """<svg class="hero-illo" viewBox="0 0 380 300" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="190" cy="278" rx="150" ry="12" fill="#000" opacity="0.06"/>
      <rect x="150" y="50" width="80" height="140" rx="12" fill="#202a3a"/>
      <rect x="158" y="64" width="64" height="98" rx="3" fill="#f8f5ea"/>
      <text x="190" y="100" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="9" fill="#6b6558">(704) 555-0182</text>
      <line x1="168" y1="112" x2="212" y2="112" stroke="#c9bf9e" stroke-width="1.5" stroke-dasharray="3 2"/>
      <text x="190" y="132" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="7.5" fill="#a63a2e">ORIGIN: UNKNOWN</text>
      <g transform="translate(275 60)">
        <circle cx="0" cy="0" r="20" fill="none" stroke="#a63a2e" stroke-width="3.5"/>
        <line x1="14" y1="14" x2="28" y2="28" stroke="#a63a2e" stroke-width="5" stroke-linecap="round"/>
      </g>
      <g transform="translate(75 90)">
        <circle cx="0" cy="0" r="14" fill="none" stroke="#2f6e62" stroke-width="2.5"/>
        <text x="0" y="4" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="6.5" font-weight="700" fill="#234f46">TELL</text>
      </g>
    </svg>""",

    "protect": """<svg class="hero-illo" viewBox="0 0 380 300" xmlns="http://www.w3.org/2000/svg">
      <ellipse cx="190" cy="278" rx="150" ry="12" fill="#000" opacity="0.06"/>
      <g transform="translate(60 60)">
        <rect x="0" y="0" width="54" height="106" rx="10" fill="#202a3a"/>
        <rect x="6" y="9" width="42" height="78" rx="2" fill="#f8f5ea"/>
      </g>
      <g transform="translate(266 60)">
        <rect x="0" y="0" width="54" height="106" rx="10" fill="#202a3a"/>
        <rect x="6" y="9" width="42" height="78" rx="2" fill="#f8f5ea"/>
      </g>
      <g transform="translate(146 78)">
        <path d="M0 10 L88 10 L82 68 Q82 74 74 74 L14 74 Q6 74 6 68 Z" fill="#f2ede0" stroke="#202a3a" stroke-width="2"/>
        <path d="M0 10 L16 2 L72 2 L88 10 Z" fill="#e4dcc4" stroke="#202a3a" stroke-width="2"/>
      </g>
      <path d="M118 100 Q133 96 148 104" stroke="#2f6e62" stroke-width="2" stroke-dasharray="3 4" fill="none"/>
      <path d="M262 100 Q247 96 232 104" stroke="#2f6e62" stroke-width="2" stroke-dasharray="3 4" fill="none"/>
      <path d="M190 32 C182 20 168 20 165 32 C162 44 190 60 190 60 C190 60 218 44 215 32 C212 20 198 20 190 32 Z" fill="none" stroke="#a63a2e" stroke-width="2.5"/>
    </svg>""",
}
