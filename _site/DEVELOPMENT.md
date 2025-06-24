# Local Jekyll Development Setup

This guide explains how to set up and run your Jekyll blog locally for faster development and testing.

## Prerequisites

- Ruby 3.0+ (already installed on your system)
- Jekyll 4.4.1+ (installed via gem)
- Bundler (for dependency management)

## Quick Start

### 1. Install Dependencies
```bash
bundle install --path vendor/bundle
```

### 2. Start Development Server
```bash
./dev-server.sh start
```

### 3. Access Your Blog
Open your browser and go to: **http://localhost:4000/crw-blog/**

### 4. Stop Server (when done)
```bash
./dev-server.sh stop
```

## Development Server Commands

The `dev-server.sh` script provides easy management of your local Jekyll server:

```bash
./dev-server.sh start    # Start the server
./dev-server.sh stop     # Stop the server
./dev-server.sh restart  # Restart the server
./dev-server.sh status   # Check server status
```

## Manual Commands

If you prefer to run commands manually:

### Build the site
```bash
bundle exec jekyll build
```

### Start server with live reload
```bash
bundle exec jekyll serve --livereload
```

### Start server with specific host/port
```bash
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

## File Structure

- `_posts/` - Your blog posts (markdown files)
- `_layouts/` - HTML templates
- `_config.yml` - Jekyll configuration
- `_site/` - Generated static site (don't edit directly)
- `vendor/bundle/` - Ruby gems (managed by Bundler)

## MathJax Configuration

The site is configured to use MathJax for LaTeX rendering. The configuration is in `_layouts/default.html`.

## Troubleshooting

### Server won't start
- Check if port 4000 is already in use: `lsof -i :4000`
- Kill existing Jekyll processes: `pkill -f jekyll`

### Math not rendering
- Check browser console for MathJax errors
- Verify LaTeX syntax in your markdown files
- Ensure math blocks are properly delimited with `$$` or `$`

### Build errors
- Check the log file: `jekyll.log`
- Run `bundle exec jekyll build --verbose` for detailed output

## Git Workflow

1. Make changes to your markdown files
2. Test locally with `./dev-server.sh start`
3. Commit changes when satisfied
4. Push to GitHub for deployment

## Performance Tips

- Use `--incremental` flag for faster builds during development
- Use `--livereload` for automatic browser refresh
- The local server is much faster than waiting for GitHub Pages builds 