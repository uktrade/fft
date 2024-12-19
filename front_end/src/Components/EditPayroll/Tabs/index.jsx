export default function Tabs({ activeTab, setActiveTab, children }) {
  const tabs = Array.isArray(children) ? children : [children];
  return (
    <>
      <div className="govuk-tabs" data-module="govuk-tabs">
        <h2 className="govuk-tabs__title">Contents</h2>
        <ul className="govuk-tabs__list">
          {tabs.map((tab, index) => (
            <li
              className={`govuk-tabs__list-item ${activeTab === index ? "govuk-tabs__list-item--selected" : ""}`}
              key={index}
            >
              <a
                className="govuk-tabs__tab"
                href="#"
                onClick={() => setActiveTab(index)}
              >
                {tab.props.label}
              </a>
            </li>
          ))}
        </ul>
        {tabs.map((tab, index) => (
          <div
            className={`govuk-tabs__panel ${activeTab === index ? "" : "govuk-tabs__panel--hidden"}`}
            key={index}
            id={tab.props.label}
          >
            <h2 className="govuk-heading-m">{tab.props.label}</h2>
            {tab.props.children}
          </div>
        ))}
      </div>
    </>
  );
}

export const Tab = ({ children }) => {
  return <div>{{ children }}</div>;
};
