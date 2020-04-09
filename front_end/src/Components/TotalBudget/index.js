import React from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const TotalBudget = (id) => {
    const rows = useSelector(state => state.allCells.cells);

    let total = 0

    // eslint-disable-next-line
    for (const row of rows) {
        total += row["budget"].value
    }

    return (
    	<td id={id} className={"govuk-table__cell forecast-month-cell total-figure not-editable figure-cell "}>{formatValue(total / 100)}</td>
    );
}

export default TotalBudget