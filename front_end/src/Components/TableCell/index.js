import React, {Fragment, useState, useCallback, useEffect, useRef, useContext, memo } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import {
    getCellId,
    months
} from '../../Util'
import { SET_INITIAL, SET_LAST } from '../../Reducers/Select'
import { SET_EDIT_CELL } from '../../Reducers/Edit'

const TableCell = ({index, cellId, initialValue, selected, selectInitialCell, row, col, mouseOverCell, mouseUpOnCell, setRect}) => {
    const dispatch = useDispatch();

    let cellRef = React.createRef();
    const inputRef = useRef(null);

    const [isEditing, setIsEditing] = useState(false);


    const [value, setValue] = useState(initialValue);

    //const [rect, setRect] = useState(null);

    // console.log("Re-rendering...");

    // const selectCell = () => {
    //     if (window.mouseDown) {
    //         dispatch(
    //             SELECT_CELL({
    //                 id: cellId
    //             })
    //         );

    //         dispatch(
    //             SET_LAST_CELL({
    //                 id: cellId
    //             })
    //         );
    //     }
    // }

    useEffect(() => {
        setRect(cellId, row, cellRef.current.getBoundingClientRect())
    }, [])

    // useEffect(() => {
    //     if (inputRef && inputRef.current) {
    //         inputRef.current.focus();
    //     }
    // });

    const isSelected = () => {
        // let cellData = thisCell;

        // if (cellData && cellData.selected) {
        //     return true;
        // }

        // return false

        return false
    }

    const handleKeyPress = (event) => {
        // if(event.key === 'Enter'){
        //     dispatch({
        //         type: SET_EDIT_CELL,
        //         cellId: null
        //     });
        // }
    }

    //console.log("re-render cell")

    const setContentState = (value) => {
        if (!parseInt(value)) {
            return
        }

        setValue(value)
    }

    //sconsole.log("Cell ids: ",editCellId, cellId)

    return (
        <Fragment>
            <td
                className={selected ? 'highlight govuk-table__cell' : 'no-select govuk-table__cell'}
                ref={cellRef}
                onDoubleClick={ () => {
                    console.log("cellId", cellId)
                    dispatch(
                        SET_EDIT_CELL({
                            rect: cellRef.current.getBoundingClientRect(),
                            content: value
                        })
                    )
                }}

                onMouseOver={ () => {
                    mouseOverCell(cellId, row, col, cellRef.current.getBoundingClientRect())
                }}

                onMouseUp={ () => {
                    mouseUpOnCell(cellId, row, col)
                }}

                onMouseDown={ () => {
                    selectInitialCell(cellId, row, col, cellRef.current.getBoundingClientRect())
                }}
            >
                {1 == 2 ? (
                    <input
                        className="cell-input"
                        ref={inputRef}
                        type="text"
                        value={value}
                        onChange={e => setContentState(e.target.value)}
                        onKeyPress={handleKeyPress}
                    />
                ) : (
                    <Fragment>
                        {value}
                    </Fragment>
                )}
            </td>
        </Fragment>
    );
}

const comparisonFn = function(prevProps, nextProps) {
    return (
        prevProps.editing === nextProps.editing &&
        prevProps.selected === nextProps.selected
    )
};

export default memo(TableCell, comparisonFn);
