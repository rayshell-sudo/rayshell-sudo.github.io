# rayshell-sudo.github.io

## Setup
This repo brought to you by AI Slop!

### Prerequisites

- **Git** - Version control
- **Ruby** (v2.7 or higher) - Required for Jekyll
- **Bundler** - Ruby dependency manager
- **Node.js** (optional) - For JavaScript utilities
- **Python 3** (optional) - For Python utilities

### Local Development

#### 1. Clone the Repository

```bash
git clone https://github.com/rayshell-sudo/rayshell-sudo.github.io.git
cd rayshell-sudo.github.io
```

#### 2. Install Ruby Dependencies

```bash
bundle install
```

This installs Jekyll and the remote theme dependencies specified in `Gemfile`.

#### 3. Serve Locally

```bash
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000`

### Project Structure

- **_config.yml** - Jekyll configuration and site metadata
- **index.md** - Home page content
- **spreadsheet-filter.md** - Spreadsheet-backed filter page
- **data/items.csv** - CSV dataset used by the filter page
- **docstringgeneration.js** - JavaScript utility for docstring generation
- **docstringgeneration.py** - Python utility for docstring generation

### Spreadsheet Data Workflow (Option 1)

Use this workflow to keep data on the site while editing in a spreadsheet:

1. Update your spreadsheet.
2. Export as CSV.
3. Replace `data/items.csv` with the new export (keep header names stable where possible).
4. Commit and push.

The page at `/spreadsheet-filter.html` will load the latest committed CSV and let users filter by shop, brand, item, and free-text search.

### Building for Production

Jekyll automatically builds the site when you run `bundle exec jekyll serve`. For a production build:

```bash
bundle exec jekyll build
```

The compiled site will be in the `_site/` directory.

### Deployment

This site is automatically deployed to GitHub Pages when you push to the `main` branch. No additional steps are needed beyond committing and pushing your changes.

### Customization

- Modify `_config.yml` to change site title, theme, and plugins
- Edit markdown files in the root directory to update content
- Update utility scripts as needed
