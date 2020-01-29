import React from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const TotalAggregate = ({rowIndex, actualsOnly, id}) => {
    const cells = useSelector(state => state.allCells.cells);

    let total = 0
    let negative = ''

    // eslint-disable-next-line
    for (const cell of cells) {
        for (let i = 1; i < 13; i++) {
            if (!cell[i] || (actualsOnly && cell[i].isEditable))
                continue

            total += cell[i].amount
        }
    }

    if (total < 0) {
        negative='negative'
    }

    return (
        <td id={id} className={"govuk-table__cell forecast-month-cell total-figure not-editable " + negative}>{formatValue(total / 100)}</td>
    );
}

export default TotalAggregate
