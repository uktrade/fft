import React, {Fragment, useState, useEffect, useRef, useContext, memo } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import {
    getCellId,
    months
} from '../../Util'
import { SET_INITIAL, SET_LAST } from '../../Reducers/Select'

const TableCell = ({index, cellId, initialValue, selected, editing, setEditing, selectInitialCell, row, col, mouseOverCell, mouseUpOnCell, setRect}) => {
    const dispatch = useDispatch();

    let cellRef = React.createRef();
    const inputRef = useRef(null);

    //const editCell = useSelector(state => state.editCell.cellId);




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

    const setContentState = (value) => {
        if (!parseInt(value)) {
            return
        }

        setValue(value)
    }

    return (
        <Fragment>
            <td
                className={selected ? 'highlight govuk-table__cell' : 'no-select govuk-table__cell'}
                ref={cellRef}
                onDoubleClick={ () => {
                    setEditing(cellId, row)
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
                {editing ? (
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
