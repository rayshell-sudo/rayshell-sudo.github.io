---
layout: default
title: Spreadsheet Filter
---

# Spreadsheet Filter

Use this page to browse and filter data exported from your spreadsheet.

<section id="sheet-filter" aria-label="Spreadsheet item filter">
    <p class="helper-text">
        Data source: <code>/data/items.csv</code>. Replace that file with a new CSV export to refresh the page.
    </p>

    <div class="controls" role="group" aria-label="Filter controls">
        <label for="search-input">Search</label>
        <input id="search-input" type="search" placeholder="Search all columns">

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
    </div>

    <p id="result-count" class="helper-text" aria-live="polite"></p>
    <p id="load-error" class="error-text" aria-live="polite"></p>

    <section class="summary-grid" aria-label="Price summary">
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

    <section aria-label="Most recent price by shop">
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

    <div class="table-wrap">
        <table id="results-table">
            <thead id="results-head"></thead>
            <tbody id="results-body"></tbody>
        </table>
    </div>
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
        grid-template-columns: repeat(6, minmax(140px, 1fr));
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

    @media (max-width: 840px) {
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
        const CSV_PATH = '/data/items.csv';
        const NUMERIC_COLUMNS = new Set([
            'Units',
            'Grams',
            'Price',
            'Price per Unit',
            'Price per 100g'
        ]);
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

        const searchInput = document.getElementById('search-input');
        const dateFromFilter = document.getElementById('date-from-filter');
        const dateToFilter = document.getElementById('date-to-filter');
        const shopFilter = document.getElementById('shop-filter');
        const brandFilter = document.getElementById('brand-filter');
        const itemFilter = document.getElementById('item-filter');
        const resultCount = document.getElementById('result-count');
        const loadError = document.getElementById('load-error');
        const resultsHead = document.getElementById('results-head');
        const resultsBody = document.getElementById('results-body');
        const lowestPricePerUnit = document.getElementById('lowest-price-per-unit');
        const highestPricePerUnit = document.getElementById('highest-price-per-unit');
        const lowestPricePer100g = document.getElementById('lowest-price-per-100g');
        const highestPricePer100g = document.getElementById('highest-price-per-100g');
        const recentByShopHint = document.getElementById('recent-by-shop-hint');
        const recentByShopBody = document.getElementById('recent-by-shop-body');

        const state = {
            headers: [],
            rows: [],
            filteredRows: [],
            sortColumn: '',
            sortDirection: 'asc'
        };

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

        function normalizeValue(value) {
            return String(value || '').trim();
        }

        function parseNumericValue(value) {
            const normalized = normalizeValue(value).replace(/[$,]/g, '');
            if (!normalized) {
                return Number.NaN;
            }
            const parsed = Number.parseFloat(normalized);
            return Number.isFinite(parsed) ? parsed : Number.NaN;
        }

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

        function formatCurrency(value) {
            if (!Number.isFinite(value)) {
                return 'N/A';
            }
            return `$${value.toFixed(2)}`;
        }

        function formatSummaryLine(row, metric) {
            if (!row) {
                return 'No valid values in current filter.';
            }
            const value = parseNumericValue(row[metric]);
            return `${formatCurrency(value)} on ${row.Date || 'Unknown date'} (${row.Shop || 'Unknown shop'} | ${row.Item || 'Unknown item'})`;
        }

        function rowToObject(headers, rowValues) {
            const obj = {};
            headers.forEach((header, index) => {
                obj[header] = normalizeValue(rowValues[index] || '');
            });
            return obj;
        }

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
        }

        function getSortIndicator(header) {
            if (state.sortColumn !== header) {
                return '';
            }
            return state.sortDirection === 'asc' ? '▲' : '▼';
        }

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
                .sort((left, right) => left[0].localeCompare(right[0]))
                .map((entry) => entry[1]);

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

        function applyFilters() {
            const search = searchInput.value.trim().toLowerCase();
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

                if (!search) {
                    return true;
                }

                const joined = state.headers.map((header) => row[header]).join(' ').toLowerCase();
                return joined.includes(search);
            });

            const sortedRows = getSortedRows(state.filteredRows);
            resultCount.textContent = `${state.filteredRows.length} item(s) shown`;
            renderTable(state.headers, sortedRows);
            renderSummary(state.filteredRows);
            renderMostRecentByShop(state.filteredRows);
        }

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

                state.headers = parsedRows[0].map((header) => normalizeValue(header));
                state.rows = parsedRows
                    .slice(1)
                    .map((row) => rowToObject(state.headers, row));

                buildFilterValues(state.rows);
                applyFilters();
                loadError.textContent = '';
            } catch (error) {
                loadError.textContent = error.message;
                resultCount.textContent = '';
                resultsHead.innerHTML = '';
                resultsBody.innerHTML = '';
            }
        }

        [searchInput, shopFilter, brandFilter, itemFilter].forEach((element) => {
            element.addEventListener('input', applyFilters);
            element.addEventListener('change', applyFilters);
        });

        [dateFromFilter, dateToFilter].forEach((element) => {
            element.addEventListener('change', applyFilters);
            element.addEventListener('input', applyFilters);
        });

        loadCsv();
    })();
</script>
