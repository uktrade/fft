import React, {Fragment, useState, useEffect, useRef, useContext } from 'react';

import RowContext from '../../Components/RowContext'

function ColumnHeader({index}) {
	const context = useContext(RowContext)

	return (
		<th className="column-header"
			onClick={() => {
				context.selectColumn(index);
			}
		}>
			Column {index}
		</th>
	);
}

export default ColumnHeader;
