const PayPeriods = ({ row, id, onTogglePayPeriods }) => {
  return (
    <>
      {row.pay_periods.map((enabled, index) => {
        return (
          <td className="govuk-table__cell" key={index}>
            <input
              type="checkbox"
              checked={enabled}
              onChange={() => onTogglePayPeriods(id, index, enabled)}
            />
          </td>
        );
      })}
    </>
  );
};

export default PayPeriods;
