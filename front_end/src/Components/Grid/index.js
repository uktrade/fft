




function Grid() {
	    useEffect(() => {
        let cellIndex = 0;
        window.table_data.forEach(function (cellData, rowIndex) {
            for (let key in cellData) {

                let editable = false;

                for (let i = 0; i < window.editable_periods.length; i++) {
                    let shortName = window.editable_periods[i]["fields"]["period_short_name"];
                    if (shortName && shortName.toLowerCase() == key) {
                        editable = true;
                        break;
                    }
                }

                dispatch(
                    ADD_CELL({
                        id: getCellId(key, rowIndex),
                        index: cellIndex,
                        rowIndex: rowIndex,
                        key: key,
                        value: cellData[key],
                        editable: editable,
                        programmeCode: cellData["programme__programme_code"],
                        naturalAccountCode: cellData["natural_account_code__natural_account_code"]
                    })
                );
                cellIndex++;
            }
        });
    }, []);
}