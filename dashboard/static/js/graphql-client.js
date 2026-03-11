/**
 * GraphQL client for making queries to the GraphQL endpoint.
 */

const GRAPHQL_ENDPOINT = "/graphql/";

/**
 * Execute a GraphQL query.
 * @param {string} query - The GraphQL query string
 * @param {Object} variables - Optional variables for the query
 * @returns {Promise<any>} - The query result data
 */
async function executeQuery(query, variables = {}) {
  const response = await fetch(GRAPHQL_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, variables }),
  });

  if (!response.ok) {
    throw new Error(`GraphQL request failed: ${response.status}`);
  }

  const result = await response.json();

  if (result.errors) {
    throw new Error(`GraphQL errors: ${JSON.stringify(result.errors)}`);
  }

  return result.data;
}

/**
 * Fetch all enabled widgets.
 * @returns {Promise<Array>}
 */
export async function fetchWidgets() {
  const query = `
    query {
      widgets {
        id
        title
        widgetType
        apiEndpoint
        gridX
        gridY
        width
        height
        refreshIntervalSeconds
      }
    }
  `;

  const data = await executeQuery(query);
  return data.widgets;
}

/**
 * Fetch all enabled keyboard shortcuts.
 * @returns {Promise<Array>}
 */
export async function fetchShortcuts() {
  const query = `
    query {
      shortcuts {
        id
        key
        description
        actionType
        targetWidget
      }
    }
  `;

  const data = await executeQuery(query);
  return data.shortcuts;
}

/**
 * Fetch market data by type.
 * @param {string} type - One of: goldPrice, silverPrice, oilPrice, treasury10y, dowGoldRatio
 * @returns {Promise<{x: string[], y: number[]}>}
 */
export async function fetchMarketData(type) {
  const query = `
    query {
      ${type} {
        x
        y
      }
    }
  `;

  const data = await executeQuery(query);
  return data[type];
}

/**
 * Fetch RSS entries with optional limit.
 * @param {number} limit - Optional limit on number of entries
 * @returns {Promise<Array>}
 */
export async function fetchRSSEntries(limit = null) {
  const query = `
    query($limit: Int) {
      rssEntries(limit: $limit) {
        id
        title
        link
        summary
        publishedAt
        feedName
      }
    }
  `;

  const data = await executeQuery(query, { limit });
  return data.rssEntries;
}

export { executeQuery };
