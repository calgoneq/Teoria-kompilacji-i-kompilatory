export default function CompileButton({ onClick, isCompiling }) {
  return (
    <button
      className={`compile-btn ${isCompiling ? 'compiling' : ''}`}
      onClick={onClick}
      disabled={isCompiling}
      id="compile-button"
      title="Ctrl+Enter"
    >
      {isCompiling ? (
        <>
          <div className="spinner"></div>
          <span>Compiling...</span>
        </>
      ) : (
        <>
          <span>▶ Compile</span>
          <span className="compile-shortcut">Ctrl+Enter</span>
        </>
      )}
    </button>
  )
}
