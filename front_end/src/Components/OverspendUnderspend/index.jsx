import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'
import {
    formatValue
} from '../../Util'

const OverspendUnderspend = ({rowIndex}) => {
    const row = useSelector(state => state.allCells.cells[rowIndex]);
    let budget = row["budget"].value

    let className = ''

    let total = 0

    for (let i = 1; i < 13; i++) {
        if (!row[i])
            continue

        total += row[i].amount
    }

    total =  budget - total

    if (total < 0) {
        className='negative'
    }

    return (
        <Fragment><span id={"ou_spend_" + rowIndex} className={className}>{formatValue(total / 100)}</span></Fragment>
    );
}

export default OverspendUnderspend
