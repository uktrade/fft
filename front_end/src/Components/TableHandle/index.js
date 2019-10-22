import React, { useContext } from 'react';

import RowContext from '../../Components/RowContext'

function TableHandle({children, rowIndex}) {
	const context = useContext(RowContext)

	return (
		<td className="handle govuk-table__cell indicate-action"
			onClick={() => { 
				context.selectRow(rowIndex);
			}
		}>
			{children}
		</td>
	);
}

export default TableHandle;
