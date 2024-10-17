import { useEffect, useReducer } from "react";

import EditPayroll from "../Components/EditPayroll";
import * as api from "../Components/EditPayroll/api";

const initialPayrollState = [];

export default function Payroll() {
  const [payroll, dispatch] = useReducer(payrollReducer, initialPayrollState);

  useEffect(() => {
    api.getPayrollData().then((data) => dispatch({ type: "fetched", data }));
  }, []);

  // Handlers
  function handleLogPayroll() {
    dispatch({ type: "logged" });
  }

  function handleTogglePayPeriods(employeeNo, index, enabled) {
    dispatch({ type: "updatePayPeriods", employeeNo, index, enabled });
  }

  return (
    <EditPayroll
      payroll={payroll}
      onLogPayroll={handleLogPayroll}
      onTogglePayPeriods={handleTogglePayPeriods}
    />
  );
}

function payrollReducer(payroll, action) {
  switch (action.type) {
    case "fetched": {
      return action.data;
    }
    case "logged": {
      console.log(payroll);
      return payroll;
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
