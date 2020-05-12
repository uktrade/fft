import React, { Fragment, useEffect, useState } from 'react'

const CostCentreList = ({rowIndex, cellKey, format}) => {
    const [costCentres, setCostCentres] = useState([])
    const [displayedCentres, setDisplayedCentres] = useState([])

    useEffect(() => {
        const timer = () => {
            setTimeout(() => {
                if (window.costCentres) {
                    setCostCentres(window.costCentres)
                    setDisplayedCentres(window.costCentres)
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
            <h3 className="govuk-heading-m">You have access to {costCentres.length} cost centres</h3>
            <input placeholder="Filter your cost centres" type="text" className="govuk-input"
                onChange={(e) => {
                    filterCostCentres(e.target.value);
                }}
            />
            <ul className="cost-centre-list">
              {displayedCentres.map((costCentre, index) => {
                return <li key={index}>
                    <a href={ `/forecast/edit/${costCentre.code}/` } className="govuk-link">{costCentre.code} - {costCentre.name}</a>
                </li>
              })}
            </ul>
        </Fragment>
    )
}

export default CostCentreList
