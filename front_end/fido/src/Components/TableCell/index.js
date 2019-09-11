import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { ADD_SELECTED_CELL } from '../../Reducers/Selection'
import TableContext from '../../Components/TableContext'

function TableCell({children, cellId}) {
    const dispatch = useDispatch();

	const context = useContext(TableContext);

	const [cellContent, setCellContent] = useState("test");
	const [editMode, setEditMode] = useState(false);

	const cellRef = useRef(null);
	const inputRef = useRef(null);

	const selectedCells = useSelector(state => state.selection.cells);

	const checkInteraction = (e) => {
		if (editMode && e.target != inputRef.current) {
			setEditMode(false);
		}
	}

	const selectCell = () => {
		console.log(context.mouseIsDown);

		//if (mouseIsDown) {
	        // dispatch({
	        //     type: ADD_SELECTED_CELL,
	        //     cell: cellId
	        // });
		//}
	}

    useEffect(() => {
		document.addEventListener("mouseover", selectCell);
		return () => {
			document.removeEventListener("mouseover", selectCell);
		};
    }, [editMode]);

    useEffect(() => {
		document.addEventListener("click", checkInteraction);
		return () => {
			document.removeEventListener("click", checkInteraction);
		};
    }, [editMode]);

	useEffect(() => {
		console.log(inputRef);
		if (inputRef && inputRef.current) {
			inputRef.current.focus();
		}
	});

	const isSelected = () => {
		console.log(selectedCells);


		if (selectedCells.includes(cellId)) {
			return true;
		} else {
			return false;
		}
	}

	return (
		<Fragment>
			<td
				className={isSelected() ? 'highlight' : ''}
				ref={cellRef}

				onDoubleClick={ () => { 
					setEditMode(true);
				}}

				// onClick={ () => { 
				// 	selectCell();
				// }}
			>
				{editMode ? (
					<input
						ref={inputRef}
						type="text"
						value={cellContent}
						onChange={e => setCellContent(e.target.value)}
					/>
				) : (
					<Fragment>
						{cellContent}
					</Fragment>
				)}
			</td>
      	</Fragment>
	);
}

export default TableCell;
