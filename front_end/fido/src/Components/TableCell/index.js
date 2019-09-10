import React, {Fragment, useState, useEffect, useRef } from 'react';


function TableCell({children}) {
	const [cellContent, setCellContent] = useState("test");
	const [editMode, setEditMode] = useState(false);
	const cellRef = useRef(null);

    useEffect(() => {
		document.addEventListener("click", function(e) {
			console.log(cellRef);
			console.log(e);
		});
    }, []);

	return (
		<Fragment>
			<td 
				ref={cellRef}
				onClick={() => { 
					setEditMode(true);
				}
			}>
				{editMode ? (
				<input 
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
