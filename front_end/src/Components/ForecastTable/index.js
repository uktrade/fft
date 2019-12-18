import React, {Fragment, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import Table from '../../Components/Table/index'
import { TOGGLE_NAC, TOGGLE_PROG } from '../../Reducers/ShowHideCols'
import { SET_ERROR } from '../../Reducers/Error'

import { SET_CELLS } from '../../Reducers/Cells'

import {
    postData,
    processForecastData
} from '../../Util'


function ForecastTable() {
    const dispatch = useDispatch();

    const errorMessage = useSelector(state => state.error.errorMessage)
    const selectedRow = useSelector(state => state.selected.selectedRow)
    const allSelected = useSelector(state => state.selected.all)

    const cells = useSelector(state => state.allCells.cells);

    useEffect(() => {
        const timer = () => {
                setTimeout(() => {
                if (window.table_data) {
                    let rows = processForecastData(window.table_data)

                    console.log(rows)
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

            postData(
                `/forecast/paste-forecast/${window.cost_centre}/`,
                payload
            ).then((response) => {
                if (response.status === 200) {
                    let rows = processForecastData(response.data)
                      dispatch({
                        type: SET_CELLS,
                        cells: rows
                      })
                } else {
                    dispatch(
                        SET_ERROR({
                            errorMessage: response.data.error
                        })
                    );
                }
            })
        }

        capturePaste();
        //window.addEventListener("mousedown", captureMouseDn);
        //window.addEventListener("mouseup", captureMouseUp);
        document.addEventListener("paste", capturePaste)
        // window.addEventListener("keydown", handleKeyDown);
        // window.addEventListener("copy", setClipBoardContent);

        return () => {
           //window.removeEventListener("onmouseup", captureMouseUp);
            //window.removeEventListener("mousedown", captureMouseDn);
            document.removeEventListener("paste", capturePaste)
            // window.removeEventListener("keydown", handleKeyDown);
            // window.removeEventListener("copy", setClipBoardContent);
        };
    }, [dispatch, cells, selectedRow, allSelected]);

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
            <p>
                <button
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_NAC()
                        );
                        e.preventDefault()
                    }}
                >Toggle NAC</button>
            </p>
            <p>
                <button
                    onClick={(e) => {
                        dispatch(
                            TOGGLE_PROG()
                        );
                        e.preventDefault()
                    }}
                >Toggle programme</button>
            </p>
            <Table />
        </Fragment>
    );
}

export default ForecastTable;
