export const monthsWithActuals = (previousMonths) => {
  return previousMonths
    .filter((month) => month.is_actual)
    .map((month) => month.short_name.toLowerCase());
};
