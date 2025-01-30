import { useDispatch } from "react-redux";

export default function CheckboxItem({ dispatcher, checked, name, label }) {
  const dispatch = useDispatch();
  return (
    <div className="govuk-checkboxes__item">
      <input
        type="checkbox"
        name={name}
        id={`show_hide_${name}`}
        className="govuk-checkboxes__input"
        checked={checked}
        onChange={(e) => {
          dispatch(dispatcher(name));
        }}
      />
      <label className="govuk-label govuk-checkboxes__label" htmlFor={name}>
        {label}
      </label>
    </div>
  );
}
