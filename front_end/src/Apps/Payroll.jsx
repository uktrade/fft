import { useEffect, useReducer, useState, useMemo } from "react";

import EditPayroll from "../Components/EditPayroll";
import * as api from "../Components/EditPayroll/api";
import {
  payrollHeaders,
  vacancyHeaders,
} from "../Components/EditPayroll/constants";
import EmployeeRow from "../Components/EditPayroll/EmployeeRow";
import VacancyRow from "../Components/EditPayroll/VacancyRow";

const initialPayrollState = [];
const initialVacanciesState = [];

export default function Payroll() {
  const [allPayroll, dispatch] = useReducer(
    payrollReducer,
    initialPayrollState
  );
  const [vacancies, dispatchVacancies] = useReducer(
    vacanciesReducer,
    initialVacanciesState
  );
  const [saveSuccess, setSaveSuccess] = useState(false);

  const addVacancyUrl = "vacancies/create"; // Should not be hardcoded ideally

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
    [allPayroll]
  );
  const nonPayroll = useMemo(
    () => allPayroll.filter((payroll) => payroll.basic_pay <= 0),
    [allPayroll]
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

  function handleTogglePayPeriods(employeeNo, index, enabled) {
    dispatch({ type: "updatePayPeriods", employeeNo, index, enabled });
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
      <EditPayroll
        payroll={payroll}
        headers={payrollHeaders}
        onTogglePayPeriods={handleTogglePayPeriods}
        RowComponent={EmployeeRow}
      />
      <h2 className="govuk-heading-m">Non-payroll</h2>
      <EditPayroll
        payroll={nonPayroll}
        headers={payrollHeaders}
        onTogglePayPeriods={handleTogglePayPeriods}
        RowComponent={EmployeeRow}
      />
      <h2 className="govuk-heading-m">Vacancies</h2>
      <a class="govuk-button" href={addVacancyUrl}>
        Add Vacancy
      </a>
      <EditPayroll
        payroll={vacancies}
        headers={vacancyHeaders}
        onTogglePayPeriods={handleToggleVacancyPayPeriods}
        RowComponent={VacancyRow}
      />
      <button className="govuk-button" onClick={handleSavePayroll}>
        Save payroll
      </button>
    </>
  );
}

function payrollReducer(payroll, action) {
  switch (action.type) {
    case "fetched": {
      return action.data;
    }
    case "updatePayPeriods": {
      return payroll.map((employeeRow) => {
        if (employeeRow.employee_no == action.employeeNo) {
          const updatedPayPeriods = employeeRow.pay_periods.map(
            (period, index) => {
              if (index + 1 >= action.index + 1) {
                return !action.enabled;
              }
              return period;
            }
          );
          return {
            ...employeeRow,
            pay_periods: updatedPayPeriods,
          };
        }
        return employeeRow;
      });
    }
  }
}

function vacanciesReducer(vacancies, action) {
  switch (action.type) {
    case "fetched": {
      return action.data;
    }
    case "updatePayPeriods": {
      return vacancies.map((vacancy) => {
        if (vacancy.id == action.id) {
          const updatedPayPeriods = vacancy.pay_periods.map((period, index) => {
            if (index + 1 >= action.index + 1) {
              return !action.enabled;
            }
            return period;
          });
          return {
            ...vacancy,
            pay_periods: updatedPayPeriods,
          };
        }
        return vacancy;
      });
    }
  }
}
