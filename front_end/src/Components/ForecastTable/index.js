import React, {Fragment, useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Table from '../../Components/Table/index'
import { SET_EDITING_CELL } from '../../Reducers/Edit'
import { store } from '../../Store';
import { 
    TOGGLE_NAC,
    TOGGLE_PROG, 
    TOGGLE_AN1,
    TOGGLE_AN2,
    TOGGLE_PROJ_CODE,

} from '../../Reducers/ShowHideCols'
import { SET_ERROR } from '../../Reducers/Error'
import { SET_CELLS } from '../../Reducers/Cells'

import {
    getCellId,
    postData,
    processForecastData
} from '../../Util'


function ForecastTable() {
    const dispatch = useDispatch();

    const nac = useSelector(state => state.showHideCols.nac);
    const programme = useSelector(state => state.showHideCols.programme);
    const analysis1 = useSelector(state => state.showHideCols.analysis1);
    const analysis2 = useSelector(state => state.showHideCols.analysis2);
    const projectCode = useSelector(state => state.showHideCols.projectCode);

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
            let next_id = null
            let footerLink = document.getElementsByClassName("govuk-footer__link")[0]

            if (event.key === "Tab") {
                console.log("document.activeElement.className", document.activeElement.className)

                if (document.activeElement.className === "select_row_btn link-button") {
                    let parts = document.activeElement.id.split("_")
                    let row = parseInt(parts[2])

                    if (event.shiftKey) {
                        if (row === 0) {
                            return
                        } else {
                            next_id = getCellId(3, (row - 1))
                        }
                    } else {
                        next_id = getCellId(4 + window.actuals.length, row)
                    }

                    document.activeElement.blur();
                    event.preventDefault()
                } else if (event.shiftKey && document.activeElement === footerLink) {
                    next_id = getCellId(3, cells.length - 1)
                    document.activeElement.blur();
                    event.preventDefault()
                } else {
                    if (!editCellId)
                        return
                }

                if (!next_id) {
                    const state = store.getState();

                    if (!state.edit.cellId)
                        return

                    let idParts = state.edit.cellId.split("_")

                    let month = parseInt(idParts[1])
                    let rowIndex = parseInt(idParts[2])

                    if (event.shiftKey) { // reverse tab
                        // check for start of table
                        if (rowIndex === 0 && month === (4 + window.actuals.length)) {
                            let selectRowBtn = document.getElementById("select_row_0")
                            selectRowBtn.focus()
                            next_id = null
                            event.preventDefault()
                        } else {
                            // 4 is march and the end of the financial year
                            if (month === (4 + window.actuals.length)) {
                                let selectRowBtn = document.getElementById("select_row_" + rowIndex)
                                selectRowBtn.focus()
                                next_id = null
                            } else if (month === 1) { // 1 is april, the start of fin year
                                month = 13
                                next_id = getCellId(month - 1, rowIndex)
                            } else {
                                next_id = getCellId(month - 1, rowIndex)
                            }
                            event.preventDefault()
                        }
                    } else { // tab
                        // check for end of table
                        if (rowIndex === (cells.length - 1) && month === 3) {
                            next_id = null
                            footerLink.focus()
                            event.preventDefault()
                        } else {
                            if (month === 12) { // allow for financial year
                                month = 0
                                next_id = getCellId(month + 1, rowIndex)
                            } else if (month === 3) { // jump to select to btn if 3
                                rowIndex++
                                let selectRowBtn = document.getElementById("select_row_" + rowIndex)
                                selectRowBtn.focus()
                                next_id = null
                            } else {
                                next_id = getCellId(month + 1, rowIndex)
                            }
                            event.preventDefault()
                        }
                    }
                }

                dispatch(
                    SET_EDITING_CELL({
                        "cellId": next_id
                    })
                );
            }
        }

        window.addEventListener("keydown", handleKeyDown);

        return () => {
            window.removeEventListener("keydown", handleKeyDown);
        };
    }, [dispatch, cells, editCellId]);

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
                    className="link-button"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_NAC()
                        );
                        e.preventDefault()
                    }}
                >{nac ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} NAC</button>
                <button id="show_hide_prog"
                    className="link-button"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_PROG()
                        );
                        e.preventDefault()
                    }}
                >{programme ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} programme</button>
                <button id="show_hide_a1"
                    className="link-button"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_AN1()
                        );
                        e.preventDefault()
                    }}
                >{analysis1 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} analysis code sector</button>
                <button id="show_hide_a2"
                    className="link-button"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_AN2()
                        );
                        e.preventDefault()
                    }}
                >{analysis2 ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} analysis code market</button>
                <button id="show_hide_proj"
                    className="link-button"
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_PROJ_CODE()
                        );
                        e.preventDefault()
                    }}
                >{projectCode ? (
                        <Fragment>Hide</Fragment>
                    ) : (
                        <Fragment>Show</Fragment>
                    )} project code</button>
            </div>            
            <Table sheetUpdating={sheetUpdating} />
        </Fragment>
    );
}

export default ForecastTable;
