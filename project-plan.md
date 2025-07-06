# README Generator Project Plan

## Overview
- Goal: Interactive README generator using Python, Rich, and Inquirer.py
- Core features:
  - Template-based README creation with merge tags
  - Interactive prompts for input
  - Preview and regeneration support

## Features

### Input Handling
- Prompt user for built-in options
- Support custom templates with merge tags
- Error handling:
  - Missing merge tags
  - Unclosed code blocks

### Template Management
- `--template` command to generate new templates
- `--settings` command to configure rules:
  - Header merge tag requirements (#, ##, etc.)
  - Code block merge tag requirements (languages)
  - Emoji mappings per section
  - Visual formatting options (horizontal lines)

### Regeneration & History
- Save input JSON with timestamps (e.g., `generation-args-YYYY-MM-DD-HH-MM.json`)
- `--regenerate` command:
  - List saved inputs (highlight last)
  - Option `--last` to regenerate most recent
- Allow editing saved inputs before regeneration (optional)

### Preview
- Convert Markdown to HTML
- Open in system default browser for preview
- Use markdown library (https://www.linode.com/docs/guides/how-to-use-python-markdown-to-convert-markdown-to-html/)
- Extensions fenced_code and codehilite
- Pygments to generate css

## Future Ideas
- Advanced template generation wizard
- Custom merge tag patterns
- Config file support for defaults
- Extend emoji and formatting options
- Live preview for merge tag replacements in current section using Rich layout splitting

## Development Notes
- Use Rich for CLI interface and colors
- Use Inquirer.py for prompts
- Use argparse for argument routing
- Modularize code: input handling, template parsing, file IO

## Program structure

### main.py
- Handles input to filter to other modules
- Loads settings and keeps variable to be used by template & readme generators
- Handles preview generation with --preview flag

### settings.py
- Class Settings to store data
- Handles input/output for settings when called by main.py at .cli()

### template-generator.py
- class TemplateGenerator
- Handles input/output for generating a template when called by main.py at .cli()
- Keeps a reference to a settings object

### readme-generator.py
- class ReadmeGenerator
- Handles input/output for generating a readme when called by main.py
- Takes a template path on .cli(template_path)
- Validates a template is in the correct format
- Handles regeneration from saved inputs
- Holds a dictionary of sections and prompt instructions. Detects sections in templates by # tags and then looks for merge tags to replace.