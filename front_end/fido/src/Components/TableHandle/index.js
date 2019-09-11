import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';

import RowContext from '../../Components/RowContext'

function TableHandle() {
	const context = useContext(RowContext)

	return (
		<td
			onClick={() => { 
				context.selectRow();
			}
		}>
			HANDLE
		</td>
	);
}

export default TableHandle;
