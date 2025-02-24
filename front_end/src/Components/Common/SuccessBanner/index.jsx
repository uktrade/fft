export default function SuccessBanner({ children }) {
  return (
    <div className="govuk-notification-banner govuk-notification-banner--success">
      <div className="govuk-notification-banner__header">
        <h2
          className="govuk-notification-banner__title"
          id="govuk-notification-banner-title"
        >
          {children}
        </h2>
      </div>
    </div>
  );
}
