---
layout: default
title: Grocery Price Book
---

# Grocery Price Book

Select an item to compare prices over time. 

<section id="sheet-filter" aria-label="Spreadsheet item filter">
    <p class="helper-text">
        Data source: <code>/data/items.csv</code>. Replace that file with a new CSV export to refresh the page.
    </p>

    <div class="controls" role="group" aria-label="Filter controls">
        <label for="date-from-filter">Date From</label>
        <input id="date-from-filter" type="date">

        <label for="date-to-filter">Date To</label>
        <input id="date-to-filter" type="date">

        <label for="shop-filter">Shop</label>
        <select id="shop-filter">
            <option value="">All shops</option>
        </select>

        <label for="brand-filter">Brand</label>
        <select id="brand-filter">
            <option value="">All brands</option>
        </select>

        <label for="item-filter">Item</label>
        <select id="item-filter">
            <option value="">All items</option>
        </select>

        <label for="item-search">Search Items</label>
        <input id="item-search" type="search" placeholder="Filter item list">

        <label for="reset-filters-btn">Reset</label>
        <button id="reset-filters-btn" type="button">Reset Filters</button>
    </div>

    <p id="result-count" class="helper-text" aria-live="polite"></p>
    <p id="load-error" class="error-text" aria-live="polite"></p>

    <!-- Summary metrics - shown only when item is selected -->
    <section class="summary-grid" id="summary-section" aria-label="Price summary" hidden>
        <article class="summary-card">
            <h3>Lowest Price per Unit</h3>
            <p id="lowest-price-per-unit">No data</p>
        </article>
        <article class="summary-card">
            <h3>Highest Price per Unit</h3>
            <p id="highest-price-per-unit">No data</p>
        </article>
        <article class="summary-card">
            <h3>Lowest Price per 100g</h3>
            <p id="lowest-price-per-100g">No data</p>
        </article>
        <article class="summary-card">
            <h3>Highest Price per 100g</h3>
            <p id="highest-price-per-100g">No data</p>
        </article>
    </section>

    <!-- Most recent by shop table - shown only when item is selected -->
    <section aria-label="Most recent price by shop" id="recent-section" hidden>
        <h3>Most Recent Price by Shop</h3>
        <p id="recent-by-shop-hint" class="helper-text"></p>
        <div class="table-wrap">
            <table id="recent-by-shop-table">
                <thead>
                    <tr>
                        <th>Shop</th>
                        <th>Item</th>
                        <th>Date</th>
                        <th>Price per Unit</th>
                        <th>Price per 100g</th>
                    </tr>
                </thead>
                <tbody id="recent-by-shop-body"></tbody>
            </table>
        </div>
    </section>

    <!-- Detailed results table - shown only when item is selected -->
    <div class="table-wrap" id="results-section" hidden>
        <h3>Price History</h3>
        <table id="results-table">
            <thead id="results-head"></thead>
            <tbody id="results-body"></tbody>
        </table>
    </div>

    <!-- Item trend chart - shown only when item is selected -->
    <section id="item-trend-section" aria-label="Item price trend" hidden>
        <h3>Price per 100g by Date (Split by Shop)</h3>
        <p id="item-trend-hint" class="helper-text"></p>
        <div class="chart-wrap">
            <svg id="item-trend-chart" viewBox="0 0 960 360" role="img" aria-label="Item trend line chart"></svg>
        </div>
        <div id="item-trend-legend" class="chart-legend"></div>
    </section>

    <section id="item-unit-trend-section" aria-label="Item unit price trend" hidden>
        <h3>Price per Unit by Date (Split by Shop)</h3>
        <p id="item-unit-trend-hint" class="helper-text"></p>
        <div class="chart-wrap">
            <svg id="item-unit-trend-chart" viewBox="0 0 960 360" role="img" aria-label="Item unit price trend line chart"></svg>
        </div>
        <div id="item-unit-trend-legend" class="chart-legend"></div>
    </section>
</section>

