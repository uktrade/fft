
export const SET_MOUSE_DOWN = 'SET_MOUSE_DOWN';

const mouseInitial = {
    down: false
};

export const mouse = (state = mouseInitial, action) => {
    switch (action.type) {
        case SET_MOUSE_DOWN:
            return Object.assign({}, state, {
                down: action.down
            });
        default:
            return state;
    }
}
