import React, {Fragment, useState, useEffect, useRef, useCallback, useMemo } from 'react';

import Table from '../../Components/Table/index'

import {
    getCellId,
    months
} from '../../Util'

function ForecastTable() {
    const [rowData, setRowData] = useState([]);
    const [cellCount, setCellCount] = useState(0);

    useEffect(() => {
        let cellCounter = -1
        let cellIndex = 0;
        let rows = [];
        window.table_data.forEach(function (rowdata, rowIndex) {
            let cellDatas = []
            let colIndex = 0
            for (let key in rowdata) {
                let editable = false;

                for (let i = 0; i < window.editable_periods.length; i++) {
                    let shortName = window.editable_periods[i]["fields"]["period_short_name"];
                    if (shortName && shortName.toLowerCase() == key) {
                        editable = true;
                        break;
                    }
                }

                let cell = {
                    rect: null,
                    id: getCellId(key, rowIndex),
                    index: cellIndex,
                    colIndex: colIndex,
                    rowIndex: rowIndex,
                    key: key,
                    value: rowdata[key],
                    editable: editable,
                    selected: false,
                    editing: false,
                    programmeCode: rowdata["programme__programme_code"],
                    naturalAccountCode: rowdata["natural_account_code__natural_account_code"]
                }

                if (months.includes(cell.key.toLowerCase())) {
                    cellCounter++
                }

                cellDatas.push(cell)
                cellIndex++
                colIndex++
            }
            rows.push(cellDatas)
        });

        setRowData(rows)
        console.log("cellCounter", cellCounter)
        setCellCount(cellCounter)
    }, [window.table_data]);

    return (
        <Fragment>
            <Table rowData={rowData} cellCount={cellCount} />
        </Fragment>
    );
}

export default ForecastTable;
