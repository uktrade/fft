import React from 'react'
import { useSelector } from 'react-redux'

const TotalVariancePercentage = ({rowIndex, id}) => {
    const rows = useSelector(state => state.allCells.cells);

    let budget = 0
    let total = 0
    let negative = ''
    let percentage = null

    // eslint-disable-next-line
    for (const row of rows) {
        let rowTotal = 0
        for (let i = 1; i < 13; i++) {
            if (!row[i])
                continue

            rowTotal += row[i].amount
        }
        budget += row["budget"].value
        total += rowTotal
    }

    if (budget === 0) {
        percentage = 'No Budget'
    } else {
        let difference = budget - total
        percentage =  Math.round((difference/budget) * 100)
        
        if (percentage < 0) {
            negative='negative'
        }

        percentage = percentage + '%'
    }

    return (
        <td id={id} className={"govuk-table__cell total-figure forecast-month-cell not-editable figure-cell " + negative }>{percentage}</td>
    );
}

export default TotalVariancePercentage
