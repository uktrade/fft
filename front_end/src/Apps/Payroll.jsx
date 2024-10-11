import { useEffect, useReducer } from "react";

import EditPayoll from "../Components/EditPayroll";
import * as api from "../Components/EditPayroll/api";

const initialPayrollState = [];

export default function Payroll() {
  const [payroll, dispatch] = useReducer(payrollReducer, initialPayrollState);

  useEffect(() => {
    api.getPayrollData().then((data) => dispatch({ type: "fetched", data }));
  });

  // Handlers
  function handleLogPayroll() {
    dispatch({ type: "logged" });
  }

  return <EditPayoll payroll={payroll} onLogPayroll={handleLogPayroll} />;
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
  }
}
