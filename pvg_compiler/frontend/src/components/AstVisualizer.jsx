import { useState } from 'react'

function getNodeCategory(type) {
  const keywords = new Set(['IF', 'FOR', 'WHILE', 'DEF', 'BREAK', 'CONTINUE'])
  const statements = new Set([
    'ASSIGN', 'ASSIGN_ARRAY', 'SET_ARRAY', 'CALL', 'PRINT',
    'CANVAS', 'BACKGROUND', 'FILL', 'STROKE', 'STROKE_WIDTH', 'OPACITY',
    'FONT_SIZE', 'FONT_FAMILY', 'CIRCLE', 'RECT', 'LINE', 'ELLIPSE',
    'POLYGON', 'POLYLINE', 'PATH', 'TEXT', 'ROTATE', 'TRANSLATE', 'SCALE'
  ])
  const expressions = new Set(['BINOP', 'UNARY', 'NOT', 'MATH_FUNC', 'VAR', 'GET_ARRAY'])
  const literals = new Set(['NUMBER', 'STRING', 'LITERAL'])

  if (type === 'PROGRAM') return 'program'
  if (keywords.has(type)) return 'keyword'
  if (statements.has(type)) return 'statement'
  if (expressions.has(type)) return 'expression'
  if (literals.has(type)) return 'literal'
  return 'statement'
}

function AstNode({ node, depth = 0 }) {
  const [expanded, setExpanded] = useState(depth < 2)

  if (!node || typeof node !== 'object') return null

  if (Array.isArray(node)) {
    return (
      <div>
        {node.map((child, i) => (
          <AstNode key={i} node={child} depth={depth} />
        ))}
      </div>
    )
  }

  const { type, children, value, kind } = node
  const hasChildren = children && children.length > 0
  const category = getNodeCategory(type || '')
  const isLeaf = !hasChildren

  return (
    <div className="ast-node" style={{ animationDelay: `${depth * 30}ms` }}>
      <div className="ast-node-header" onClick={() => !isLeaf && setExpanded(!expanded)}>
        <span className={`ast-node-toggle ${expanded ? 'expanded' : ''} ${isLeaf ? 'leaf' : ''}`}>
          ▶
        </span>
        <span className={`ast-node-type ast-type-${category}`}>
          {type || 'unknown'}
        </span>
        {value !== undefined && (
          <span className="ast-node-value">
            {kind === 'string' ? `"${value}"` : value}
          </span>
        )}
      </div>
      {hasChildren && expanded && (
        <div className="ast-node-children">
          {children.map((child, i) => (
            <AstNode key={i} node={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  )
}

export default function AstVisualizer({ ast }) {
  if (!ast) {
    return (
      <div className="ast-empty">
        <div className="ast-empty-icon">🌳</div>
        <div className="ast-empty-text">Compile code to see the AST</div>
      </div>
    )
  }

  return (
    <div className="ast-tree" id="ast-visualizer">
      <AstNode node={ast} depth={0} />
    </div>
  )
}
