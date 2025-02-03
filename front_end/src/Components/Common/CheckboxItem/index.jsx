export default function CheckboxItem({ onChange, checked, name, label }) {
  return (
    <div className="govuk-checkboxes__item">
      <input
        type="checkbox"
        name={name}
        id={`show_hide_${name}`}
        className="govuk-checkboxes__input"
        checked={checked}
        onChange={onChange}
      />
      <label className="govuk-label govuk-checkboxes__label" htmlFor={name}>
        {label}
      </label>
    </div>
  );
}
