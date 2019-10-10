import React from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';

const Selection = () => {
    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

    const initial = useSelector(state => state.select.initial);
    const last = useSelector(state => state.select.last);

    let horizontalDirection = LEFT_TO_RIGHT;
    let verticalDirection = TOP_TO_BOTTOM;

    let styles = {}

    // Check for select direction
    if (initial.x > last.x) {
        // left to right
        horizontalDirection = RIGHT_TO_LEFT;
    }

    if (initial.y > last.y) {
        // top to bottom
        verticalDirection = BOTTOM_TO_TOP
    }

    if (horizontalDirection === LEFT_TO_RIGHT) {
        if (verticalDirection === TOP_TO_BOTTOM) {
            styles = {
                left : initial.x + window.scrollX,
                top: initial.y + window.scrollY,
                width: (last.x - initial.x) + initial.width,
                height: (last.y - initial.y) + initial.height
            }
        } else {
            styles = {
                left : initial.x + window.scrollX,
                top: initial.y + window.scrollY,
                width: (last.x - initial.x) + initial.width,
                height: (last.y - initial.y) + initial.height
            }
        }
    } else { // RIGHT_TO_LEFT
        if (verticalDirection === TOP_TO_BOTTOM) {
            styles = {
                left : last.x + window.scrollX,
                top: last.y + window.scrollY,
                width: (initial.x - last.x) + last.width,
                height: (initial.y - last.y) + last.height
            }
        } else {
            styles = {
                left : initial.x + window.scrollX,
                top: initial.y + window.scrollY,
                width: (last.x - initial.x) + initial.width,
                height: (last.y - initial.y) + initial.height
            }
        }
    }

    return (
        <div style={styles} className="selection">

            
        </div>
    )
}

export default Selection;
