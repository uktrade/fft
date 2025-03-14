import { rankItem } from "@tanstack/match-sorter-utils";

export const monthsWithActuals = (previousMonths) => {
  return previousMonths
    .filter((month) => month.is_actual)
    .map((month) => month.short_name.toLowerCase());
};

export const totalOfColumn = (data, callback) =>
  data.reduce((acc, cur) => acc + callback(cur), 0);

// Documentation: https://tanstack.com/table/v8/docs/guide/fuzzy-filtering
export const fuzzyFilter = (row, columnId, value, addMeta) => {
  const itemRank = rankItem(row.getValue(columnId), value);
  addMeta({ itemRank });
  return itemRank.passed;
};