<style>
    #sheet-filter {
        margin-top: 1.5rem;
        padding: 1rem;
        border: 1px solid #d7e2eb;
        border-radius: 10px;
        background: #f8fbfe;
    }

    .helper-text {
        margin: 0.5rem 0;
        color: #4f6479;
    }

    .error-text {
        color: #b21f2d;
        min-height: 1.2rem;
    }

    .controls {
        display: grid;
        grid-template-columns: repeat(4, minmax(140px, 1fr));
        gap: 0.6rem;
        margin: 1rem 0;
    }

    .controls label {
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    .controls input,
    .controls select {
        border: 1px solid #c3cfda;
        border-radius: 6px;
        padding: 0.5rem 0.6rem;
        font-size: 0.95rem;
        min-height: 38px;
    }

    .controls button {
        border: 1px solid #94aac0;
        border-radius: 6px;
        padding: 0.5rem 0.6rem;
        font-size: 0.95rem;
        min-height: 38px;
        font-weight: 600;
        background: #ffffff;
        color: #1f3b57;
        cursor: pointer;
    }

    .controls button:hover {
        background: #f0f6fb;
    }

    .table-wrap {
        overflow-x: auto;
    }

    #results-table {
        width: 100%;
        border-collapse: collapse;
        background: #ffffff;
    }

    #results-table th,
    #results-table td,
    #recent-by-shop-table th,
    #recent-by-shop-table td {
        border-bottom: 1px solid #e5edf4;
        text-align: left;
        padding: 0.55rem;
        white-space: nowrap;
    }

    #results-table th,
    #recent-by-shop-table th {
        background: #edf4fa;
        font-weight: 700;
    }

    #recent-section {
        margin-bottom: 1.25rem;
    }

    .summary-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(180px, 1fr));
        gap: 0.75rem;
        margin: 1rem 0;
    }

    .summary-card {
        background: #ffffff;
        border: 1px solid #d7e2eb;
        border-radius: 8px;
        padding: 0.75rem;
    }

    .summary-card h3 {
        margin: 0;
        font-size: 0.95rem;
    }

    .summary-card p {
        margin: 0.4rem 0 0;
        color: #1f3b57;
    }

    .sort-button {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        width: 100%;
        border: 0;
        background: transparent;
        cursor: pointer;
        font: inherit;
        font-weight: 700;
        color: inherit;
        padding: 0;
        text-align: left;
    }

    .sort-indicator {
        color: #426788;
        font-size: 0.85rem;
    }

    #item-trend-section {
        margin-top: 1rem;
        padding-top: 0.5rem;
    }

    .chart-wrap {
        margin-top: 0.5rem;
        background: #ffffff;
        border: 1px solid #d7e2eb;
        border-radius: 8px;
        padding: 0.5rem;
    }

    #item-trend-chart,
    #item-unit-trend-chart {
        width: 100%;
        height: auto;
        display: block;
    }

    .chart-legend {
        margin-top: 0.5rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem 0.9rem;
    }

    .chart-legend-item {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        font-size: 0.9rem;
        color: #1f3b57;
    }

    .chart-legend-swatch {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
    }

    @media (max-width: 1000px) {
        .controls {
            grid-template-columns: repeat(3, minmax(150px, 1fr));
        }

        .summary-grid {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 520px) {
        .controls {
            grid-template-columns: 1fr;
        }
    }
</style>

<script>
    (() => {
        // ============================================================================
        // SPREADSHEET FILTER - Data loader and dynamic UI with search/sort/filter
        // ============================================================================
        // This script initializes a CSV data table with client-side filtering,
        // sorting, and analytics. All data is loaded into memory for fast searching.
        // ============================================================================

        // Configuration
        const CSV_PATH = '/data/items.csv';
        const ALLOWED_COLUMNS = [
            'Date',
            'Shop',
            'Brand',
            'Item',
            'Units',
            'Grams',
            'Price',
            'Price per Unit',
            'Price per 100g'
        ];
        // Columns that contain numeric values (used for sorting and min/max calculations)
        const NUMERIC_COLUMNS = new Set([
            'Units',
            'Grams',
            'Price',
            'Price per Unit',
            'Price per 100g'
        ]);
        // Month name to numeric index mapping for date parsing
        const MONTHS = {
            jan: 0,
            feb: 1,
            mar: 2,
            apr: 3,
            may: 4,
            jun: 5,
            jul: 6,
            aug: 7,
            sep: 8,
            oct: 9,
            nov: 10,
            dec: 11
        };

        // ============================================================================
        // DOM Element References
        // ============================================================================
        // Filter/search controls
        const dateFromFilter = document.getElementById('date-from-filter');
        const dateToFilter = document.getElementById('date-to-filter');
        const shopFilter = document.getElementById('shop-filter');
        const brandFilter = document.getElementById('brand-filter');
        const itemFilter = document.getElementById('item-filter');
        const itemSearch = document.getElementById('item-search');
        const resetFiltersButton = document.getElementById('reset-filters-btn');
        
        // Result display and feedback
        const resultCount = document.getElementById('result-count');
        const loadError = document.getElementById('load-error');
        
        // Results table
        const resultsHead = document.getElementById('results-head');
        const resultsBody = document.getElementById('results-body');
        const resultsSection = document.getElementById('results-section');
        
        // Summary cards (min/max prices)
        const lowestPricePerUnit = document.getElementById('lowest-price-per-unit');
        const highestPricePerUnit = document.getElementById('highest-price-per-unit');
        const lowestPricePer100g = document.getElementById('lowest-price-per-100g');
        const highestPricePer100g = document.getElementById('highest-price-per-100g');
        const summarySection = document.getElementById('summary-section');
        
        // Most recent by shop table
        const recentByShopHint = document.getElementById('recent-by-shop-hint');
        const recentByShopBody = document.getElementById('recent-by-shop-body');
        const recentSection = document.getElementById('recent-section');
        
        // Trend chart (shown only when item selected)
        const itemTrendSection = document.getElementById('item-trend-section');
        const itemTrendHint = document.getElementById('item-trend-hint');
        const itemTrendChart = document.getElementById('item-trend-chart');
        const itemTrendLegend = document.getElementById('item-trend-legend');
        const itemUnitTrendSection = document.getElementById('item-unit-trend-section');
        const itemUnitTrendHint = document.getElementById('item-unit-trend-hint');
        const itemUnitTrendChart = document.getElementById('item-unit-trend-chart');
        const itemUnitTrendLegend = document.getElementById('item-unit-trend-legend');

        // SVG and charting configuration
        const SVG_NS = 'http://www.w3.org/2000/svg';
        // Color palette for chart lines (one per shop, cycles if more than 10 shops)
        const CHART_COLORS = [
            '#1f77b4',
            '#d62728',
            '#2ca02c',
            '#ff7f0e',
            '#9467bd',
            '#17becf',
            '#8c564b',
            '#e377c2',
            '#bcbd22',
            '#7f7f7f'
        ];

        // ============================================================================
        // Application State
        // ============================================================================
        // Maintains all data and current filter/sort state
        const state = {
            headers: [],              // CSV column headers
            rows: [],                 // All CSV data rows (unchanged)
            filteredRows: [],          // Rows after applying current filters
            sortColumn: 'Date',        // Current sort column
            sortDirection: 'desc',     // Current sort direction (asc or desc)
            itemFilterOptions: []      // All unique items (for item search filtering)
        };

        const DEFAULT_SORT_COLUMN = 'Date';
        const DEFAULT_SORT_DIRECTION = 'desc';

        // ============================================================================
        // URL Parameter Persistence
        // ============================================================================
        // Allows filtering state to be persisted and shared via URL parameters
        
        function readUrlState() {
            const params = new URLSearchParams(window.location.search);
            return {
                dateFrom: params.get('from') || '',
                dateTo: params.get('to') || '',
                shop: params.get('shop') || '',
                brand: params.get('brand') || '',
                item: params.get('item') || '',
                sort: params.get('sort') || '',
                dir: params.get('dir') || ''
            };
        }

        function setSelectValueIfExists(selectElement, value) {
            if (!value) {
                selectElement.value = '';
                return;
            }

            const optionExists = [...selectElement.options].some((option) => option.value === value);
            selectElement.value = optionExists ? value : '';
        }

        function hydrateStateFromUrl() {
            const urlState = readUrlState();

            dateFromFilter.value = urlState.dateFrom;
            dateToFilter.value = urlState.dateTo;
            setSelectValueIfExists(shopFilter, urlState.shop);
            setSelectValueIfExists(brandFilter, urlState.brand);
            setSelectValueIfExists(itemFilter, urlState.item);

            if (urlState.sort && state.headers.includes(urlState.sort)) {
                state.sortColumn = urlState.sort;
            }
            if (urlState.dir === 'asc' || urlState.dir === 'desc') {
                state.sortDirection = urlState.dir;
            }
        }

        function updateUrlFromState() {
            const params = new URLSearchParams();

            if (dateFromFilter.value) {
                params.set('from', dateFromFilter.value);
            }
            if (dateToFilter.value) {
                params.set('to', dateToFilter.value);
            }
            if (shopFilter.value) {
                params.set('shop', shopFilter.value);
            }
            if (brandFilter.value) {
                params.set('brand', brandFilter.value);
            }
            if (itemFilter.value) {
                params.set('item', itemFilter.value);
            }

            if (state.sortColumn && state.sortColumn !== DEFAULT_SORT_COLUMN) {
                params.set('sort', state.sortColumn);
            }
            if (state.sortDirection && state.sortDirection !== DEFAULT_SORT_DIRECTION) {
                params.set('dir', state.sortDirection);
            }

            const queryString = params.toString();
            const newUrl = queryString ? `${window.location.pathname}?${queryString}` : window.location.pathname;
            window.history.replaceState(null, '', newUrl);
        }

        // ============================================================================
        // CSV Parsing and Data Transformation
        // ============================================================================
        // Handles CSV parsing with proper quote-escaping and line-ending support
        
        function parseCsv(text) {
            const rows = [];
            let current = '';
            let row = [];
            let inQuotes = false;

            for (let i = 0; i < text.length; i += 1) {
                const char = text[i];
                const next = text[i + 1];

                if (char === '"') {
                    if (inQuotes && next === '"') {
                        current += '"';
                        i += 1;
                    } else {
                        inQuotes = !inQuotes;
                    }
                } else if (char === ',' && !inQuotes) {
                    row.push(current);
                    current = '';
                } else if ((char === '\n' || char === '\r') && !inQuotes) {
                    if (char === '\r' && next === '\n') {
                        i += 1;
                    }
                    row.push(current);
                    current = '';
                    if (row.some((value) => value !== '')) {
                        rows.push(row);
                    }
                    row = [];
                } else {
                    current += char;
                }
            }

            if (current.length > 0 || row.length > 0) {
                row.push(current);
                if (row.some((value) => value !== '')) {
                    rows.push(row);
                }
            }

            return rows;
        }

        // Normalize string values by trimming whitespace
        function normalizeValue(value) {
            return String(value || '').trim();
        }

        // Parse numeric values, stripping currency symbols and commas
        function parseNumericValue(value) {
            const normalized = normalizeValue(value).replace(/[$,]/g, '');
            if (!normalized) {
                return Number.NaN;
            }
            const parsed = Number.parseFloat(normalized);
            return Number.isFinite(parsed) ? parsed : Number.NaN;
        }

        // Parse date strings in format "DD-MMM-YY" to UTC millisecond timestamp
        // Falls back to Date.parse() for other formats
        function parseDateToTimestamp(value) {
            const normalized = normalizeValue(value);
            if (!normalized) {
                return Number.NaN;
            }

            const match = normalized.match(/^(\d{1,2})-([A-Za-z]{3})-(\d{2,4})$/);
            if (match) {
                const day = Number.parseInt(match[1], 10);
                const monthIndex = MONTHS[match[2].toLowerCase()];
                let year = Number.parseInt(match[3], 10);
                if (year < 100) {
                    year += 2000;
                }
                if (Number.isInteger(monthIndex)) {
                    return Date.UTC(year, monthIndex, day);
                }
            }

            const fallback = Date.parse(normalized);
            return Number.isFinite(fallback) ? fallback : Number.NaN;
        }

        // Parse HTML date input format (YYYY-MM-DD)
        function parseInputDate(value) {
            if (!value) {
                return Number.NaN;
            }
            const parts = value.split('-').map((part) => Number.parseInt(part, 10));
            if (parts.length !== 3 || parts.some((part) => !Number.isFinite(part))) {
                return Number.NaN;
            }
            const [year, month, day] = parts;
            return Date.UTC(year, month - 1, day);
        }

        // Format numeric value as currency
        function formatCurrency(value) {
            if (!Number.isFinite(value)) {
                return 'N/A';
            }
            return `$${value.toFixed(2)}`;
        }

        function roundDownToNearestHalf(value) {
            return Math.floor(value * 2) / 2;
        }

        function roundUpToNearestHalf(value) {
            return Math.ceil(value * 2) / 2;
        }

        // Format timestamp as ISO date string (YYYY-MM-DD)
        function formatIsoDate(timestamp) {
            if (!Number.isFinite(timestamp)) {
                return '';
            }
            return new Date(timestamp).toISOString().slice(0, 10);
        }

        // Format a summary line showing price, date, shop, and item
        function formatSummaryLine(row, metric) {
            if (!row) {
                return 'No valid values in current filter.';
            }
            const value = parseNumericValue(row[metric]);
            return `${formatCurrency(value)} on ${row.Date || 'Unknown date'} (${row.Shop || 'Unknown shop'} | ${row.Item || 'Unknown item'})`;
        }

        // Convert CSV row array to object keyed by header
        function rowToObject(headers, rowValues, headerIndexMap) {
            const obj = {};
            headers.forEach((header, index) => {
                const sourceIndex = typeof headerIndexMap[header] === 'number' ? headerIndexMap[header] : index;
                obj[header] = normalizeValue(rowValues[sourceIndex] || '');
            });
            return obj;
        }

        // Populate a select element with sorted options
        function setSelectOptions(selectElement, values, allLabel) {
            const sorted = [...values].sort((a, b) => a.localeCompare(b));
            selectElement.innerHTML = '';

            const allOption = document.createElement('option');
            allOption.value = '';
            allOption.textContent = allLabel;
            selectElement.appendChild(allOption);

            sorted.forEach((value) => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value;
                selectElement.appendChild(option);
            });
        }

        // ============================================================================
        // Filter Dropdown Initialization
        // ============================================================================
        // Extract and populate Shop, Brand, and Item dropdowns
        
        function buildFilterValues(rows) {
            const shops = new Set();
            const brands = new Set();
            const items = new Set();

            rows.forEach((row) => {
                if (row.Shop) {
                    shops.add(row.Shop);
                }
                if (row.Brand) {
                    brands.add(row.Brand);
                }
                if (row.Item) {
                    items.add(row.Item);
                }
            });

            setSelectOptions(shopFilter, shops, 'All shops');
            setSelectOptions(brandFilter, brands, 'All brands');
            setSelectOptions(itemFilter, items, 'All items');
            // Store items for item search filtering
            state.itemFilterOptions = [...items].sort((a, b) => a.localeCompare(b));
        }

        // ============================================================================
        // Sorting and Table Rendering
        // ============================================================================
        
        function getSortIndicator(header) {
            if (state.sortColumn !== header) {
                return '';
            }
            return state.sortDirection === 'asc' ? '▲' : '▼';
        }

        // Compare two rows by a column, handling dates, numerics, and text
        function compareByColumn(left, right, column) {
            if (column === 'Date') {
                const leftValue = parseDateToTimestamp(left.Date);
                const rightValue = parseDateToTimestamp(right.Date);
                if (!Number.isFinite(leftValue) && !Number.isFinite(rightValue)) {
                    return 0;
                }
                if (!Number.isFinite(leftValue)) {
                    return 1;
                }
                if (!Number.isFinite(rightValue)) {
                    return -1;
                }
                return leftValue - rightValue;
            }

            if (NUMERIC_COLUMNS.has(column)) {
                const leftValue = parseNumericValue(left[column]);
                const rightValue = parseNumericValue(right[column]);
                if (!Number.isFinite(leftValue) && !Number.isFinite(rightValue)) {
                    return 0;
                }
                if (!Number.isFinite(leftValue)) {
                    return 1;
                }
                if (!Number.isFinite(rightValue)) {
                    return -1;
                }
                return leftValue - rightValue;
            }

            const leftValue = normalizeValue(left[column]).toLowerCase();
            const rightValue = normalizeValue(right[column]).toLowerCase();
            return leftValue.localeCompare(rightValue);
        }

        function getSortedRows(rows) {
            if (!state.sortColumn) {
                return rows;
            }

            const direction = state.sortDirection === 'asc' ? 1 : -1;
            return [...rows].sort((left, right) => compareByColumn(left, right, state.sortColumn) * direction);
        }

        // Render the detailed results table with sortable headers
        function renderTable(headers, rows) {
            resultsHead.innerHTML = '';
            resultsBody.innerHTML = '';

            const tr = document.createElement('tr');
            headers.forEach((header) => {
                const th = document.createElement('th');

                const button = document.createElement('button');
                button.type = 'button';
                button.className = 'sort-button';
                button.setAttribute('aria-label', `Sort by ${header}`);
                button.addEventListener('click', () => {
                    if (state.sortColumn === header) {
                        state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc';
                    } else {
                        state.sortColumn = header;
                        state.sortDirection = 'asc';
                    }
                    applyFilters();
                });

                const text = document.createElement('span');
                text.textContent = header;
                const indicator = document.createElement('span');
                indicator.className = 'sort-indicator';
                indicator.textContent = getSortIndicator(header);
                button.appendChild(text);
                button.appendChild(indicator);
                th.appendChild(button);
                tr.appendChild(th);
            });
            resultsHead.appendChild(tr);

            rows.forEach((row) => {
                const rowEl = document.createElement('tr');
                headers.forEach((header) => {
                    const cell = document.createElement('td');
                    cell.textContent = row[header] || '';
                    rowEl.appendChild(cell);
                });
                resultsBody.appendChild(rowEl);
            });
        }

        // ============================================================================
        // Analytics and Summary Rendering
        // ============================================================================
        // Find min/max prices and render summary cards and tables
        
        function findExtremeRow(rows, metric, mode) {
            const validRows = rows.filter((row) => Number.isFinite(parseNumericValue(row[metric])));
            if (validRows.length === 0) {
                return null;
            }

            return validRows.reduce((best, current) => {
                if (!best) {
                    return current;
                }

                const bestValue = parseNumericValue(best[metric]);
                const currentValue = parseNumericValue(current[metric]);
                if (mode === 'min') {
                    return currentValue < bestValue ? current : best;
                }
                return currentValue > bestValue ? current : best;
            }, null);
        }

        // Render summary cards showing min/max prices with context
        function renderSummary(rows) {
            const lowestUnit = findExtremeRow(rows, 'Price per Unit', 'min');
            const highestUnit = findExtremeRow(rows, 'Price per Unit', 'max');
            const lowest100g = findExtremeRow(rows, 'Price per 100g', 'min');
            const highest100g = findExtremeRow(rows, 'Price per 100g', 'max');

            lowestPricePerUnit.textContent = formatSummaryLine(lowestUnit, 'Price per Unit');
            highestPricePerUnit.textContent = formatSummaryLine(highestUnit, 'Price per Unit');
            lowestPricePer100g.textContent = formatSummaryLine(lowest100g, 'Price per 100g');
            highestPricePer100g.textContent = formatSummaryLine(highest100g, 'Price per 100g');
        }

        // Render table of most recent price entries grouped by shop
        function renderMostRecentByShop(rows) {
            recentByShopBody.innerHTML = '';

            const byShop = new Map();
            rows.forEach((row) => {
                const shop = normalizeValue(row.Shop) || 'Unknown shop';
                const rowDate = parseDateToTimestamp(row.Date);
                const existing = byShop.get(shop);
                const existingDate = existing ? parseDateToTimestamp(existing.Date) : Number.NaN;

                if (!existing || (!Number.isFinite(existingDate) && Number.isFinite(rowDate)) || rowDate > existingDate) {
                    byShop.set(shop, row);
                }
            });

            const latestRows = [...byShop.entries()]
                .map((entry) => entry[1])
                .sort((left, right) => {
                    const leftDate = parseDateToTimestamp(left.Date);
                    const rightDate = parseDateToTimestamp(right.Date);

                    if (!Number.isFinite(leftDate) && !Number.isFinite(rightDate)) {
                        return (left.Shop || '').localeCompare(right.Shop || '');
                    }
                    if (!Number.isFinite(leftDate)) {
                        return 1;
                    }
                    if (!Number.isFinite(rightDate)) {
                        return -1;
                    }

                    if (rightDate !== leftDate) {
                        return rightDate - leftDate;
                    }

                    return (left.Shop || '').localeCompare(right.Shop || '');
                });

            if (latestRows.length === 0) {
                recentByShopHint.textContent = 'No rows available for the current filters.';
                return;
            }

            recentByShopHint.textContent = `${latestRows.length} shop(s) with latest matching price entries.`;

            latestRows.forEach((row) => {
                const tr = document.createElement('tr');
                const values = [
                    row.Shop || 'Unknown shop',
                    row.Item || 'Unknown item',
                    row.Date || '',
                    row['Price per Unit'] || '',
                    row['Price per 100g'] || ''
                ];

                values.forEach((value) => {
                    const td = document.createElement('td');
                    td.textContent = value;
                    tr.appendChild(td);
                });

                recentByShopBody.appendChild(tr);
            });
        }

        // ============================================================================
        // Trend Chart Rendering
        // ============================================================================
        // SVG-based line chart showing price trends by shop over time
        
        function clearChart(chartElement, legendElement) {
            chartElement.innerHTML = '';
            legendElement.innerHTML = '';
        }

        // Create an SVG element with namespace and attributes
        function createSvgElement(tag, attributes) {
            const element = document.createElementNS(SVG_NS, tag);
            Object.entries(attributes).forEach(([key, value]) => {
                element.setAttribute(key, String(value));
            });
            return element;
        }

        // Render chart legend showing shop names with color swatches
        function renderLegend(groups, legendElement) {
            legendElement.innerHTML = '';
            groups.forEach((group, index) => {
                const color = CHART_COLORS[index % CHART_COLORS.length];
                const legendItem = document.createElement('span');
                legendItem.className = 'chart-legend-item';

                const swatch = document.createElement('span');
                swatch.className = 'chart-legend-swatch';
                swatch.style.backgroundColor = color;

                const label = document.createElement('span');
                label.textContent = group.shop;

                legendItem.appendChild(swatch);
                legendItem.appendChild(label);
                legendElement.appendChild(legendItem);
            });
        }

        // Render SVG trend chart: Price per 100g over time, split by shop
        // Only renders if an item is selected
        function renderItemTrendChart(rows, selectedItem) {
            if (!selectedItem) {
                itemTrendSection.hidden = true;
                clearChart(itemTrendChart, itemTrendLegend);
                return;
            }

            itemTrendSection.hidden = false;
            clearChart(itemTrendChart, itemTrendLegend);

            const grouped = new Map();
            rows.forEach((row) => {
                if (row.Item !== selectedItem) {
                    return;
                }

                const timestamp = parseDateToTimestamp(row.Date);
                const pricePer100g = parseNumericValue(row['Price per 100g']);
                if (!Number.isFinite(timestamp) || !Number.isFinite(pricePer100g)) {
                    return;
                }

                const shop = normalizeValue(row.Shop) || 'Unknown shop';
                if (!grouped.has(shop)) {
                    grouped.set(shop, []);
                }
                grouped.get(shop).push({
                    timestamp,
                    pricePer100g,
                    dateText: row.Date || '',
                    shop
                });
            });

            const groups = [...grouped.entries()]
                .map(([shop, points]) => ({
                    shop,
                    points: points.sort((a, b) => a.timestamp - b.timestamp)
                }))
                .filter((group) => group.points.length > 0)
                .sort((a, b) => a.shop.localeCompare(b.shop));

            if (groups.length === 0) {
                itemTrendHint.textContent = 'No valid Date and Price per 100g values for the selected item in current filters.';
                return;
            }

            const allPoints = groups.flatMap((group) => group.points);
            const minDate = Math.min(...allPoints.map((point) => point.timestamp));
            const maxDate = Math.max(...allPoints.map((point) => point.timestamp));
            const minPriceRaw = Math.min(...allPoints.map((point) => point.pricePer100g));
            const maxPriceRaw = Math.max(...allPoints.map((point) => point.pricePer100g));

            let minPrice = roundDownToNearestHalf(minPriceRaw);
            let maxPrice = roundUpToNearestHalf(maxPriceRaw);
            if (minPrice === maxPrice) {
                minPrice -= 0.5;
                maxPrice += 0.5;
            }
            const safeMaxDate = minDate === maxDate ? minDate + 86400000 : maxDate;

            const width = 960;
            const height = 360;
            const margins = {
                top: 20,
                right: 20,
                bottom: 45,
                left: 56
            };
            const plotWidth = width - margins.left - margins.right;
            const plotHeight = height - margins.top - margins.bottom;

            const scaleX = (value) => margins.left + ((value - minDate) / (safeMaxDate - minDate)) * plotWidth;
            const scaleY = (value) => margins.top + ((maxPrice - value) / (maxPrice - minPrice)) * plotHeight;

            const background = createSvgElement('rect', {
                x: margins.left,
                y: margins.top,
                width: plotWidth,
                height: plotHeight,
                fill: '#ffffff'
            });
            itemTrendChart.appendChild(background);

            const yTicks = 5;
            for (let i = 0; i <= yTicks; i += 1) {
                const ratio = i / yTicks;
                const value = minPrice + (maxPrice - minPrice) * ratio;
                const y = scaleY(value);

                const grid = createSvgElement('line', {
                    x1: margins.left,
                    y1: y,
                    x2: width - margins.right,
                    y2: y,
                    stroke: '#e5edf4',
                    'stroke-width': 1
                });
                itemTrendChart.appendChild(grid);

                const label = createSvgElement('text', {
                    x: margins.left - 8,
                    y: y + 4,
                    'text-anchor': 'end',
                    'font-size': 11,
                    fill: '#4f6479'
                });
                label.textContent = formatCurrency(value);
                itemTrendChart.appendChild(label);
            }

            const xTicks = Math.min(6, allPoints.length);
            for (let i = 0; i < xTicks; i += 1) {
                const ratio = xTicks === 1 ? 0 : i / (xTicks - 1);
                const tickValue = minDate + (safeMaxDate - minDate) * ratio;
                const x = scaleX(tickValue);

                const grid = createSvgElement('line', {
                    x1: x,
                    y1: margins.top,
                    x2: x,
                    y2: height - margins.bottom,
                    stroke: '#f1f6fa',
                    'stroke-width': 1
                });
                itemTrendChart.appendChild(grid);

                const label = createSvgElement('text', {
                    x,
                    y: height - margins.bottom + 18,
                    'text-anchor': 'middle',
                    'font-size': 11,
                    fill: '#4f6479'
                });
                label.textContent = formatIsoDate(tickValue);
                itemTrendChart.appendChild(label);
            }

            const xAxis = createSvgElement('line', {
                x1: margins.left,
                y1: height - margins.bottom,
                x2: width - margins.right,
                y2: height - margins.bottom,
                stroke: '#8ea5bb',
                'stroke-width': 1.25
            });
            const yAxis = createSvgElement('line', {
                x1: margins.left,
                y1: margins.top,
                x2: margins.left,
                y2: height - margins.bottom,
                stroke: '#8ea5bb',
                'stroke-width': 1.25
            });
            itemTrendChart.appendChild(xAxis);
            itemTrendChart.appendChild(yAxis);

            groups.forEach((group, index) => {
                const color = CHART_COLORS[index % CHART_COLORS.length];
                const pathData = group.points
                    .map((point, pointIndex) => {
                        const x = scaleX(point.timestamp);
                        const y = scaleY(point.pricePer100g);
                        return `${pointIndex === 0 ? 'M' : 'L'} ${x} ${y}`;
                    })
                    .join(' ');

                const path = createSvgElement('path', {
                    d: pathData,
                    fill: 'none',
                    stroke: color,
                    'stroke-width': 2
                });
                itemTrendChart.appendChild(path);

                group.points.forEach((point) => {
                    const circle = createSvgElement('circle', {
                        cx: scaleX(point.timestamp),
                        cy: scaleY(point.pricePer100g),
                        r: 3,
                        fill: color
                    });
                    const title = createSvgElement('title', {});
                    title.textContent = `${group.shop} | ${point.dateText} | ${formatCurrency(point.pricePer100g)}`;
                    circle.appendChild(title);
                    itemTrendChart.appendChild(circle);
                });
            });

            renderLegend(groups, itemTrendLegend);
            itemTrendHint.textContent = `${allPoints.length} point(s) across ${groups.length} shop(s) for ${selectedItem}.`;
        }

        // Render SVG trend chart: Price per Unit over time, split by shop
        // Only renders if an item is selected
        function renderItemUnitTrendChart(rows, selectedItem) {
            if (!selectedItem) {
                itemUnitTrendSection.hidden = true;
                clearChart(itemUnitTrendChart, itemUnitTrendLegend);
                return;
            }

            itemUnitTrendSection.hidden = false;
            clearChart(itemUnitTrendChart, itemUnitTrendLegend);

            const grouped = new Map();
            rows.forEach((row) => {
                if (row.Item !== selectedItem) {
                    return;
                }

                const timestamp = parseDateToTimestamp(row.Date);
                const pricePerUnit = parseNumericValue(row['Price per Unit']);
                if (!Number.isFinite(timestamp) || !Number.isFinite(pricePerUnit)) {
                    return;
                }

                const shop = normalizeValue(row.Shop) || 'Unknown shop';
                if (!grouped.has(shop)) {
                    grouped.set(shop, []);
                }
                grouped.get(shop).push({
                    timestamp,
                    pricePerUnit,
                    dateText: row.Date || '',
                    shop
                });
            });

            const groups = [...grouped.entries()]
                .map(([shop, points]) => ({
                    shop,
                    points: points.sort((a, b) => a.timestamp - b.timestamp)
                }))
                .filter((group) => group.points.length > 0)
                .sort((a, b) => a.shop.localeCompare(b.shop));

            if (groups.length === 0) {
                itemUnitTrendHint.textContent = 'No valid Date and Price per Unit values for the selected item in current filters.';
                return;
            }

            const allPoints = groups.flatMap((group) => group.points);
            const minDate = Math.min(...allPoints.map((point) => point.timestamp));
            const maxDate = Math.max(...allPoints.map((point) => point.timestamp));
            const minPriceRaw = Math.min(...allPoints.map((point) => point.pricePerUnit));
            const maxPriceRaw = Math.max(...allPoints.map((point) => point.pricePerUnit));

            let minPrice = roundDownToNearestHalf(minPriceRaw);
            let maxPrice = roundUpToNearestHalf(maxPriceRaw);
            if (minPrice === maxPrice) {
                minPrice -= 0.5;
                maxPrice += 0.5;
            }
            const safeMaxDate = minDate === maxDate ? minDate + 86400000 : maxDate;

            const width = 960;
            const height = 360;
            const margins = {
                top: 20,
                right: 20,
                bottom: 45,
                left: 56
            };
            const plotWidth = width - margins.left - margins.right;
            const plotHeight = height - margins.top - margins.bottom;

            const scaleX = (value) => margins.left + ((value - minDate) / (safeMaxDate - minDate)) * plotWidth;
            const scaleY = (value) => margins.top + ((maxPrice - value) / (maxPrice - minPrice)) * plotHeight;

            const background = createSvgElement('rect', {
                x: margins.left,
                y: margins.top,
                width: plotWidth,
                height: plotHeight,
                fill: '#ffffff'
            });
            itemUnitTrendChart.appendChild(background);

            const yTicks = 5;
            for (let i = 0; i <= yTicks; i += 1) {
                const ratio = i / yTicks;
                const value = minPrice + (maxPrice - minPrice) * ratio;
                const y = scaleY(value);

                const grid = createSvgElement('line', {
                    x1: margins.left,
                    y1: y,
                    x2: width - margins.right,
                    y2: y,
                    stroke: '#e5edf4',
                    'stroke-width': 1
                });
                itemUnitTrendChart.appendChild(grid);

                const label = createSvgElement('text', {
                    x: margins.left - 8,
                    y: y + 4,
                    'text-anchor': 'end',
                    'font-size': 11,
                    fill: '#4f6479'
                });
                label.textContent = formatCurrency(value);
                itemUnitTrendChart.appendChild(label);
            }

            const xTicks = Math.min(6, allPoints.length);
            for (let i = 0; i < xTicks; i += 1) {
                const ratio = xTicks === 1 ? 0 : i / (xTicks - 1);
                const tickValue = minDate + (safeMaxDate - minDate) * ratio;
                const x = scaleX(tickValue);

                const grid = createSvgElement('line', {
                    x1: x,
                    y1: margins.top,
                    x2: x,
                    y2: height - margins.bottom,
                    stroke: '#f1f6fa',
                    'stroke-width': 1
                });
                itemUnitTrendChart.appendChild(grid);

                const label = createSvgElement('text', {
                    x,
                    y: height - margins.bottom + 18,
                    'text-anchor': 'middle',
                    'font-size': 11,
                    fill: '#4f6479'
                });
                label.textContent = formatIsoDate(tickValue);
                itemUnitTrendChart.appendChild(label);
            }

            const xAxis = createSvgElement('line', {
                x1: margins.left,
                y1: height - margins.bottom,
                x2: width - margins.right,
                y2: height - margins.bottom,
                stroke: '#8ea5bb',
                'stroke-width': 1.25
            });
            const yAxis = createSvgElement('line', {
                x1: margins.left,
                y1: margins.top,
                x2: margins.left,
                y2: height - margins.bottom,
                stroke: '#8ea5bb',
                'stroke-width': 1.25
            });
            itemUnitTrendChart.appendChild(xAxis);
            itemUnitTrendChart.appendChild(yAxis);

            groups.forEach((group, index) => {
                const color = CHART_COLORS[index % CHART_COLORS.length];
                const pathData = group.points
                    .map((point, pointIndex) => {
                        const x = scaleX(point.timestamp);
                        const y = scaleY(point.pricePerUnit);
                        return `${pointIndex === 0 ? 'M' : 'L'} ${x} ${y}`;
                    })
                    .join(' ');

                const path = createSvgElement('path', {
                    d: pathData,
                    fill: 'none',
                    stroke: color,
                    'stroke-width': 2
                });
                itemUnitTrendChart.appendChild(path);

                group.points.forEach((point) => {
                    const circle = createSvgElement('circle', {
                        cx: scaleX(point.timestamp),
                        cy: scaleY(point.pricePerUnit),
                        r: 3,
                        fill: color
                    });
                    const title = createSvgElement('title', {});
                    title.textContent = `${group.shop} | ${point.dateText} | ${formatCurrency(point.pricePerUnit)}`;
                    circle.appendChild(title);
                    itemUnitTrendChart.appendChild(circle);
                });
            });

            renderLegend(groups, itemUnitTrendLegend);
            itemUnitTrendHint.textContent = `${allPoints.length} point(s) across ${groups.length} shop(s) for ${selectedItem}.`;
        }

        // ============================================================================
        // Filtering and Rendering Pipeline
        // ============================================================================
        // Main function: applies all active filters and updates UI
        
        function applyFilters() {
            const dateFrom = parseInputDate(dateFromFilter.value);
            const dateTo = parseInputDate(dateToFilter.value);
            const shop = shopFilter.value;
            const brand = brandFilter.value;
            const item = itemFilter.value;

            state.filteredRows = state.rows.filter((row) => {
                const rowDate = parseDateToTimestamp(row.Date);
                const hasDateRange = Number.isFinite(dateFrom) || Number.isFinite(dateTo);

                if (hasDateRange && !Number.isFinite(rowDate)) {
                    return false;
                }

                if (Number.isFinite(dateFrom) && Number.isFinite(rowDate) && rowDate < dateFrom) {
                    return false;
                }
                if (Number.isFinite(dateTo) && Number.isFinite(rowDate) && rowDate > dateTo) {
                    return false;
                }

                if (shop && row.Shop !== shop) {
                    return false;
                }
                if (brand && row.Brand !== brand) {
                    return false;
                }
                if (item && row.Item !== item) {
                    return false;
                }

                return true;
            });

            const sortedRows = getSortedRows(state.filteredRows);
            resultCount.textContent = `${state.filteredRows.length} item(s) shown`;
            renderTable(state.headers, sortedRows);
            
            // Show/hide analytics sections based on whether an item is selected
            if (item) {
                summarySection.hidden = false;
                recentSection.hidden = false;
                resultsSection.hidden = false;
            } else {
                summarySection.hidden = true;
                recentSection.hidden = true;
                resultsSection.hidden = true;
            }
            
            renderSummary(state.filteredRows);
            renderMostRecentByShop(state.filteredRows);
            renderItemTrendChart(state.filteredRows, item);
            renderItemUnitTrendChart(state.filteredRows, item);
            updateUrlFromState();
        }

        // Reset all filters and sort to defaults
        function resetFilters() {
            dateFromFilter.value = '';
            dateToFilter.value = '';
            shopFilter.value = '';
            brandFilter.value = '';
            itemFilter.value = '';

            state.sortColumn = DEFAULT_SORT_COLUMN;
            state.sortDirection = DEFAULT_SORT_DIRECTION;

            applyFilters();
        }

        // ============================================================================
        // CSV Loading and Initialization
        // ============================================================================
        
        async function loadCsv() {
            try {
                const response = await fetch(CSV_PATH, { cache: 'no-store' });
                if (!response.ok) {
                    throw new Error(`Failed to load ${CSV_PATH} (${response.status})`);
                }

                const csvText = await response.text();
                const parsedRows = parseCsv(csvText);

                if (parsedRows.length < 2) {
                    throw new Error('CSV needs a header row and at least one data row.');
                }

                const csvHeaders = parsedRows[0].map((header) => normalizeValue(header));
                const missingColumns = ALLOWED_COLUMNS.filter((column) => !csvHeaders.includes(column));
                if (missingColumns.length > 0) {
                    throw new Error(`CSV is missing required column(s): ${missingColumns.join(', ')}`);
                }
                const headerIndexMap = {};
                csvHeaders.forEach((header, index) => {
                    headerIndexMap[header] = index;
                });

                // Only use the approved columns for filter/search/sort/display.
                state.headers = ALLOWED_COLUMNS;
                state.rows = parsedRows
                    .slice(1)
                    .map((row) => rowToObject(state.headers, row, headerIndexMap));

                buildFilterValues(state.rows);
                hydrateStateFromUrl();
                applyFilters();
                loadError.textContent = '';
            } catch (error) {
                loadError.textContent = error.message;
                resultCount.textContent = '';
                resultsHead.innerHTML = '';
                resultsBody.innerHTML = '';
            }
        }

        // ============================================================================
        // Item Search Filter Handler
        // ============================================================================
        // Dynamically filter the item dropdown based on search input
        
        function filterItemDropdown() {
            const searchTerm = itemSearch.value.trim().toLowerCase();
            const items = new Set();
            
            // Filter items based on search term
            state.itemFilterOptions.forEach((item) => {
                if (item.toLowerCase().includes(searchTerm)) {
                    items.add(item);
                }
            });
            
            // Update item dropdown with filtered options
            setSelectOptions(itemFilter, items, 'All items');
        }
        
        itemSearch.addEventListener('input', filterItemDropdown);
        
        // ============================================================================
        // Event Handlers for Filter Controls
        // ============================================================================
        
        [shopFilter, brandFilter, itemFilter].forEach((element) => {
            element.addEventListener('input', applyFilters);
            element.addEventListener('change', applyFilters);
        });

        [dateFromFilter, dateToFilter].forEach((element) => {
            element.addEventListener('change', applyFilters);
            element.addEventListener('input', applyFilters);
        });

        resetFiltersButton.addEventListener('click', () => {
            itemSearch.value = ''; // Also reset the item search
            filterItemDropdown();
            resetFilters();
        });

        // ============================================================================
        // Application Initialization
        // ============================================================================
        
        loadCsv();
    })();
</script>
