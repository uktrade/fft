const PayPeriods = ({ row, id, onTogglePayPeriods, offset }) => {
  return (
    <>
      {row.pay_periods.map((enabled, index) => {
        return (
          <td className="govuk-table__cell" key={index}>
            <input
              type="checkbox"
              checked={enabled}
              onChange={() => onTogglePayPeriods(id, index + offset, enabled)}
            />
          </td>
        );
      })}
    </>
  );
};

export default PayPeriods;
