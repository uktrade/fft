export const SET_CELLS = 'SET_CELLS';
export const SET_EMPLOYEE_CELLS = 'SET_EMPLOYEE_CELLS';
export const SET_NON_EMPLOYEE_CELLS = 'SET_NON_EMPLOYEE_CELLS';

const cellsInitial = {
    cells: [],
    employeeCells: [],
    nonEmployeeCells: []
};


export const allCells = (state = cellsInitial, action) => {
    switch (action.type) {
        case SET_CELLS:
            return Object.assign({}, state, {
                cells: action.cells
            });
        case SET_EMPLOYEE_CELLS:
            return Object.assign({}, state, {
                employeeCells: action.cells
            });
        case SET_NON_EMPLOYEE_CELLS:
            return Object.assign({}, state, {
                nonEmployeeCells: action.cells
            });
        default:
            return state;
    }
}
