const EXAMPLE_META = {
  '01_podstawy': { icon: '🟢', desc: 'Basics — canvas, colors, shapes' },
  '02_petle_i_zmienne': { icon: '🔄', desc: 'Loops and variables' },
  '03_funkcje_i_matematyka': { icon: '⭐', desc: 'Functions and math (star pattern)' },
  '04_advanced_features': { icon: '🥷', desc: 'Arrays, text, transforms, polygons' },
  '05_bledy': { icon: '🐛', desc: 'Error handling demo' },
  '06_spirala': { icon: '🌀', desc: 'Archimedean spiral with colors' },
  '07_fraktale': { icon: '🌲', desc: 'Fractal tree with recursion' },
}

export default function ExampleGallery({ examples, onSelect }) {
  if (!examples || examples.length === 0) {
    return (
      <div className="gallery-grid">
        <div className="gallery-empty">
          Loading examples...
        </div>
      </div>
    )
  }

  return (
    <div className="gallery-grid" id="example-gallery">
      {examples.map((ex) => {
        const meta = EXAMPLE_META[ex.name] || { icon: '📄', desc: 'PVG example' }
        return (
          <div
            key={ex.name}
            className="gallery-card"
            onClick={() => onSelect(ex.name)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => e.key === 'Enter' && onSelect(ex.name)}
          >
            <div className="gallery-card-icon">{meta.icon}</div>
            <div className="gallery-card-title">{ex.title}</div>
            <div className="gallery-card-desc">{meta.desc}</div>
          </div>
        )
      })}
    </div>
  )
}
