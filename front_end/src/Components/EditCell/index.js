import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';

const EditCell = () => {
	const rect = useSelector(state => state.edit.rect);
	const content = useSelector(state => state.edit.content);

	const [value, setValue] = useState(content);

    useEffect(() => {
        setValue(content)
    }, [content])

    const styles = {
        left : rect.x + window.scrollX,
        top: rect.y + window.scrollY,
        width: rect.width,
        height: rect.height
    }

    return (
        <input 
        	style={styles}
        	type="text"
        	className="edit-control"
        	value={value}
        	onChange={(e) => {
        		setValue(e.target.value)
        	}}
        />
    )
}

export default EditCell
