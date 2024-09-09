import React, {Fragment, useEffect, useState } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import Table from '../../Components/PayrollTable/index'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { store } from '../../Store';
import EditActionBar from '../../Components/EditActionBar/index'

import { SET_ERROR } from '../../Reducers/Error'
import { SET_CELLS } from '../../Reducers/Cells'
import { OPEN_FILTER_IF_CLOSED } from '../../Reducers/Filter'
import { SET_SELECTED_ROW, SELECT_ALL, UNSELECT_ALL } from '../../Reducers/Selected'
import {
    getCellId,
    processPayrollData,
} from '../../Util'


function EditPayrollEmployee() {
    console.log("EditPayroll component has been rendered");
    const dispatch = useDispatch();

    const errorMessage = useSelector(state => state.error.errorMessage)
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const cells = useSelector(state => state.allCells.cells);
    const editCellId = useSelector(state => state.edit.cellId);

    const [sheetUpdating, setSheetUpdating] = useState(false)

    useEffect(() => {
        if (window.payroll_employee_data) {
            console.log('Payroll Data:', window.payroll_employee_data);
        } else {
            console.log('Payroll Data is not available');
        }

        if (window.payroll_employee_monthly_data) {
            console.log('Payroll Monthly Data:', window.payroll_employee_monthly_data);
        } else {
            console.log('Payroll Monthly Data is not available');
        }

    }, []);

    useEffect(() => {
        const timer = () => {
                setTimeout(() => {
                if (window.payroll_employee_data) {
                    let rows = processPayrollData(window.payroll_employee_data)
                      dispatch({
                        type: SET_CELLS,
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

            // postData(
            //     `/forecast/paste-forecast/${window.cost_centre}/${window.financial_year}`,
            //     payload
            // ).then((response) => {
            //     if (response.status === 200) {
            //         setSheetUpdating(false)
            //         let rows = processForecastData(response.data)
            //           dispatch({
            //             type: SET_CELLS,
            //             cells: rows
            //           })
            //     } else {
            //         setSheetUpdating(false)
            //         dispatch(
            //             SET_ERROR({
            //                 errorMessage: response.data.error
            //             })
            //         );
            //     }
            // })
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

            if(event.key === 'Enter') {
                if (document.activeElement.className === "link-button govuk-link") {
                    if (allSelected) {
                        dispatch(
                            UNSELECT_ALL()
                        )
                    } else {
                        dispatch(
                            SELECT_ALL()
                        )
                    }

                    event.preventDefault()
                } else if (document.activeElement.className === "select_row_btn govuk-link link-button") {
                    let parts = document.activeElement.id.split("_")
                    let targetRow = parseInt(parts[2], 10)

                    if (selectedRow === targetRow) {
                        dispatch(
                            SET_SELECTED_ROW({
                                selectedRow: -1
                            })
                        )
                    } else {
                        dispatch(
                            SET_SELECTED_ROW({
                                selectedRow: targetRow
                            })
                        )
                    }
                }
            }

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

export default EditPayrollEmployee
