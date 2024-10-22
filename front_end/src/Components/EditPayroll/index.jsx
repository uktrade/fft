import * as types from "./types";
import PayrollTable from "./PayrollTable/index";

/**
 *
 * @param {object} props
 * @param {types.PayrollData[]} props.payroll
 * @returns
 */
export default function EditPayroll({
  payroll,
  onSavePayroll,
  onTogglePayPeriods,
  saveSuccess,
}) {
  const headers = [
    "Name",
    "Employee No",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
    "Jan",
    "Feb",
    "Mar",
  ];
  return (
    <>
      {saveSuccess && (
        <div className="govuk-notification-banner govuk-notification-banner--success">
          <div className="govuk-notification-banner__header">
            <h2
              className="govuk-notification-banner__title"
              id="govuk-notification-banner-title"
            >
              Success
            </h2>
          </div>
        </div>
      )}
      <PayrollTable
        headers={headers}
        payroll={payroll}
        onTogglePayPeriods={onTogglePayPeriods}
      ></PayrollTable>
      <button className="govuk-button" onClick={onSavePayroll}>
        Save payroll
      </button>
    </>
  );
}
