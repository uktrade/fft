import React, {Fragment, useState, useCallback, useEffect, useRef, useContext, memo } from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';
import { store } from '../../Store';

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
