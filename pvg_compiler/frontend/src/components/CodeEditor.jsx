import Editor from '@monaco-editor/react'

function setupPvgLanguage(monaco) {

  monaco.languages.register({ id: 'pvg' })

  monaco.languages.setMonarchTokensProvider('pvg', {
    keywords: [
      'canvas', 'background', 'fill', 'color', 'stroke', 'stroke_width', 'opacity',
      'font_size', 'font_family', 'circle', 'rect', 'line', 'ellipse',
      'polygon', 'polyline', 'text', 'path', 'rotate', 'translate', 'scale',
      'def', 'for', 'while', 'let', 'if', 'else', 'print', 'break', 'continue'
    ],
    mathFunctions: [
      'sin', 'cos', 'tan', 'sqrt', 'log', 'exp', 'abs', 'round', 'ceil', 'floor'
    ],
    operators: ['==', '!=', '<=', '>=', '<', '>', '+', '-', '*', '/', '%', '=', 'and', 'or', 'not'],
    tokenizer: {
      root: [
        [/#.*$/, 'comment'],
        [/"[^"]*"/, 'string'],
        [/\d+\.\d+/, 'number.float'],
        [/\d+/, 'number'],
        [/[a-zA-Z_]\w*/, {
          cases: {
            '@keywords': 'keyword',
            '@mathFunctions': 'support.function',
            '@default': 'identifier'
          }
        }],
        [/[{}()\[\];,]/, 'delimiter'],
        [/[=!<>]=?|[+\-*\/%]/, 'operator'],
        [/\s+/, 'white']
      ]
    }
  })

  monaco.languages.registerCompletionItemProvider('pvg', {
    provideCompletionItems: (model, position) => {
      const word = model.getWordUntilPosition(position)
      const range = {
        startLineNumber: position.lineNumber,
        endLineNumber: position.lineNumber,
        startColumn: word.startColumn,
        endColumn: word.endColumn
      }

      const createItem = (label, kind, detail, insertText) => ({
        label, kind, detail, insertText, range,
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet
      })

      const suggestions = [
        createItem('canvas', monaco.languages.CompletionItemKind.Function, 'Utwórz płótno', 'canvas(${1:800}, ${2:600});'),
        createItem('background', monaco.languages.CompletionItemKind.Function, 'Ustaw tło', 'background("${1:#ffffff}");'),
        createItem('fill', monaco.languages.CompletionItemKind.Function, 'Kolor wypełnienia', 'fill("${1:#000000}");'),
        createItem('color', monaco.languages.CompletionItemKind.Function, 'Kolor wypełnienia (alias fill)', 'color("${1:#000000}");'),
        createItem('stroke', monaco.languages.CompletionItemKind.Function, 'Kolor obrysu', 'stroke("${1:#000000}");'),
        createItem('stroke_width', monaco.languages.CompletionItemKind.Function, 'Grubość obrysu', 'stroke_width(${1:1});'),
        createItem('opacity', monaco.languages.CompletionItemKind.Function, 'Przezroczystość', 'opacity(${1:1.0});'),
        createItem('circle', monaco.languages.CompletionItemKind.Function, 'Rysuj okrąg', 'circle(${1:x}, ${2:y}, ${3:r});'),
        createItem('rect', monaco.languages.CompletionItemKind.Function, 'Rysuj prostokąt', 'rect(${1:x}, ${2:y}, ${3:w}, ${4:h});'),
        createItem('line', monaco.languages.CompletionItemKind.Function, 'Rysuj linię', 'line(${1:x1}, ${2:y1}, ${3:x2}, ${4:y2});'),
        createItem('ellipse', monaco.languages.CompletionItemKind.Function, 'Rysuj elipsę', 'ellipse(${1:cx}, ${2:cy}, ${3:rx}, ${4:ry});'),
        createItem('polygon', monaco.languages.CompletionItemKind.Function, 'Rysuj wielokąt', 'polygon("${1:points}");'),
        createItem('text', monaco.languages.CompletionItemKind.Function, 'Rysuj tekst', 'text(${1:x}, ${2:y}, "${3:tekst}");'),
        createItem('for', monaco.languages.CompletionItemKind.Keyword, 'Pętla for', 'for (let ${1:i} = ${2:0}; ${1:i} < ${3:10}; ${1:i} = ${1:i} + 1) {\n\t$0\n}'),
        createItem('while', monaco.languages.CompletionItemKind.Keyword, 'Pętla while', 'while (${1:condition}) {\n\t$0\n}'),
        createItem('if', monaco.languages.CompletionItemKind.Keyword, 'Warunek', 'if (${1:condition}) {\n\t$0\n}'),
        createItem('def', monaco.languages.CompletionItemKind.Keyword, 'Definicja procedury', 'def ${1:nazwa}(${2:params}) {\n\t$0\n}'),
        createItem('let', monaco.languages.CompletionItemKind.Keyword, 'Deklaracja zmiennej', 'let ${1:nazwa} = ${2:wartość};'),
        createItem('rotate', monaco.languages.CompletionItemKind.Function, 'Rotacja', 'rotate(${1:kąt});'),
        createItem('translate', monaco.languages.CompletionItemKind.Function, 'Translacja', 'translate(${1:x}, ${2:y});'),
        createItem('scale', monaco.languages.CompletionItemKind.Function, 'Skalowanie', 'scale(${1:x}, ${2:y});'),
      ]
      return { suggestions }
    }
  })

  monaco.editor.defineTheme('pvg-dark-neutral', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: 'E06C75', fontStyle: 'bold' },
      { token: 'support.function', foreground: '8EBD79' },
      { token: 'identifier', foreground: '61AFEF' },
      { token: 'number', foreground: 'E5C07B' },
      { token: 'number.float', foreground: 'E5C07B' },
      { token: 'string', foreground: '8EBD79' },
      { token: 'comment', foreground: '686868', fontStyle: 'italic' },
      { token: 'operator', foreground: '56B6C2' },
      { token: 'delimiter', foreground: 'B0B0B0' },
    ],
    colors: {
      'editor.background': '#1e1e1e',
      'editor.foreground': '#f5f5f5',
      'editorCursor.foreground': '#61afef',
      'editor.lineHighlightBackground': '#282828',
      'editor.selectionBackground': '#3e3e3e',
      'editor.inactiveSelectionBackground': '#2e2e2e',
      'editorLineNumber.foreground': '#686868',
      'editorLineNumber.activeForeground': '#f5f5f5',
      'editorGutter.background': '#1e1e1e',
      'editorIndentGuide.background': '#2a2a2a',
      'scrollbarSlider.background': 'rgba(255,255,255,0.06)',
      'scrollbarSlider.hoverBackground': 'rgba(255,255,255,0.12)',
    }
  })
}

