import React from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const TotalCol = ({month}) => {
    const cells = useSelector(state => state.allCells.cells);

    let total = 0

    // eslint-disable-next-line
    for (const cell of cells) {
        if (!cell[month])
            continue

        total += cell[month].amount
    }

    const getClasses = () => {
        return "govuk-table__cell total-figure forecast-month-cell not-editable figure-cell " + (total < 0 ? 'negative' : '')
    }

    return (
        <td
            className={getClasses()}
            id={"col_total_" + month}
        >
            {formatValue(total / 100)}
        </td>
    );
}

export default TotalCol
