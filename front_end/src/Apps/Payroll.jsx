import { useEffect, useReducer, useState, useMemo } from "react";

import * as api from "../Components/EditPayroll/api";
import {
  payrollHeaders,
  vacancyHeaders,
} from "../Components/EditPayroll/constants";
import EmployeeRow from "../Components/EditPayroll/EmployeeRow";
import VacancyRow from "../Components/EditPayroll/VacancyRow";
import PayrollTable from "../Components/EditPayroll/PayrollTable";
import Tabs, { Tab } from "../Components/EditPayroll/Tabs";
import EditPayModifier from "../Components/EditPayroll/EditPayModifier";

const initialPayrollState = [];
const initialVacanciesState = [];
const initialPayModifiersState = [];

export default function Payroll() {
  const [allPayroll, dispatch] = useReducer(
    payrollReducer,
    initialPayrollState,
  );
  const [vacancies, dispatchVacancies] = useReducer(
    vacanciesReducer,
    initialVacanciesState,
  );
  const [payModifiers, dispatchPayModifiers] = useReducer(
    payModifiersReducer,
    initialPayModifiersState,
  );
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [activeTab, setActiveTab] = useState(() => {
    const savedTab = localStorage.getItem("activeTab");
    return savedTab ? parseInt(savedTab) : 0;
  });

  useEffect(() => {
    localStorage.setItem("activeTab", activeTab);
  }, [activeTab]);

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
    api
      .getPayModifierData()
      .then((data) => dispatchPayModifiers({ type: "fetched", data }));
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
      await api.postPayModifierData(payModifiers);

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

  function handleUpdatePayModifiers(id, index, value) {
    dispatchPayModifiers({ type: "updatePayModifiers", id, index, value });
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
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab}>
        <Tab label="Payroll" key="1">
          <PayrollTable
            payroll={payroll}
            headers={payrollHeaders}
            onTogglePayPeriods={handleTogglePayPeriods}
            RowComponent={EmployeeRow}
          />
        </Tab>
        <Tab label="Non-payroll" key="2">
          <PayrollTable
            payroll={nonPayroll}
            headers={payrollHeaders}
            onTogglePayPeriods={handleTogglePayPeriods}
            RowComponent={EmployeeRow}
          />
        </Tab>
        <Tab label="Vacancies" key="3">
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
        </Tab>
        <Tab label="Pay modifiers" key="4">
          <EditPayModifier
            data={payModifiers}
            onInputChange={handleUpdatePayModifiers}
          />
        </Tab>
      </Tabs>
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

const payModifiersReducer = (data, action) => {
  switch (action.type) {
    case "fetched": {
      return action.data;
    }
    case "updatePayModifiers": {
      return data.map((row) => {
        if (row.id === action.id) {
          const updatedPayModifier = row.pay_modifiers.map(
            (modifier, index) => {
              if (index === action.index) {
                return parseFloat(action.value);
              }
              return modifier;
            },
          );
          return {
            ...row,
            pay_modifiers: updatedPayModifier,
          };
        }
        return row;
      });
    }
  }
};

const payrollReducer = (data, action) => positionReducer(data, action);
const vacanciesReducer = (data, action) => positionReducer(data, action);
