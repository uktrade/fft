import React, {Fragment, useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Table from '../../Components/MyHREmployeeTable/index.jsx'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { store } from '../../Store';
import EditActionBar from '../../Components/EditActionBar/index'

import { SET_ERROR } from '../../Reducers/Error'
import { OPEN_FILTER_IF_CLOSED } from '../../Reducers/Filter'
import { SET_MYHR_EMPLOYEE_SELECTED_ROW, SELECT_ALL, UNSELECT_ALL } from '../../Reducers/Selected'
import {
    getCellId, processGroupData,
} from '../../Util'
import {SET_MYHR_EMPLOYEE_CELLS} from "../../Reducers/Cells.js";


function MyHREmployee() {
    console.log("MyHREmployee component has been rendered");
    const dispatch = useDispatch();

    const errorMessage = useSelector(state => state.error.errorMessage)
    const selectedRow = useSelector(state => state.selected.myHREmployeeSelectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const cells = useSelector(state => state.allCells.myhrEmployeeCells);
    const editCellId = useSelector(state => state.edit.cellId);

    const [sheetUpdating, setSheetUpdating] = useState(false)

    useEffect(() => {
        if (window.myhr_group_data) {
            console.log('MyHR Employee Data:', window.myhr_group_data);
        } else {
            console.log('MyHR Employee is not available');
        }
    }, []);

    useEffect(() => {
        const timer = () => {
                setTimeout(() => {
                if (window.myhr_group_data) {
                    let rows = processGroupData(window.myhr_group_data)
                      dispatch({
                        type: SET_MYHR_EMPLOYEE_CELLS,
                        cells: rows
                      })
                } else {
                    timer()
                }
            }, 100);
        }

        timer()
    }, [dispatch])

    useEffect(() => {
        const capturePaste = (event) => {
            if (!event)
                return

            if (selectedRow < 0 && !allSelected) {
                return
            }

            dispatch(
                SET_ERROR({
                    errorMessage: null
                })
            );

            let clipBoardContent = event.clipboardData.getData('text/plain')
            let crsfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value

            let payload = new FormData()
            payload.append("paste_content", clipBoardContent)
            payload.append("csrfmiddlewaretoken", crsfToken)

            if (allSelected) {
                payload.append("all_selected", allSelected)
            } else {
                if (selectedRow > -1) {
                    payload.append("pasted_at_row", JSON.stringify(cells[selectedRow]))
                }
            }

            setSheetUpdating(true)
        }

        capturePaste()
        document.addEventListener("paste", capturePaste)

        return () => {
            document.removeEventListener("paste", capturePaste)
        };
    }, [dispatch, cells, selectedRow, allSelected]);

    useEffect(() => {
        const handleKeyDown = (event) => {
            // This function puts editing cells into the tab order of the page
            let lowestMonth = 0
            let body = document.getElementsByTagName("BODY")[0]
            let skipLink = document.getElementsByClassName("govuk-skip-link")[0]
            let filterOpenLink = document.getElementById("action-bar-switch")
            let selectAll = document.getElementById("select_all")

            const state = store.getState();

            if (event.key === "Tab") {
                // See if users has hit open filter link
                if (document.activeElement === filterOpenLink) {
                    dispatch(
                        OPEN_FILTER_IF_CLOSED()
                    );
                    return
                }
                // See if we need to open filter because of a backwards tab from select all
                if (event.shiftKey && document.activeElement === selectAll) {
                    dispatch(
                        OPEN_FILTER_IF_CLOSED()
                    );
                    return
                }

                let targetRow = -1
                let nextId = null

                // Check for select button
                if (editCellId) {
                    let parts = state.edit.cellId.split("_")
                    targetRow = parseInt(parts[1], 10)
                } else if (document.activeElement.className === "select_row_btn govuk-link link-button") {
                    let parts = document.activeElement.id.split("_")
                    targetRow = parseInt(parts[2], 10)
                }

                if (event.shiftKey &&
                    editCellId === null && (
                    document.activeElement === body ||
                    document.activeElement === skipLink
                )) {
                    targetRow = cells.length - 1

                    nextId = getCellId(targetRow, maxMonth)

                    event.preventDefault()
                    document.activeElement.blur();

                    dispatch(
                        SET_EDITING_CELL({
                            "cellId": nextId
                        })
                    );
                }
            }
        }

        const handleMouseDown = (event) => {
            let active = document.activeElement

            if (active.tagName !== "INPUT") {
                dispatch(
                    SET_EDITING_CELL({
                        "cellId": null
                    })
                );
            }
        }

        window.addEventListener("mousedown", handleMouseDown);
        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
            window.removeEventListener("mousedown", handleMouseDown);
        };
    }, [dispatch, cells, editCellId, allSelected, selectedRow]);

    return (
        <Fragment>
            {errorMessage != null &&
                <div className="govuk-error-summary" aria-labelledby="error-summary-title" role="alert" tabIndex="-1" data-module="govuk-error-summary">
                  <h2 className="govuk-error-summary__title" id="error-summary-title">
                    There is a problem
                  </h2>
                  <div className="govuk-error-summary__body">
                    <ul className="govuk-list govuk-error-summary__list">
                      <li id="paste_error_msg">
                        {errorMessage}
                      </li>
                    </ul>
                  </div>
                </div>
            }
            <EditActionBar />          
            <Table sheetUpdating={sheetUpdating} />
        </Fragment>
    );
}

export default MyHREmployee
