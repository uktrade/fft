const PayPeriods = ({
  row,
  id,
  onTogglePayPeriods,
  previousMonths,
  showPreviousMonths,
}) => {
  return (
    <>
      {row.pay_periods.map((enabled, index) => {
        const isActual = previousMonths[index].is_actual;
        const isHidden = showPreviousMonths && isActual ? " hidden" : "";
        return (
          <td className={`govuk-table__cell ${isHidden}`} key={index}>
            <input
              type="checkbox"
              checked={enabled}
              disabled={isActual}
              onChange={() => onTogglePayPeriods(id, index, enabled)}
            />
          </td>
        );
      })}
    </>
  );
};

export default PayPeriods;
