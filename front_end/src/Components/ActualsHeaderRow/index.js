import React from 'react'

const ActualsHeaderRow = () => {

    let numActuals = 0

    if (window.actuals && window.actuals.length > 0) {
        numActuals = window.actuals.length
    }

    return (
        <tr>
            <th className="govuk-table__head meta-col" colspan="9"></th>
            {numActuals > 0 &&
                <th className="govuk-table__head meta-col" colspan="2">Actuals</th>
            }
            <th className="govuk-table__head meta-col" colspan="{{ 18 - numActuals }}">Forecast</th>
        </tr>
    );
}

export default ActualsHeaderRow
