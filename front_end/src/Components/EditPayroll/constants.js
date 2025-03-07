const monthHeaders = [
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
  "Jan",
  "Feb",
  "Mar",
];

export const payrollHeaders = [
  "Name",
  "Grade",
  "Employee No",
  "FTE",
  "Programme Code",
  "Budget Type",
  "Assignment Status",
]
  .concat(monthHeaders)
  .concat(["Notes"]);

export const vacancyHeaders = [
  "Manage",
  "Recruitment Type",
  "Grade",
  "Programme Code",
  "Budget Type",
  "Appointee Name",
  "Hiring Manager",
  "HR Ref",
  "Recruitment Stage",
]
  .concat(monthHeaders)
  .concat(["Notes"]);
