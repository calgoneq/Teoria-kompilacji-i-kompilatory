import { useState, useEffect, useCallback } from 'react'
import { compileCode, getExamples, getExample } from './utils/api'
import Header from './components/Header'
import CodeEditor from './components/CodeEditor'
import SvgPreview from './components/SvgPreview'
import AstVisualizer from './components/AstVisualizer'
import TokenInspector from './components/TokenInspector'
import CompileButton from './components/CompileButton'
import ExampleGallery from './components/ExampleGallery'
import ErrorPanel from './components/ErrorPanel'
import TabPanel from './components/TabPanel'

const DEFAULT_CODE = `canvas(800, 600);
background("#282c34");

# Witaj w PVG Studio! 🎨
# Wpisz kod i naciśnij Ctrl+Enter

fill("#61afef");
circle(400, 300, 100);

fill("#e06c75");
rect(250, 200, 100, 100);

fill("#98c379");
for (let i = 0; i < 5; i = i + 1) {
    circle(150 + i * 130, 450, 30);
}
`

export default function App() {
  const [code, setCode] = useState(DEFAULT_CODE)
  const [svgOutput, setSvgOutput] = useState(null)
  const [ast, setAst] = useState(null)
  const [tokens, setTokens] = useState(null)
  const [errors, setErrors] = useState([])
  const [output, setOutput] = useState('')
  const [isCompiling, setIsCompiling] = useState(false)
  const [activeTab, setActiveTab] = useState('preview')
  const [examples, setExamples] = useState([])

  useEffect(() => {
    getExamples()
      .then(setExamples)
      .catch(() => setExamples([]))
  }, [])

  const handleCompile = useCallback(async () => {
    if (isCompiling || !code.trim()) return
    setIsCompiling(true)

    try {
      const result = await compileCode(code)
      setSvgOutput(result.svg || null)
      setAst(result.ast || null)
      setTokens(result.tokens || null)
      setErrors(result.errors || [])
      setOutput(result.output || '')

      if (!result.success && result.errors?.length > 0) {
        setActiveTab('errors')
      }
    } catch (err) {
      setErrors([{ message: `Błąd połączenia z serwerem: ${err.message}`, type: 'runtime' }])
      setActiveTab('errors')
    } finally {
      setIsCompiling(false)
    }
  }, [code, isCompiling])

  useEffect(() => {
    const timer = setTimeout(() => {
      if (code.trim()) {
        handleCompile()
      }
    }, 1500)
    return () => clearTimeout(timer)
  }, [code])

  useEffect(() => {
    const handleKey = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault()
        handleCompile()
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [handleCompile])

  const handleLoadExample = useCallback(async (name) => {
    try {
      const data = await getExample(name)
      setCode(data.code)
      setActiveTab('preview')
    } catch (err) {
      console.error('Failed to load example:', err)
    }
  }, [])

  const tabs = [
    { id: 'preview', label: '🖼 Preview', content: <SvgPreview svg={svgOutput} /> },
    { id: 'ast', label: '🌳 AST', content: <AstVisualizer ast={ast} /> },
    { id: 'tokens', label: '🔤 Tokens', content: <TokenInspector tokens={tokens} /> },
    { id: 'errors', label: `⚠ Errors${errors.length > 0 ? ` (${errors.length})` : ''}`, content: <ErrorPanel errors={errors} /> },
    {
      id: 'output', label: '📟 Output', content: (
        output ? (
          <div className="output-console">
            {output.split('\n').map((line, i) => (
              <div key={i} className={`output-line ${line.includes('❌') || line.includes('🛑') ? 'error' : ''}`}>
                {line || '\u00A0'}
              </div>
            ))}
          </div>
        ) : (
          <div className="output-empty">
            <div className="output-empty-icon">📟</div>
            <div className="output-empty-text">No output yet</div>
          </div>
        )
      )
    },
    { id: 'examples', label: '📚 Examples', content: <ExampleGallery examples={examples} onSelect={handleLoadExample} /> }
  ]

  return (
    <div className="app-container">
      <Header isCompiling={isCompiling} hasErrors={errors.length > 0} />
      <div className="main-content">
        <div className="editor-pane">
          <div className="pane-header">
            <span className="pane-header-label">Editor</span>
            <CompileButton onClick={handleCompile} isCompiling={isCompiling} />
          </div>
          <CodeEditor code={code} onChange={setCode} />
        </div>
        <div className="preview-pane">
          <TabPanel tabs={tabs} activeTab={activeTab} onTabChange={setActiveTab} />
        </div>
      </div>
    </div>
  )
}
