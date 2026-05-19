export default function ErrorPanel({ errors }) {
  if (!errors || errors.length === 0) {
    return (
      <div className="no-errors">
        <div className="no-errors-icon">✅</div>
        <div className="no-errors-text">No errors — code is clean!</div>
        <div className="no-errors-hint">✨</div>
      </div>
    )
  }

  return (
    <div className="error-panel" id="error-panel">
      {errors.map((err, i) => (
        <div
          key={i}
          className={`error-item error-type-${err.type || 'runtime'}`}
          style={{ animationDelay: `${i * 80}ms` }}
        >
          <div className="error-icon">
            {err.type === 'semantic' ? '🛑' : err.type === 'parser' ? '❌' : err.type === 'lexer' ? '🔍' : '⚠️'}
          </div>
          <div className="error-content">
            <div className="error-message">{err.message}</div>
            <div className="error-type-label">{err.type || 'error'}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
