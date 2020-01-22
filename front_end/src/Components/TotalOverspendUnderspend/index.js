import React from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const TotalOverspendUnderspend = ({rowIndex, id}) => {
    const rows = useSelector(state => state.allCells.cells);

    let total = 0
    let negative = ''

    // eslint-disable-next-line
    for (const row of rows) {
        let rowTotal = 0
        for (let i = 1; i < 13; i++) {
            if (!row[i])
                continue

            rowTotal += row[i].amount
        }
        let budget = row["budget"].value
        total += budget - rowTotal
    }
    
    if (total < 0) {
        negative='negative'
    }

    return (
        <td id={id} className={"govuk-table__cell forecast-month-cell not-editable " + negative }>{formatValue(total / 100)}</td>
    );
}

export default TotalOverspendUnderspend
