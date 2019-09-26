import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';

import RowContext from '../../Components/RowContext'

function TableHandle({rowIndex}) {
	const context = useContext(RowContext)

	return (
		<td className="handle"
			onClick={() => { 
				context.selectRow(rowIndex);
			}
		}>
			{rowIndex}
		</td>
	);
}

export default TableHandle;
