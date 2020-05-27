import React, {Fragment} from 'react'
import { useSelector } from 'react-redux'

const VariancePercentage = ({rowIndex}) => {
    const row = useSelector(state => state.allCells.cells[rowIndex]);
    let className = ''
    let percentage = null
    let budget = Number(row["budget"].value)

    if (budget === 0) {
        percentage = 'No Budget'
    } else {
        let total = 0

        for (let i = 1; i < 13; i++) {
            if (!row[i])
                continue

            total += row[i].amount
        }

        let difference = budget - total
        percentage =  Math.round((difference/budget) * 100)

        if (total < 0) {
            className='negative'
        }

        percentage = percentage + '%'
    }

    return (
        <Fragment><span id={"var_spend_" + rowIndex} className={className}>{percentage}</span></Fragment>
    );
}

export default VariancePercentage
