export default function TabPanel({ tabs, activeTab, onTabChange }) {
  const activeContent = tabs.find(t => t.id === activeTab)

  return (
    <div className="tab-panel">
      <div className="tab-header">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {activeContent?.content}
      </div>
    </div>
  )
}
