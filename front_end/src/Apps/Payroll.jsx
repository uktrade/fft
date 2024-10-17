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
      payroll.map((employeeRow) => {
        if (employeeRow.employeeNo == action.employeeNo)
          for (let i = index + 1; i < 12; i++) {
            employeeRow.pay_periods[i].value = !enabled;
          }
        console.log("MODIFIED PAYROLL", payroll);
        return payroll;
      });
    }
  }
}
