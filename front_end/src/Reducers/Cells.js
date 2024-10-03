export const SET_CELLS = 'SET_CELLS';
export const SET_EMPLOYEE_CELLS = 'SET_EMPLOYEE_CELLS';
export const SET_NON_EMPLOYEE_CELLS = 'SET_NON_EMPLOYEE_CELLS';
export const SET_MYHR_EMPLOYEE_CELLS = 'SET_MYHR_EMPLOYEE_CELLS';
export const SET_MYHR_NON_EMPLOYEE_CELLS = 'SET_MYHR_NON_EMPLOYEE_CELLS';

const cellsInitial = {
    cells: [],
    employeeCells: [],
    nonEmployeeCells: [],
    myhrEmployeeCells: [],
    myhrNonEmployeeCells: []
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
        case SET_MYHR_EMPLOYEE_CELLS:
            return Object.assign({}, state, {
                myhrEmployeeCells: action.cells
            });
        case SET_MYHR_NON_EMPLOYEE_CELLS:
            return Object.assign({}, state, {
                myhrNonEmployeeCells: action.cells
            });
        default:
            return state;
    }
}
