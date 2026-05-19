export default function TokenInspector({ tokens }) {
  if (!tokens || tokens.length === 0) {
    return (
      <div className="token-empty">
        <div className="token-empty-icon">🔤</div>
        <div className="token-empty-text">Compile code to see the token stream</div>
      </div>
    )
  }

  let lastLine = null
  const elements = []

  tokens.forEach((token, i) => {
    if (token.lineno !== lastLine) {
      if (lastLine !== null) {
        elements.push(
          <div key={`line-${token.lineno}`} className="token-line-marker">
            ── Line {token.lineno} ──
          </div>
        )
      } else {
        elements.push(
          <div key={`line-${token.lineno}`} className="token-line-marker">
            ── Line {token.lineno} ──
          </div>
        )
      }
      lastLine = token.lineno
    }

    const category = token.category || 'punctuation'
    elements.push(
      <div
        key={`token-${i}`}
        className={`token-pill token-${category}`}
        title={`Type: ${token.type}\nValue: ${token.value}\nLine: ${token.lineno}`}
        style={{ animationDelay: `${i * 15}ms` }}
      >
        <span className="token-type">{token.type}</span>
        <span className="token-value">{token.value}</span>
      </div>
    )
  })

  return (
    <div className="token-grid" id="token-inspector">
      {elements}
    </div>
  )
}
