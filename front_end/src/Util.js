export const getCellId = (key, index) => {
  return "id_" + key + "_" + index;
};

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
  "mar",
];

export const monthsToTitleCase = months.map(
  (x) => x[0].toUpperCase() + x.slice(1),
);

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var currencyFormat = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "GBP",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export const formatMoney = (value) => {
  return currencyFormat.format(value / 100);
};

const numberFormat = new Intl.NumberFormat("en-GB");

export const formatValue = (value) => {
  let pounds = Math.round(value);
  return numberFormat.format(pounds);
};

/**
 * Make a HTTP request to fetch JSON data.
 *
 * @param {string} url The HTTP request URL for the API.
 * @returns JSON response data.
 */
export async function getData(url) {
  const request = new Request(url, {
    method: "GET",
  });

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
 * @param {?string} content_type - Content-Type header for the body.
 * @returns {PostDataResponse}
 */
export async function postData(url, data = {}, headers = {}) {
  if (!url) {
    throw new Error("URL is required");
  }
  const csrftoken = window.CSRF_TOKEN;
  try {
    // Default options are marked with *
    const response = await fetch(url, {
      method: "POST", // *GET, POST, PUT, DELETE, etc.
      mode: "same-origin", // no-cors, *cors, same-origin
      cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers: {
        "X-CSRFToken": csrftoken,
        ...headers,
      },
      redirect: "follow", // manual, *follow, error
      referrer: "no-referrer", // no-referrer, *client
      body: data, // body data type must match "Content-Type" header
    });

    // Status codes that typically don't have response bodies
    const noContentCodes = [204, 205, 304];

    // Check if the response status indicates no content
    if (noContentCodes.includes(response.status)) {
      return {
        status: response.status,
        data: null, // No content to parse
      };
    }

    // For responses that might have content, try to parse JSON
    try {
      const data = await response.json();
      return {
        status: response.status,
        data,
      };
    } catch (jsonError) {
      // Handle case where response exists but isn't valid JSON
      return {
        status: response.status,
        data: null,
        parseError: true,
      };
    }
  } catch (e) {
    return {
      status: e.status || 500,
      data: {
        error: true,
        message: e.message || "Unknown error occurred",
        name: e.name || "Error",
      },
    };
  }
}

export async function postJsonData(url, data = {}) {
  return postData(url, JSON.stringify(data), {
    "Content-Type": "application/json",
  });
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
  ];

  forecastData.forEach(function (rowData, rowIndex) {
    let row = {};
    let colIndex = 0;

    row._meta = {};
    row._meta.isLocked = rowData.is_locked;

    // eslint-disable-next-line
    for (const financialCodeCol of financialCodeCols) {
      row[financialCodeCol] = {
        rowIndex: rowIndex,
        colIndex: colIndex,
        key: financialCodeCol,
        value: rowData[financialCodeCol],
        isEditable: false,
      };

      colIndex++;
    }

    // eslint-disable-next-line
    for (const [key, monthlyFigure] of Object.entries(
      rowData["monthly_figures"],
    )) {
      row[monthlyFigure.month] = {
        rowIndex: rowIndex,
        colIndex: colIndex,
        key: monthlyFigure.month,
        amount: monthlyFigure.amount,
        startingAmount: monthlyFigure.starting_amount,
      };

      colIndex++;
    }

    rows.push(row);
  });

  return rows;
};

export const makeFinancialCodeKey = (
  costCentre,
  programme,
  nac,
  {
    analysis1 = null,
    analysis2 = null,
    project = null,
    year = null,
    period = null,
    separator = "/",
  } = {},
) => {
  return [
    costCentre,
    programme,
    nac,
    analysis1,
    analysis2,
    project,
    year,
    period,
  ].join(separator);
};

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

export const getURLSegment = (index = 0) =>
  window.location.pathname.split("/").filter(Boolean).reverse()[index];
