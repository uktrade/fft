import { useState } from "react";

export default function ToggleCheckbox({ payrollToggle, setPayrollToggle, id, value, label }) {

  const handleToggle = () => {
    setPayrollToggle(!payrollToggle);
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
                checked={payrollToggle}
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
