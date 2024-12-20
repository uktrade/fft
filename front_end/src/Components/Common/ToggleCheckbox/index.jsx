export default function ToggleCheckbox({ toggle, handler, id, value, label }) {
  return (
    <>
      <div className="govuk-form-group govuk-!-margin-bottom-0">
        <fieldset className="govuk-fieldset" aria-describedby="toggle-hint">
          <div
            className="govuk-checkboxes govuk-checkboxes--small"
            data-module="govuk-checkboxes"
          >
            <div className="govuk-checkboxes__item">
              <input
                className="govuk-checkboxes__input"
                id={id}
                name={id}
                type="checkbox"
                checked={toggle}
                onChange={handler}
                value={value}
              />
              <label
                className="govuk-label govuk-checkboxes__label"
                htmlFor={id}
              >
                {label}
              </label>
            </div>
          </div>
        </fieldset>
      </div>
    </>
  );
}
