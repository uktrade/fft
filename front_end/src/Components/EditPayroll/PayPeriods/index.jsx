const PayPeriods = ({ row, id, onTogglePayPeriods, offset }) => {
  const hasActuals = row.pay_periods.length < 12;
  return (
    <>
      {row.pay_periods.map((enabled, index) => {
        const row_id = hasActuals ? index + offset : index;
        return (
          <td className="govuk-table__cell" key={index}>
            <input
              type="checkbox"
              checked={enabled}
              disabled={row_id < offset}
              onChange={() => onTogglePayPeriods(id, row_id, enabled)}
            />
          </td>
        );
      })}
    </>
  );
};

export default PayPeriods;
