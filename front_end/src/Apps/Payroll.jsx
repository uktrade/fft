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
import DisplayPayModifier from "../Components/EditPayroll/DisplayPayModifier";
import ToggleCheckbox from "../Components/Common/ToggleCheckbox";
import ErrorSummary from "../Components/Common/ErrorSummary";
import SuccessBanner from "../Components/Common/SuccessBanner";
import ForecastTable from "../Components/EditPayroll/ForecastTable";
import { makeFinancialCodeKey } from "../Util";

const initialPayrollState = {
  employees: [],
  vacancies: [],
  pay_modifiers: [],
  forecast: [],
  // TODO: Rename as this covers all months not only previous.
  previous_months: [],
  actuals: [],
};
const costCentreCode = window.costCentreCode;
const financialYear = window.financialYear;

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
  const forecastAndActuals = useMemo(() => {
    const total_results = [];

    for (const item of allPayroll.forecast) {
      let results = {
        programme_code: item.programme_code,
        natural_account_code: item.natural_account_code,
      };

      allPayroll.previous_months.map((month) => {
        if (month.is_actual) {
          const financialCodeKey = makeFinancialCodeKey(
            costCentreCode,
            item.natural_account_code,
            item.programme_code,
            { year: financialYear, period: month.index },
          );
          results[month.key] = allPayroll.actuals[financialCodeKey];
        } else {
          results[month.key] = item[month.key];
        }
      });

      total_results.push(results);
    }

    return total_results;
  }, [allPayroll]);

  // Handlers
  async function handleSavePayroll() {
    try {
      await api.postPayrollData(allPayroll);
      setSaveSuccess(true);
      setSaveError(false);
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

  function handleCreatePayModifiers() {
    api.createPayModifiers().then((r) => {
      getAllPayroll();
    });
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
            showPreviousMonths={showPreviousMonths}
          />
        </Tab>
        <Tab label="Non-payroll" key="2">
          <PayrollTable
            payroll={nonPayroll}
            headers={payrollHeaders}
            onTogglePayPeriods={handleTogglePayPeriods}
            RowComponent={EmployeeRow}
            previousMonths={allPayroll.previous_months}
            showPreviousMonths={showPreviousMonths}
          />
        </Tab>
        <Tab label="Vacancies" key="3">
          <PayrollTable
            payroll={allPayroll.vacancies}
            headers={vacancyHeaders}
            onTogglePayPeriods={handleToggleVacancyPayPeriods}
            RowComponent={VacancyRow}
            previousMonths={allPayroll.previous_months}
            showPreviousMonths={showPreviousMonths}
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
            onCreate={handleCreatePayModifiers}
          />
          {/* <DisplayPayModifier data={allPayroll.pay_modifiers.pay_uplift} /> */}
        </Tab>
      </Tabs>
      <button className="govuk-button" onClick={handleSavePayroll}>
        Save payroll
      </button>
      <ForecastTable
        forecast={forecastAndActuals}
        months={allPayroll.previous_months}
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
