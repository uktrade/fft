export const getCellId = (key, index) => {
    return "id_" + key + "_" + index;
}

export const months = [ 
    "apr", 
    "may", 
    "jun",
    "jul", 
    "aug", 
    "sep", 
    "oct", 
    "nov", 
    "dec",
    "jan", 
    "feb", 
    "mar"
];

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export const formatValue = (value) => {
    let nfObject = new Intl.NumberFormat('en-GB'); 
    let pounds = Math.round(value)
    return nfObject.format(pounds); 
}

export async function getData(url) {
    const request = new Request(
        url,
        {
            method: "GET",
        },
    );

    let resp = await fetch(request);

    if (!resp.ok) {
      throw new Error("Something went wrong");
    }

    return await resp.json();
}

/**
 * @typedef {object} PostDataResponse
 * @property {number} status
 * @property {object} data
 */

/**
 * POST data to an API.
 * 
 * @param {string} url - URL to POST data to.
 * @param {object} data - Payload to send.
 * @returns {PostDataResponse}
 */
export async function postData(url = '', data = {}) {
    // NOTE: This doesn't work! We set `CSRF_COOKIE_HTTPONLY = True` so the code which
    // uses this function include the CSRF token as part of the submitted form data by
    // pulling it from DOM.
    var csrftoken = getCookie('csrftoken');

    /*
    const defaults = {
      'method': 'POST',
      'credentials': 'include',
      'headers': new Headers({
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
      })
    */

    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            //'Content-Type': 'application/json',
            //'Content-Type': 'multipart/formdata',
            'X-CSRFToken': csrftoken,
            //'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        },
        redirect: 'follow', // manual, *follow, error
        referrer: 'no-referrer', // no-referrer, *client
        body: data // body data type must match "Content-Type" header
    });

    let jsonData = await response.json()

    return {
        status: response.status,
        data: jsonData // parses JSON response into native JavaScript objects
    }
}

export const processForecastData = (forecastData) => {
    let rows = [];

    let financialCodeCols = [
        "analysis1_code",
        "analysis2_code",
        "cost_centre",
        "natural_account_code",
        "programme",
        "nac_description",
        "programme_description",
        "project_code",
        "budget",
    ]

    forecastData.forEach(function (rowData, rowIndex) {
        let cells = {}
        let colIndex = 0

        // eslint-disable-next-line
        for (const financialCodeCol of financialCodeCols) {
            cells[financialCodeCol] = {
                rowIndex: rowIndex,
                colIndex: colIndex,
                key: financialCodeCol,
                value: rowData[financialCodeCol],
                isEditable: false
            }

            colIndex++
        }

        // eslint-disable-next-line
        for (const [key, monthlyFigure] of Object.entries(rowData["monthly_figures"])) {
            cells[monthlyFigure.month] = {
                rowIndex: rowIndex,
                colIndex: colIndex,
                key: monthlyFigure.month,
                amount: monthlyFigure.amount,
                startingAmount: monthlyFigure.starting_amount,
                isEditable: !monthlyFigure.actual
            }

            colIndex++
        }

        rows.push(cells)
    });

    return rows;
}


/**
 * Retrieves JSON data from an HTML element with the given ID.
 *
 * @param {string} id The ID of the HTML element containing the JSON data.
 * @returns {Promise<Object>} A promise resolving to the parsed JSON data.
 */
export function getScriptJsonData(id) {
    // The promise is here to facilitate a smooth future transition to an API call.
    return new Promise((resolve, reject) => {
        const json = JSON.parse(document.getElementById(id).textContent);
        resolve(json);
    });
}
