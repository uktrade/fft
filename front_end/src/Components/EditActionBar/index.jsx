import React, { Fragment } from "react";
import ReactDOM from "react-dom";
import { useSelector, useDispatch } from "react-redux";
import { TOGGLE_ITEM, TOGGLE_SHOW_ALL } from "../../Reducers/HiddenCols";
import { TOGGLE_FILTER } from "../../Reducers/Filter";
import CheckboxItem from "../Common/CheckboxItem";

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
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("programme_code") === -1}
                  name={"programme_code"}
                  label={"Programme code"}
                />
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("programme_description") === -1}
                  name={"programme_description"}
                  label={"Programme description"}
                />
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("nac_code") === -1}
                  name={"nac_code"}
                  label={"NAC code"}
                />
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("nac_description") === -1}
                  name={"nac_description"}
                  label={"NAC description"}
                />
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("analysis1_code") === -1}
                  name={"analysis1_code"}
                  label={"Analysis 1"}
                />
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("analysis2_code") === -1}
                  name={"analysis2_code"}
                  label={"Analysis 2"}
                />
                <CheckboxItem
                  dispatcher={TOGGLE_ITEM}
                  checked={hiddenCols.indexOf("project_code") === -1}
                  name={"project_code"}
                  label={"Project code"}
                />
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
