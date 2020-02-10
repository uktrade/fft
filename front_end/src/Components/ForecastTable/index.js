import React, {Fragment, useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Table from '../../Components/Table/index'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { store } from '../../Store';
import { 
    TOGGLE_ITEM,
} from '../../Reducers/HiddenCols'
import { SET_ERROR } from '../../Reducers/Error'
import { SET_CELLS } from '../../Reducers/Cells'
import { SET_SELECTED_ROW, SELECT_ALL, UNSELECT_ALL } from '../../Reducers/Selected'
import {
    getCellId,
    postData,
    processForecastData,
} from '../../Util'


function ForecastTable() {
    const dispatch = useDispatch();

    const hiddenCols = useSelector(state => state.hiddenCols.hiddenCols)

    const errorMessage = useSelector(state => state.error.errorMessage)
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const cells = useSelector(state => state.allCells.cells);
    const editCellId = useSelector(state => state.edit.cellId);

    const [sheetUpdating, setSheetUpdating] = useState(false)

    useEffect(() => {
        const timer = () => {
                setTimeout(() => {
                if (window.table_data) {
                    let rows = processForecastData(window.table_data)
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
    }, [dispatch]);

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
            let payload = new FormData()
            payload.append("paste_content", clipBoardContent)

            if (allSelected) {
                payload.append("all_selected", allSelected)
            } else {
                if (selectedRow > -1) {
                    payload.append("pasted_at_row", JSON.stringify(cells[selectedRow]))
                }
            }

            setSheetUpdating(true)

            postData(
                `/forecast/paste-forecast/${window.cost_centre}/`,
                payload
            ).then((response) => {
                if (response.status === 200) {
                    setSheetUpdating(false)
                    let rows = processForecastData(response.data)
                      dispatch({
                        type: SET_CELLS,
                        cells: rows
                      })
                } else {
                    setSheetUpdating(false)
                    dispatch(
                        SET_ERROR({
                            errorMessage: response.data.error
                        })
                    );
                }
            })
        }

        capturePaste();
        document.addEventListener("paste", capturePaste)

        return () => {
            document.removeEventListener("paste", capturePaste)
        };
    }, [dispatch, cells, selectedRow, allSelected]);

    useEffect(() => {
        const handleKeyDown = (event) => {
            // This function puts editing cells into the tab order of the page
            let footerLink = document.getElementsByClassName("national-archives")[0]
            let lowestMonth = 0

            if (window.actuals && window.actuals.length > 0) {
                let highestActual = Math.max(...window.actuals)

                if (highestActual) {
                    lowestMonth = highestActual
                }
            }

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
                    let targetRow = parseInt(parts[2])

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
                let targetRow = -1
                let targetMonth = null
                let nextId = null

                // Check for select button
                if (editCellId) {
                    let parts = state.edit.cellId.split("_")
                    targetRow = parseInt(parts[1])
                    targetMonth = parseInt(parts[2])
                } else if (document.activeElement.className === "select_row_btn govuk-link link-button") {
                    let parts = document.activeElement.id.split("_")
                    targetRow = parseInt(parts[2])
                }

                if (event.shiftKey && document.activeElement === footerLink) {
                    targetRow = cells.length - 1
                    targetMonth = 12

                    nextId = getCellId(targetRow, targetMonth)
                    event.preventDefault()
                    document.activeElement.blur();

                    dispatch(
                        SET_EDITING_CELL({
                            "cellId": nextId
                        })
                    );

                    return
                }

                if (targetRow > -1) {
                    if (event.shiftKey) { // We're going backwards
                        if (document.activeElement === footerLink) {
                            targetRow = cells.length
                            targetMonth = 12
                        }
                        else if (!targetMonth) { // See if we're on a select button
                            if (targetRow === 0) { // See if we're at the start of the table
                                dispatch(
                                    SET_EDITING_CELL({
                                        "cellId": null
                                    })
                                )
                                return
                            } else {
                                targetRow--
                                targetMonth = 12
                            }
                        } else { // We're coming from a cell
                            if (targetMonth === (lowestMonth + 1)) { // See if we need to jump to select link
                                let selectRowBtn = document.getElementById("select_row_" + targetRow)
                                selectRowBtn.focus()
                                event.preventDefault()
                                dispatch(
                                    SET_EDITING_CELL({
                                        "cellId": null
                                    })
                                )
                                return
                            } else {
                                targetMonth--
                            }
                        }
                    } else {
                        // Going forwards
                        if (!targetMonth)
                            targetMonth = lowestMonth

                        targetMonth++

                        // Jump to next row if we've reached the end of the current one
                        if (targetMonth > 12) {
                            targetRow++
                            // targetMonth = lowestMonth + 1

                            // Check for end of table
                            if (targetRow > (cells.length - 1)) {
                                dispatch(
                                    SET_EDITING_CELL({
                                        "cellId": null
                                    })
                                );
                                footerLink.focus()
                                event.preventDefault()
                                return
                            }

                            let selectRowBtn = document.getElementById("select_row_" + targetRow)
                            selectRowBtn.focus()
                            event.preventDefault()
                            dispatch(
                                SET_EDITING_CELL({
                                    "cellId": null
                                })
                            )
                            return
                        }

                        if (targetMonth <= lowestMonth) {
                            targetMonth = lowestMonth
                        }
                    }

                    nextId = getCellId(targetRow, targetMonth)

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
            <div className="toggle-links">
                <button id="show_hide_nac"
                    className="link-button govuk-link"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_ITEM("natural_account_code")
                        );
                        e.preventDefault()
                    }}
                >{hiddenCols.indexOf("natural_account_code") === -1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} NAC</button>
                <button id="show_hide_prog"
                    className="link-button govuk-link"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_ITEM("programme")
                        );
                        e.preventDefault()
                    }}
                >{hiddenCols.indexOf("programme") === -1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} programme</button>
                <button id="show_hide_a1"
                    className="link-button govuk-link"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_ITEM("analysis1_code")
                        );
                        e.preventDefault()
                    }}
                >{hiddenCols.indexOf("analysis1_code") === -1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} analysis code sector</button>
                <button id="show_hide_a2"
                    className="link-button govuk-link"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_ITEM("analysis2_code")
                        );
                        e.preventDefault()
                    }}
                >{hiddenCols.indexOf("analysis2_code") === -1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} analysis code market</button>
                <button id="show_hide_proj"
                    className="link-button govuk-link"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_ITEM("project_code")
                        );
                        e.preventDefault()
                    }}
                >{hiddenCols.indexOf("project_code") === -1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} project code</button>
            </div>            
            <Table sheetUpdating={sheetUpdating} />
        </Fragment>
    );
}

export default ForecastTable