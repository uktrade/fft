import { useState } from "react";

export default function ToggleCheckbox({ toggle, setToggle, id, value, label }) {

  const handleToggle = () => {
    setToggle(!toggle);

    // To fix: Hacky method, set to local storage so this value can be passed
    // to processForecastData when updating a cell
    localStorage.setItem('isPayrollEnabled', JSON.stringify(!toggle));
  }

  return (
    <>
      <div className="govuk-form-group">
        <fieldset className="govuk-fieldset" aria-describedby='toggle-hint'>
          <div className="govuk-checkboxes govuk-checkboxes--small" data-module="govuk-checkboxes">
            <div className="govuk-checkboxes__item">
              <input
                className="govuk-checkboxes__input"
                id={id}
                name={id}
                type="checkbox"
                checked={toggle}
                onChange={handleToggle}
                value={value}
              />
              <label className="govuk-label govuk-checkboxes__label" htmlFor={id}>
                { label }
              </label>
            </div>
          </div>
        </fieldset>
      </div>
    </>
  );
}
