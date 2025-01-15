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
import ToggleCheckbox from "../Components/Common/ToggleCheckbox";
import ErrorSummary from "../Components/Common/ErrorSummary";
import SuccessBanner from "../Components/Common/SuccessBanner";
import ForecastTable from "../Components/EditPayroll/ForecastTable";
import { monthsToTitleCase } from "../Util";

const initialPayrollState = {
  employees: [],
  vacancies: [],
  pay_modifiers: [],
  forecast: [],
  previous_months: [],
};

export default function Payroll() {
  const [allPayroll, dispatch] = useReducer(
    payrollReducer,
    initialPayrollState,
  );
  const initialShowPreviousMonths = localStorage.getItem(
    "editPayroll.showPreviousMonths",
  );
  const [showPreviousMonths, setShowPreviousMonths] = useState(
    initialShowPreviousMonths === "true",
  );
  const [offset, setOffset] = useState(0);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [saveError, setSaveError] = useState(false);
  const [activeTab, setActiveTab] = useState(() => {
    const savedTab = localStorage.getItem("editPayroll.activeTab");
    return savedTab ? parseInt(savedTab) : 0;
  });

  function getAllPayroll() {
    api.getPayrollData().then((data) => {
      dispatch({ type: "fetched", data });
    });
  }

  // Use Effects
  useEffect(() => {
    localStorage.setItem("editPayroll.activeTab", activeTab);
    setSaveSuccess(false);
    setSaveError(false);
  }, [activeTab]);

  useEffect(() => {
    const showAllMonths = localStorage.getItem(
      "editPayroll.showPreviousMonths",
    );
    setOffset(allPayroll.previous_months.length);

    if (showAllMonths === "true") {
      allPayroll.previous_months = [];
    } else {
      getAllPayroll();
    }
  }, [showPreviousMonths]);

  useEffect(() => {
    getAllPayroll();
  }, []);

  // Computed properties
  const payroll = useMemo(
    () => allPayroll.employees.filter((payroll) => payroll.basic_pay > 0),
    [allPayroll],
  );
  const nonPayroll = useMemo(
    () => allPayroll.employees.filter((payroll) => payroll.basic_pay <= 0),
    [allPayroll],
  );

  // Handlers
  async function handleSavePayroll() {
    try {
      await api.postPayrollData(allPayroll);
      setSaveSuccess(true);
      getAllPayroll();
    } catch (error) {
      console.error("Error saving payroll: ", error);
      setSaveSuccess(false);
      setSaveError(true);
    }
  }

  function handleTogglePayPeriods(id, index, enabled) {
    dispatch({ type: "updatePayPeriodsEmployees", id, index, enabled });
  }

  function handleToggleVacancyPayPeriods(id, index, enabled) {
    dispatch({ type: "updatePayPeriodsVacancies", id, index, enabled });
  }

  function handleUpdatePayModifiers(id, index, value) {
    dispatch({ type: "updatePayModifiers", id, index, value });
  }

  function handleHidePreviousMonths() {
    setShowPreviousMonths(!showPreviousMonths);

    localStorage.setItem(
      "editPayroll.showPreviousMonths",
      JSON.stringify(!showPreviousMonths),
    );
  }

  const errors = [{ label: "", message: "Error saving payroll data" }];

  return (
    <>
      {saveSuccess && <SuccessBanner />}
      {saveError && <ErrorSummary errors={errors} />}
      <ToggleCheckbox
        toggle={showPreviousMonths}
        handler={handleHidePreviousMonths}
        id="payroll-previous-months"
        value="payroll-previous-months"
        label="Hide previous months"
      />
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab}>
        <Tab label="Payroll" key="1">
          <PayrollTable
            payroll={payroll}
            headers={payrollHeaders}
            onTogglePayPeriods={handleTogglePayPeriods}
            RowComponent={EmployeeRow}
            previousMonths={allPayroll.previous_months}
            offset={offset}
          />
        </Tab>
        <Tab label="Non-payroll" key="2">
          <PayrollTable
            payroll={nonPayroll}
            headers={payrollHeaders}
            onTogglePayPeriods={handleTogglePayPeriods}
            RowComponent={EmployeeRow}
            previousMonths={allPayroll.previous_months}
            offset={offset}
          />
        </Tab>
        <Tab label="Vacancies" key="3">
          <PayrollTable
            payroll={allPayroll.vacancies}
            headers={vacancyHeaders}
            onTogglePayPeriods={handleToggleVacancyPayPeriods}
            RowComponent={VacancyRow}
            previousMonths={allPayroll.previous_months}
            offset={offset}
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
            data={allPayroll.pay_modifiers}
            onInputChange={handleUpdatePayModifiers}
          />
        </Tab>
      </Tabs>
      <button className="govuk-button" onClick={handleSavePayroll}>
        Save payroll
      </button>
      <ForecastTable
        forecast={allPayroll.forecast}
        months={monthsToTitleCase}
      />
    </>
  );
}

function updatePayPeriods(data, action) {
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

function updatePayModifiers(data, action) {
  return data.map((row) => {
    if (row.id === action.id) {
      const updatedPayModifier = row.pay_modifiers.map((modifier, index) => {
        if (index === action.index) {
          return parseFloat(action.value);
        }
        return modifier;
      });
      return {
        ...row,
        pay_modifiers: updatedPayModifier,
      };
    }
    return row;
  });
}

const payrollReducer = (data, action) => {
  switch (action.type) {
    case "fetched": {
      return action.data;
    }
    case "updatePayPeriodsEmployees": {
      return {
        ...data,
        employees: updatePayPeriods(data.employees, action),
      };
    }
    case "updatePayPeriodsVacancies": {
      return {
        ...data,
        vacancies: updatePayPeriods(data.vacancies, action),
      };
    }
    case "updatePayModifiers": {
      return {
        ...data,
        pay_modifiers: updatePayModifiers(data.pay_modifiers, action),
      };
    }
  }
};
