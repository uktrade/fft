import React, { Fragment, useEffect, useState } from "react";

const CostCentreList = ({ rowIndex, cellKey, format }) => {
  const [costCentres, setCostCentres] = useState([]);
  const [displayedCentres, setDisplayedCentres] = useState([]);
  const [financialYears, setFinancialYears] = useState([]);
  const [forecastFinYearDisplay, setForecastFinYearDisplay] = useState(null);
  const [forecastFinYear, setForecastFinYear] = useState(null);
  const [nextPage, setNextPage] = useState(null);

  useEffect(() => {
    const timer = () => {
      setTimeout(() => {
        if (window.costCentres) {
          setCostCentres(window.costCentres);
          setDisplayedCentres(window.costCentres);
          setForecastFinYearDisplay(window.currentFinancialYearDisplay);
          setForecastFinYear(window.currentFinancialYear);
          if (window.financialYears) {
            setFinancialYears(window.financialYears);
          }
          setNextPage(window.nextPage);
        } else {
          timer();
        }
      }, 100);
    };

    timer();
  }, []);

  const filterCostCentres = (searchStr) => {
    let filtered = [];
    for (const costCentre of costCentres) {
      if (costCentre.name.toLowerCase().includes(searchStr.toLowerCase())) {
        filtered.push(costCentre);
      } else if (costCentre.code.includes(searchStr.toLowerCase())) {
        filtered.push(costCentre);
      } else if (
        `${costCentre.code} - ${costCentre.name}`
          .toLowerCase()
          .includes(searchStr.toLowerCase())
      ) {
        filtered.push(costCentre);
      }
    }
    setDisplayedCentres(filtered);
  };

  return (
    <Fragment>
      {financialYears.length > 0 && (
        <div className="govuk-form-group">
          <label className="govuk-label" htmlFor="sort">
            Choose financial year
          </label>
          <select
            className="govuk-select"
            id="sort"
            name="sort"
            onChange={(e) => {
              setForecastFinYearDisplay(
                e.target.options[e.target.selectedIndex].label.toLowerCase(),
              );
              setForecastFinYear(e.target.value);
            }}
          >
            {financialYears.map((financialYear, index) => {
              return (
                <option key={index} value={financialYear.financial_year}>
                  {financialYear.financial_year_display}
                </option>
              );
            })}
          </select>
        </div>
      )}
      <h3 className="govuk-heading-m">
        You have access to {costCentres.length} cost centres for the{" "}
        {forecastFinYearDisplay} financial year
      </h3>
      <input
        placeholder="Search your cost centres"
        type="text"
        className="govuk-input"
        onChange={(e) => {
          filterCostCentres(e.target.value);
        }}
      />
      <ul className="cost-centre-list">
        {displayedCentres.map((costCentre, index) => {
          return (
            <li key={index}>
              <a
                href={`/${nextPage}/edit/${costCentre.code}/${forecastFinYear}`}
                className="govuk-link"
              >
                {costCentre.code} - {costCentre.name}
              </a>
            </li>
          );
        })}
      </ul>
    </Fragment>
  );
};

export default CostCentreList;
