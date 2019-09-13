import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import {
	SET_INITIAL_CELL,
	SET_LAST_CELL,
	ADD_SELECTED_CELL
} from '../../Reducers/Selection'
import { 
	ADD_CELL,
	SET_EDITING
} from '../../Reducers/Cells'

function TableCell({children, cellId}) {
    const dispatch = useDispatch();

	const [cellContent, setCellContent] = useState("test");
	const [editMode, setEditMode] = useState(false);

	let cellRef = React.createRef();
	const inputRef = useRef(null);

	const selectedCells = useSelector(state => state.selection.cells);
	const intialCell = useSelector(state => state.selection.intialCell);

	const mouseDn = useSelector(state => state.mouse.down);

    const allCells = useSelector(state => state.allCells.allCells);

	const checkInteraction = (e) => {
		if (editMode && e.target != inputRef.current) {
			setEditMode(false);
		}
	}

	const selectCell = () => {
		if (mouseDn) {
	        // dispatch({
	        //     type: ADD_SELECTED_CELL,
	        //     cell: cellId
	        // });

	        dispatch({
	            type: SET_LAST_CELL,
	            cell: cellId
	        });
		}
	}

    useEffect(() => {
        dispatch({
            type: ADD_CELL,
            id: "id_" + cellId,
            rect: cellRef.current.getBoundingClientRect()
        });
    }, []);

	useEffect(() => {
		if (inputRef && inputRef.current) {
			inputRef.current.focus();
		}
	});

	const isSelected = () => {
		let cellData = allCells["id_" + cellId];
		if (cellData && cellData.selected) {
			return true;
		}

		return false
	}

	const isEditing = () => {
		let cellData = allCells["id_" + cellId];
		if (cellData && cellData.isEditing) {
			return true;
		}

		return false
	}

	return (
		<Fragment>
			<td
				className={isSelected() ? 'highlight' : 'no-select'}
				ref={cellRef}

				onDoubleClick={ () => { 
					dispatch({
						type: SET_EDITING,
						cell: cellId
					});
				}}

				onMouseOver={ () => { 
					selectCell();
				}}

				onMouseDown={ () => {
					dispatch({
						type: SET_INITIAL_CELL,
						cell: cellId
					});
				}}
			>
				{isEditing() ? (
					<input
						ref={inputRef}
						type="text"
						value={cellContent}
						onChange={e => setCellContent(e.target.value)}
					/>
				) : (
					<Fragment>
						{cellId}:
						{cellContent}
					</Fragment>
				)}
			</td>
      	</Fragment>
	);
}

export default TableCell;
