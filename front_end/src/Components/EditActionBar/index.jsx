import React, { Fragment } from "react";
import ReactDOM from "react-dom";
import { useSelector, useDispatch } from "react-redux";
import { TOGGLE_ITEM, TOGGLE_SHOW_ALL } from "../../Reducers/HiddenCols";
import { TOGGLE_FILTER } from "../../Reducers/Filter";

const EditActionBar = () => {
  const dispatch = useDispatch();
  const hiddenCols = useSelector((state) => state.hiddenCols.hiddenCols);
  const showAll = useSelector((state) => state.hiddenCols.showAll);
  const filterOpen = useSelector((state) => state.filter.open);

  const getClasses = () => {
    let classes = "action-bar-content-wrapper ";

    if (filterOpen) classes += "action-bar-open";

    return classes;
  };

  const getArrowClass = () => {
    if (filterOpen) return "arrow-up";

    return "arrow-down";
  };

  const getComponent = () => {
    return (
      <Fragment>
        <div className="action-bar-by">
          <button
            id="action-bar-switch"
            className="link-button govuk-link"
            onClick={(e) => {
              dispatch(TOGGLE_FILTER());
              e.preventDefault();
            }}
          >
            Show/hide columns
          </button>
          <span className={getArrowClass()}></span>
        </div>
        <div className={getClasses()}>
          <div className="action-bar-content">
            <h3 className="govuk-heading-s">Show/hide columns</h3>
            <div className="govuk-checkboxes govuk-checkboxes--small">
              <div className="govuk-checkboxes__item">
                <input
                  type="checkbox"
                  className="govuk-checkboxes__input"
                  checked={showAll}
                  onChange={(e) => {
                    dispatch(TOGGLE_SHOW_ALL());
                  }}
                />
                <label className="govuk-label govuk-checkboxes__label">
                  All info columns
                </label>
              </div>
            </div>

            <div className="action-bar-cols">
              <h4 className="govuk-heading-s">Individual columns</h4>
              <div className="govuk-checkboxes govuk-checkboxes--small">
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="nac_code"
                    id="show_hide_nac"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("nac_code") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("nac_code"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="nac_code"
                  >
                    NAC code
                  </label>
                </div>
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="nac_description"
                    id="show_hide_nac"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("nac_description") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("nac_description"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="nac_description"
                  >
                    NAC description
                  </label>
                </div>
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="programme_code"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("programme_code") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("programme_code"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="programme_code"
                  >
                    Programme code
                  </label>
                </div>
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="programme_description"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("programme_description") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("programme_description"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="programme_description"
                  >
                    Programme description
                  </label>
                </div>
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="analysis1_code"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("analysis1_code") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("analysis1_code"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="analysis1_code"
                  >
                    Analysis 1
                  </label>
                </div>
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="analysis2_code"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("analysis2_code") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("analysis2_code"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="analysis2_code"
                  >
                    Analysis 2
                  </label>
                </div>
                <div className="govuk-checkboxes__item">
                  <input
                    type="checkbox"
                    name="project_code"
                    className="govuk-checkboxes__input"
                    checked={hiddenCols.indexOf("project_code") === -1}
                    onChange={(e) => {
                      dispatch(TOGGLE_ITEM("project_code"));
                    }}
                  />
                  <label
                    className="govuk-label govuk-checkboxes__label"
                    htmlFor="project_code"
                  >
                    Project Code
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Fragment>
    );
  };

  return ReactDOM.createPortal(
    getComponent(),
    document.getElementById("action-bar"),
  );
};

export default EditActionBar;
