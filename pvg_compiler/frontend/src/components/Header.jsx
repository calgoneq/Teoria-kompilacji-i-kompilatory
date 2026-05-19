export default function Header({ isCompiling, hasErrors }) {
  const statusClass = isCompiling ? 'compiling' : hasErrors ? 'error' : 'ready'
  const statusText = isCompiling ? 'Compiling...' : hasErrors ? 'Errors' : 'Ready'

  return (
    <header className="header" id="app-header">
      <div className="header-left">
        <div className="header-logo">
          <span className="header-logo-text">PVG Studio</span>
        </div>
        <span className="header-subtitle">Procedural Vector Graphics Compiler</span>
      </div>
      <div className="header-right">
        <div className={`status-badge ${statusClass}`}>
          <span className="status-dot"></span>
          <span>{statusText}</span>
        </div>
        <span className="version-badge">v1.0</span>
      </div>
    </header>
  )
}