export default function CodeEditor({ code, onChange }) {
  const handleBeforeMount = (monaco) => {
    setupPvgLanguage(monaco)
  }

  return (
    <div className="editor-container">
      <Editor
        height="100%"
        language="pvg"
        theme="pvg-dark-neutral"
        value={code}
        onChange={(value) => onChange(value || '')}
        beforeMount={handleBeforeMount}
        loading={
          <div className="editor-loading">
            <div className="spinner"></div>
            <span>Loading editor...</span>
          </div>
        }
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          fontFamily: "'JetBrains Mono', monospace",
          fontLigatures: true,
          lineNumbers: 'on',
          scrollBeyondLastLine: false,
          padding: { top: 16, bottom: 16 },
          roundedSelection: true,
          smoothScrolling: true,
          cursorBlinking: 'smooth',
          cursorSmoothCaretAnimation: 'on',
          renderLineHighlight: 'all',
          bracketPairColorization: { enabled: true },
          autoClosingBrackets: 'always',
          autoClosingQuotes: 'always',
          formatOnPaste: true,
          suggestOnTriggerCharacters: true,
          wordWrap: 'off',
          overviewRulerBorder: false,
          hideCursorInOverviewRuler: true,
          scrollbar: {
            verticalScrollbarSize: 6,
            horizontalScrollbarSize: 6,
          },
        }}
      />
    </div>
  )
}
