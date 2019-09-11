import React, {Fragment, useState, useEffect, useRef } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { RowProvider } from  '../../Components/RowContext'
import { SET_SELECTED_ROW } from '../../Reducers/Selection'

function TableRow({children, index}) {
    const dispatch = useDispatch();
	const [selected, setSelected] = useState(false);
	const selectedRow = useSelector(state => state.selection.row);

	const selectRow = () => {
        dispatch({
            type: SET_SELECTED_ROW,
            row: index
        });
	}

	return (
		<RowProvider value={{ selectRow: selectRow }}>
			<tr className={selectedRow == index ? 'highlight' : ''}>
				{children}
			</tr>
		</RowProvider>
	);
}

export default TableRow;
