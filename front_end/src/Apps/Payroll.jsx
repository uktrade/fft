import { useEffect, useReducer, useState, useMemo } from "react";

import * as api from "../Components/EditPayroll/api";
import Tabs, { Tab } from "../Components/EditPayroll/Tabs";
import DisplayAttrition from "../Components/EditPayroll/DisplayAttrition";
import DisplayPayModifier from "../Components/EditPayroll/DisplayPayModifier";
import ErrorSummary from "../Components/Common/ErrorSummary";
import SuccessBanner from "../Components/Common/SuccessBanner";
import ForecastTable from "../Components/EditPayroll/ForecastTable";
import { makeFinancialCodeKey } from "../Util";
import Loading from "../Components/Common/Loading";
import TanstackTable from "../Components/EditPayroll/TanstackTable";
import getPayrollColumns, {
  getVacanciesColumns,
} from "../Components/EditPayroll/TanstackTable/columns";

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

  // State

  const [isLoading, setIsLoading] = useState(true);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [errors, setErrors] = useState(null);
  const [activeTab, setActiveTab] = useState(() => {
    const savedTab = localStorage.getItem("editPayroll.activeTab");
    return savedTab ? parseInt(savedTab) : 0;
  });

  // Fetches

  async function getAllPayroll() {
    try {
      const data = await api.getPayrollData();
      dispatch({ type: "fetched", data });
    } catch (error) {
      setErrors([
        {
          label: "",
          message: "Error occurred whilst fetching payroll data",
        },
      ]);
    }
    // finally
    setIsLoading(false);
  }

  // Use Effects
  useEffect(() => {
    localStorage.setItem("editPayroll.activeTab", activeTab);
    setSaveSuccess(false);
    setErrors(null);
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
      setErrors(null);
      getAllPayroll();
    } catch (error) {
      setSaveSuccess(false);
      setErrors([{ label: "", message: "Error saving payroll data" }]);
    }
  }

  function handleTogglePayPeriods(id, index, enabled) {
    dispatch({ type: "updatePayPeriodsEmployees", id, index, enabled });
  }

  function handleToggleVacancyPayPeriods(id, index, enabled) {
    dispatch({ type: "updatePayPeriodsVacancies", id, index, enabled });
  }

  function handleUpdateAttrition(index, value) {
    dispatch({ type: "updateAttrition", index, value });
  }

  function handleCreateAttrition() {
    api.createPayModifiers().then((r) => {
      getAllPayroll();
    });
  }

  if (isLoading) {
    return <Loading />;
  }

  return (
    <>
      {saveSuccess && <SuccessBanner>Success - forecast updated</SuccessBanner>}
      {errors && <ErrorSummary errors={errors} />}
      <div className="govuk-form-group">
        <button className="govuk-button" onClick={handleSavePayroll}>
          Save changes
        </button>
        <a
          className="govuk-button govuk-button--secondary govuk-!-margin-left-4"
          href={window.forecastUrl}
        >
          Go to forecast
        </a>
      </div>
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab}>
        <Tab label="Payroll" key="1">
          <TanstackTable
            data={payroll}
            columns={getPayrollColumns(
              payroll,
              handleTogglePayPeriods,
              allPayroll.previous_months,
            )}
            previousMonths={allPayroll.previous_months}
            tableId="payroll"
          />
        </Tab>
        <Tab label="Non-payroll" key="2">
          <div className="govuk-grid-row">
            <div className="govuk-grid-column-two-thirds">
              <p className="govuk-body">
                Non-payroll includes staff on maternity leave,{" "}
                <a
                  className="govuk-link"
                  target="_blank"
                  href="https://www.civil-service-careers.gov.uk/fast-stream/"
                >
                  Fast Streamers
                </a>
                , contingent workers (contractors), staff loaned in from other
                departments and secondments.
              </p>
            </div>
          </div>
          <TanstackTable
            data={nonPayroll}
            columns={getPayrollColumns(
              nonPayroll,
              handleTogglePayPeriods,
              allPayroll.previous_months,
            )}
            previousMonths={allPayroll.previous_months}
            tableId="non-payroll"
          />
        </Tab>
        <Tab label="Vacancies" key="3">
          <TanstackTable
            data={allPayroll.vacancies}
            columns={getVacanciesColumns(
              allPayroll.vacancies,
              handleToggleVacancyPayPeriods,
              allPayroll.previous_months,
            )}
            previousMonths={allPayroll.previous_months}
            tableId="vacancies"
          />
          <a
            className="govuk-button govuk-!-margin-right-2 govuk-button--secondary"
            href={window.addVacancyUrl}
          >
            Add vacancy
          </a>
        </Tab>
        <Tab label="Pay modifiers" key="4">
          <div className="scrollable">
            <DisplayAttrition
              attrition={allPayroll.pay_modifiers.attrition}
              global_attrition={allPayroll.pay_modifiers.global_attrition}
              onInputChange={handleUpdateAttrition}
              onCreate={handleCreateAttrition}
            />
            <DisplayPayModifier
              modifier={allPayroll.pay_modifiers.pay_uplift}
              title="Pay uplift"
            />
          </div>
        </Tab>
      </Tabs>
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

function updateAttrition(data, action) {
  const updatedAttrition = data.map((value, index) => {
    if (index === action.index) {
      return parseFloat(action.value);
    }
    return value;
  });

  return updatedAttrition;
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
    case "updateAttrition": {
      return {
        ...data,
        pay_modifiers: {
          attrition: updateAttrition(data.pay_modifiers.attrition, action),
          pay_uplift: data.pay_modifiers.pay_uplift,
        },
      };
    }
  }
};
