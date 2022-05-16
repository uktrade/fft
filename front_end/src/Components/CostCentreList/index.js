import React, { Fragment, useEffect, useState } from 'react'

const CostCentreList = ({rowIndex, cellKey, format}) => {
    const [costCentres, setCostCentres] = useState([])
    const [displayedCentres, setDisplayedCentres] = useState([])
    const [financialYears, setFinancialYears] = useState([])
    const [forecastFinYear, setForecastFinYear] = useState(null)

    useEffect(() => {
        const timer = () => {
            setTimeout(() => {
                if (window.costCentres && window.financialYears) {
                    setCostCentres(window.costCentres)
                    setDisplayedCentres(window.costCentres)
                    setFinancialYears(window.financialYears)
                    forecastFinYear = financialYears[0]
                } else {
                    timer()
                }
            }, 100);
        }

        timer()
    }, [])

    const filterCostCentres = (searchStr) => {
        let filtered = []
        for (const costCentre of costCentres) {
            if (costCentre.name.toLowerCase().includes(searchStr.toLowerCase())) {
                filtered.push(costCentre)
            } else if (costCentre.code.includes(searchStr.toLowerCase())) {
                filtered.push(costCentre)
            } else if (`${costCentre.code} - ${costCentre.name}`.toLowerCase().includes(searchStr.toLowerCase())) {
                filtered.push(costCentre)
            }
        }
        setDisplayedCentres(filtered) 
    }

    return (
        <Fragment>
            <div class="govuk-form-group">
                <label class="govuk-label" for="sort">Financial Year</label>
                <select class="govuk-select" id="sort" name="sort"
                    onChange={(e) => {
                        forecastFinYear = e.target.value
                    }}
                >
                    {financialYears.map((financialYear, index) => {
                        return <option key={index} value="{financialYear.year}">{financialYear.code}</option>
                    })}
                </select>
            </div>
            <h3 className="govuk-heading-m">You have access to {costCentres.length} cost centres</h3>
            <input placeholder="Filter your cost centres" type="text" className="govuk-input"
                onChange={(e) => {
                    filterCostCentres(e.target.value);
                }}
            />
            <ul className="cost-centre-list">
              {displayedCentres.map((costCentre, index) => {
                return <li key={index}>
                    <a href={ `/forecast/edit/${costCentre.code}/${forecastFinYear.year}` } className="govuk-link">{costCentre.code} - {costCentre.name}</a>
                </li>
              })}
            </ul>
        </Fragment>
    )
}

export default CostCentreList
