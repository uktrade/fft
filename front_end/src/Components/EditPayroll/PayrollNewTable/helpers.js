export const monthsWithActuals = (previousMonths) => {
  return previousMonths
    .filter((month) => month.is_actual)
    .map((month) => month.short_name.toLowerCase());
};

export const totalOfColumn = (data, callback) =>
  data.reduce((acc, cur) => acc + callback(cur), 0);
