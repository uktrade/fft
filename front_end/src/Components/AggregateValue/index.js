import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const AggregateValue = ({rowIndex, actualsOnly}) => {
    const cells = useSelector(state => state.allCells.cells[rowIndex]);
    let className = ''

    let total = 0

    for (let i = 1; i < 13; i++) {
        if (!cells[i] || (actualsOnly && cells[i].isEditable))
            continue

        total += cells[i].amount
    }

    if (total < 0) {
        className='negative'
    }

    return (
        <Fragment><span id={(actualsOnly ? 'to_date_total_' : 'year_total_') + rowIndex} className={className}>{formatValue(total / 100)}</span></Fragment>
    );
}

export default AggregateValue
