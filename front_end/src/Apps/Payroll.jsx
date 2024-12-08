import { useEffect, useReducer, useState, useMemo } from "react";

import * as api from "../Components/EditPayroll/api";
import {
  payrollHeaders,
  vacancyHeaders,
} from "../Components/EditPayroll/constants";
import EmployeeRow from "../Components/EditPayroll/EmployeeRow";
import VacancyRow from "../Components/EditPayroll/VacancyRow";
import PayrollTable from "../Components/EditPayroll/PayrollTable";

const initialPayrollState = [];
const initialVacanciesState = [];

export default function Payroll() {
  const [allPayroll, dispatch] = useReducer(
    payrollReducer,
    initialPayrollState,
  );
  const [vacancies, dispatchVacancies] = useReducer(
    vacanciesReducer,
    initialVacanciesState,
  );
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    const savedSuccessFlag = localStorage.getItem("saveSuccess");
    if (savedSuccessFlag === "true") {
      setSaveSuccess(true);
      localStorage.removeItem("saveSuccess");
    }

    api.getPayrollData().then((data) => dispatch({ type: "fetched", data }));
    api
      .getVacancyData()
      .then((data) => dispatchVacancies({ type: "fetched", data }));
  }, []);

  // Computed properties
  const payroll = useMemo(
    () => allPayroll.filter((payroll) => payroll.basic_pay > 0),
    [allPayroll],
  );
  const nonPayroll = useMemo(
    () => allPayroll.filter((payroll) => payroll.basic_pay <= 0),
    [allPayroll],
  );

  // Handlers
  async function handleSavePayroll() {
    try {
      await api.postPayrollData(allPayroll);
      await api.postVacancyData(vacancies);

      setSaveSuccess(true);
      localStorage.setItem("saveSuccess", "true");

      window.location.reload();
    } catch (error) {
      console.error("Error saving payroll: ", error);
    }
  }

  function handleTogglePayPeriods(id, index, enabled) {
    dispatch({ type: "updatePayPeriods", id, index, enabled });
  }

  function handleToggleVacancyPayPeriods(id, index, enabled) {
    dispatchVacancies({ type: "updatePayPeriods", id, index, enabled });
  }

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
      <h2 className="govuk-heading-m">Payroll</h2>
      <PayrollTable
        payroll={payroll}
        headers={payrollHeaders}
        onTogglePayPeriods={handleTogglePayPeriods}
        RowComponent={EmployeeRow}
      />
      <h2 className="govuk-heading-m">Non-payroll</h2>
      <PayrollTable
        payroll={nonPayroll}
        headers={payrollHeaders}
        onTogglePayPeriods={handleTogglePayPeriods}
        RowComponent={EmployeeRow}
      />
      <h2 className="govuk-heading-m">Vacancies</h2>
      <PayrollTable
        payroll={vacancies}
        headers={vacancyHeaders}
        onTogglePayPeriods={handleToggleVacancyPayPeriods}
        RowComponent={VacancyRow}
      />
      <a
        className="govuk-button govuk-!-margin-right-2 govuk-button--secondary"
        href={window.addVacancyUrl}
      >
        Add Vacancy
      </a>
      <button className="govuk-button" onClick={handleSavePayroll}>
        Save payroll
      </button>
    </>
  );
}

const positionReducer = (data, action) => {
  switch (action.type) {
    case "fetched": {
      return action.data;
    }
    case "updatePayPeriods": {
      return data.map((row) => {
        if (row.id === action.id) {
          const updatedPayPeriods = row.pay_periods.map((period, index) => {
            if (index + 1 >= action.index + 1) {
              return !action.enabled;
            }
            return period;
          });
          return {
            ...row,
            pay_periods: updatedPayPeriods,
          };
        }
        return row;
      });
    }
  }
};

const payrollReducer = (data, action) => positionReducer(data, action);
const vacanciesReducer = (data, action) => positionReducer(data, action);
