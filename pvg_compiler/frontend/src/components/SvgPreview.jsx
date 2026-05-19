import { useState, useCallback } from 'react'

export default function SvgPreview({ svg }) {
  const [copied, setCopied] = useState(false)

  const handleCopy = useCallback(async () => {
    if (!svg) return
    try {
      await navigator.clipboard.writeText(svg)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      console.error('Failed to copy SVG')
    }
  }, [svg])

  const handleDownload = useCallback(() => {
    if (!svg) return
    const blob = new Blob([svg], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'pvg_output.svg'
    a.click()
    URL.revokeObjectURL(url)
  }, [svg])

  if (!svg) {
    return (
      <div className="svg-preview-container">
        <div className="svg-preview-empty">
          <div className="svg-preview-empty-icon">🖼</div>
          <div className="svg-preview-empty-text">No SVG generated yet</div>
          <div className="svg-preview-empty-hint">Write PVG code and compile to see the result</div>
        </div>
      </div>
    )
  }

  return (
    <div className="svg-preview-container">
      <div className="svg-preview-wrapper" id="svg-preview">
        <div className="preview-actions">
          <button
            className={`preview-action-btn ${copied ? 'copied' : ''}`}
            onClick={handleCopy}
            title="Copy SVG to clipboard"
          >
            {copied ? '✓ Copied' : '📋 Copy'}
          </button>
          <button
            className="preview-action-btn"
            onClick={handleDownload}
            title="Download SVG file"
          >
            💾 Download
          </button>
        </div>
        <div dangerouslySetInnerHTML={{ __html: svg }} />
      </div>
    </div>
  )
}
