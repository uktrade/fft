import { useEffect, useReducer, useState } from "react";

import EditPayroll from "../Components/EditPayroll";
import * as api from "../Components/EditPayroll/api";

const initialPayrollState = [];

export default function Payroll() {
  const [payroll, dispatch] = useReducer(payrollReducer, initialPayrollState);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    const savedSuccessFlag = localStorage.getItem("saveSuccess");
    if (savedSuccessFlag === "true") {
      setSaveSuccess(true);
      localStorage.removeItem("saveSuccess");
    }

    api.getPayrollData().then((data) => dispatch({ type: "fetched", data }));
  }, []);

  // Handlers
  async function handleSavePayroll() {
    try {
      api.postPayrollData(payroll);

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

  return (
    <EditPayroll
      payroll={payroll}
      onSavePayroll={handleSavePayroll}
      onTogglePayPeriods={handleTogglePayPeriods}
      saveSuccess={saveSuccess}
    />
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