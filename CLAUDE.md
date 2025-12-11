# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**VCU QA Document Generator** (md2html-converter) - 优雅的 Markdown 转 HTML 报告生成工具，专为 VCU（车辆控制单元）项目质量文档和技术报告设计。

### Core Purpose
- 将 Markdown 技术文档转换为专业的 HTML 报告
- 支持图片自动嵌入（Base64）、Mermaid 图表、多主题
- 提供批量处理和交互式界面
- **新增**: 项目分析与质量报告生成（`analyzers` 模块）

---

## Development Commands

### Running the Tool

```bash
# Single file conversion
python md2html.py report.md

# With theme selection
python md2html.py report.md -t minimal

# Batch conversion
python md2html.py docs/ -r -o output/

# Interactive mode (no arguments)
python md2html.py

# List available themes
python md2html.py --list-themes
```

### Project Analysis Tool

```bash
# Analyze current project
python analyze_project.py

# Analyze specific project
python analyze_project.py /path/to/project

# Specify output file
python analyze_project.py -o my_report

# Generate only Markdown
python analyze_project.py -f markdown

# Generate only HTML
python analyze_project.py -f html

# Verbose output
python analyze_project.py -v
```

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (testing, linting)
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

### Testing (if implemented)

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_converter.py

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black src/

# Check code style
flake8 src/

# Type checking
mypy src/

# Sort imports
isort src/
```

---

## Architecture Overview

### Layered Architecture

```
md2html.py (Entry Point)              analyze_project.py (Analysis Entry)
    ↓                                          ↓
src/cli.py (CLI & Argument Parsing)   src/analyzers/report_generator.py
    ↓                                          ↓
src/interactive.py (Interactive UI)   src/analyzers/metrics_collector.py
    ↓                                          ↓
src/core/converter.py (Conversion)    ┌────────────────────────────────┐
    ↓                                 │  Project Analysis Modules      │
┌─────────────┬──────────────┬───────┼────────────────────────────────┤
│ Processors  │   Themes     │ Utils │ Analyzers (project, quality,   │
│ (image,     │ (default,    │(scan, │  dependency, metrics)          │
│  mermaid)   │  minimal,    │format)│                                │
│             │professional) │       │                                │
└─────────────┴──────────────┴───────┴────────────────────────────────┘
```

### Core Components

#### 1. **Conversion Pipeline** (`src/core/converter.py`)
The `HTMLConverter` class orchestrates the entire conversion process:
- **Input**: Markdown file path
- **Processing**:
  1. Read Markdown content
  2. Process images (embed as Base64 if enabled)
  3. Process Mermaid diagrams
  4. Convert Markdown to HTML using `python-markdown` with extensions
  5. Apply selected theme
  6. Generate complete HTML document
- **Output**: HTML file with embedded resources

**Key method**: `convert(source_path, output_path, theme, embed_images, process_mermaid)`

#### 2. **Theme System** (`src/themes/`)
All themes inherit from `BaseTheme` (abstract base class):
- **BaseTheme**: Defines interface (`get_styles()`, `get_scripts()`, `render()`)
- **DefaultTheme**: Feature-rich theme with sidebar, image zoom, TOC navigation
- **MinimalTheme**: Clean, reading-focused design
- **ProfessionalTheme**: Technical report style

**To add a new theme**:
1. Create new file in `src/themes/your_theme.py`
2. Inherit from `BaseTheme`
3. Implement `get_styles()` and `get_scripts()`
4. Register in `src/themes/__init__.py`

#### 3. **Processors** (`src/processors/`)
- **ImageProcessor**: Converts local images to Base64 data URIs
- **MermaidProcessor**: Wraps Mermaid code blocks with proper HTML structure for client-side rendering

#### 4. **Configuration System** (`src/config_manager.py`)
Manages user preferences stored in `~/.md2html/config.json`:
- Default theme, image embedding, Mermaid processing
- Batch conversion settings (recursive, pattern, max_workers)
- Preset management (save/load/delete custom configurations)

#### 5. **Batch Processing** (`src/batch_processor.py`)
Handles concurrent conversion of multiple files:
- Multi-threaded processing with progress reporting
- Error handling and result tracking
- Configurable worker count

#### 6. **Project Analysis System** (`src/analyzers/`)
Analyzes project structure, code quality, and dependencies:
- **BaseAnalyzer**: Abstract base class for all analyzers
- **ProjectAnalyzer**: Scans file structure, counts code lines, generates directory tree
- **CodeQualityAnalyzer**: Analyzes complexity, style issues, best practices
- **DependencyAnalyzer**: Parses requirements.txt, package.json, checks versions
- **MetricsCollector**: Aggregates all analysis results and calculates scores
- **ReportGenerator**: Generates Markdown and HTML reports using existing converter

**Key Features**:
- Cyclomatic complexity calculation
- Code style checking (line length, docstrings, naming)
- Best practices validation (tests, README, .gitignore, etc.)
- Dependency version analysis
- Overall project health score (0-100)
- Comprehensive HTML reports with professional theme

---

## Key Design Patterns

### 1. **Strategy Pattern**: Theme System
Different rendering strategies (themes) can be swapped without changing core logic.

### 2. **Template Method Pattern**: BaseTheme
`BaseTheme.render()` defines conversion skeleton; subclasses fill in specific styles/scripts.

### 3. **Facade Pattern**: HTMLConverter
Provides simplified interface to complex subsystems (processors, themes, markdown extensions).

### 4. **Dataclass Results**: ConversionResult
Immutable result objects with type safety for conversion outcomes.

---

## Markdown Extensions Used

The converter uses these `python-markdown` extensions:
- `tables`: GitHub-flavored tables
- `fenced_code`: Code blocks with syntax highlighting
- `codehilite`: Syntax highlighting with Pygments
- `toc`: Automatic table of contents with permalinks
- `sane_lists`: Better list parsing
- `nl2br`: Newline to `<br>` conversion
- `attr_list`: CSS classes and IDs on elements
- `def_list`: Definition lists
- `footnotes`: Footnote support
- `meta`: Metadata parsing from Markdown front matter
- `abbr`: Abbreviation support

---

## File Organization Logic

### Source Structure
```
src/
├── cli.py              # Command-line interface
├── interactive.py      # Interactive TUI
├── batch_processor.py  # Multi-file processing
├── config_manager.py   # Configuration persistence
├── core/
│   ├── converter.py    # Main conversion engine
│   └── stats.py        # Statistics tracking
├── processors/
│   ├── image_processor.py   # Image → Base64
│   └── mermaid_processor.py # Mermaid wrapping
├── themes/
│   ├── base.py         # Abstract base class
│   ├── default.py      # Default theme
│   ├── minimal.py      # Minimal theme
│   └── professional.py # Professional theme
├── analyzers/          # 🆕 Project analysis module
│   ├── base.py         # Base analyzer class
│   ├── project_analyzer.py      # Project structure analysis
│   ├── code_quality_analyzer.py # Code quality metrics
│   ├── dependency_analyzer.py   # Dependency analysis
│   ├── metrics_collector.py     # Metrics aggregation
│   ├── report_generator.py      # Report generation
│   └── templates/      # Report templates (future)
└── utils/
    ├── file_scanner.py # Markdown file discovery
    └── formatter.py    # CLI output formatting
```

### Configuration Storage
- User config: `~/.md2html/config.json`
- Presets: `~/.md2html/presets/*.json`

---

## Error Handling Strategy

Currently uses generic `Exception` catching in multiple places:
- `cli.py`: Top-level exception handler with traceback on `--verbose`
- `converter.py`: Returns `ConversionResult` with `success=False` and `error_message`
- `config_manager.py`: Prints warnings and returns default values on JSON errors

**Improvement needed**: Create custom exception hierarchy:
```python
class MD2HTMLError(Exception): pass
class FileNotFoundError(MD2HTMLError): pass
class ConversionError(MD2HTMLError): pass
class ThemeError(MD2HTMLError): pass
```

---

## Image Processing Flow

1. **Detection**: Regex finds `![alt](path)` in Markdown
2. **Path Resolution**: Relative paths resolved from source file directory
3. **Base64 Encoding**: Image read as binary, converted to data URI
4. **Replacement**: Original path replaced with `data:image/*;base64,...`
5. **Result**: Self-contained HTML with embedded images

**Supported formats**: PNG, JPG, JPEG, GIF, SVG, WEBP, BMP

---

## Mermaid Integration

Mermaid diagrams are rendered **client-side**:
1. Markdown code blocks with `mermaid` language tag are detected
2. Wrapped in `<div class="mermaid">` tags
3. Theme includes Mermaid.js CDN script
4. Browser renders diagrams on page load

**No server-side processing** - diagrams require JavaScript-enabled browser.

---

## Common Gotchas

### 1. Image Path Resolution
Images are resolved relative to the **source Markdown file**, not the working directory:
```python
# Correct
image_path = source_path.parent / relative_image_path

# Wrong
image_path = Path.cwd() / relative_image_path
```

### 2. Theme Registration
New themes must be added to `src/themes/__init__.py`:
```python
def get_theme(name: str) -> BaseTheme:
    themes = {
        'default': DefaultTheme,
        'minimal': MinimalTheme,
        'professional': ProfessionalTheme,
        'your_theme': YourTheme,  # Add here
    }
    ...
```

### 3. Markdown Instance Reuse
DO NOT reuse `markdown.Markdown()` instances across files:
```python
# Wrong - state persists between conversions
self.md = markdown.Markdown(...)
html = self.md.convert(content)

# Correct - create new instance per conversion
md = markdown.Markdown(...)
html = md.convert(content)
```

### 4. Config File Encoding
Always use `encoding='utf-8'` when reading/writing config files to support Chinese characters.

---

## Performance Considerations

### Current Bottlenecks
1. **Image Processing**: Large images are fully loaded into memory for Base64 encoding
2. **Sequential Processing**: Single-threaded by default in CLI mode
3. **Markdown Parser**: Creates new instance per file (necessary but expensive)

### Optimization Strategies
1. Use `batch_processor.py` for multi-file conversions (enables threading)
2. Consider image size limits or compression before encoding
3. Cache theme CSS/JS generation (currently regenerated per file)

---

## Testing Strategy (When Implemented)

Recommended test structure:
```
tests/
├── conftest.py              # Pytest fixtures
├── fixtures/                # Test data
│   ├── sample.md
│   └── images/
├── test_converter.py        # Core conversion tests
├── test_processors.py       # Image/Mermaid processing
├── test_themes.py           # Theme rendering tests
└── test_cli.py              # CLI argument parsing
```

Key test scenarios:
- Markdown → HTML conversion correctness
- Image embedding with various formats
- Mermaid code block detection and wrapping
- Theme CSS/JS generation
- Config persistence and migration
- Error handling for missing files/invalid input

---

## Project-Specific Conventions

### Naming
- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/methods**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`

### Docstrings
Use Google-style docstrings:
```python
def convert(self, source_path: Path, theme: str = "default") -> ConversionResult:
    """
    Convert Markdown file to HTML.

    Args:
        source_path: Path to Markdown file
        theme: Theme name (default: "default")

    Returns:
        ConversionResult with success status and metadata

    Raises:
        FileNotFoundError: If source_path does not exist
    """
```

### Type Hints
Use type hints for all function signatures:
```python
from pathlib import Path
from typing import Optional, List, Dict, Any

def process_files(
    files: List[Path],
    output_dir: Optional[Path] = None
) -> Dict[str, Any]:
    ...
```

---

## Deployment & Distribution

### Installation Methods
```bash
# Development mode
pip install -e .

# User mode (when published)
pip install md2html-converter

# Direct execution
python md2html.py
```

### Entry Point
`pyproject.toml` defines CLI command:
```toml
[project.scripts]
md2html = "cli:main"
```

After installation: `md2html report.md` works globally.

---

## Future Architecture Considerations

### Planned Improvements (from PROJECT_ANALYSIS_REPORT.md)
1. **Custom Exception Hierarchy**: Replace generic `Exception` with domain-specific errors
2. **Logging System**: Structured logging for debugging and production monitoring
3. **Plugin System**: Allow third-party themes and processors
4. **Template Engine**: Separate HTML templates from Python code
5. **Async Processing**: Use `asyncio` for concurrent I/O operations
6. **Caching Layer**: Cache parsed Markdown and theme resources

### Current Limitations
- No test coverage (0%)
- No formal logging (only `print()` statements)
- Image processing not optimized for large files
- No validation of user input paths
- Config migration strategy not defined

---

## Project Analysis Module (`analyzers/`)

### Overview

The `analyzers` module provides comprehensive project analysis capabilities, generating detailed reports about project structure, code quality, and dependencies. This is a **variable/extensible** part of the codebase designed to be customized for different analysis needs.

### Module Architecture

```
src/analyzers/
├── base.py                      # Abstract base class for all analyzers
│   ├── BaseAnalyzer             # Common analysis interface
│   └── AnalysisResult           # Standardized result format
├── project_analyzer.py          # Project structure analysis
│   └── ProjectAnalyzer          # File scanning, code statistics, directory tree
├── code_quality_analyzer.py     # Code quality metrics
│   └── CodeQualityAnalyzer      # Complexity, style, best practices
├── dependency_analyzer.py       # Dependency analysis
│   └── DependencyAnalyzer       # Parse requirements, check versions
├── metrics_collector.py         # Aggregate all metrics
│   └── MetricsCollector         # Run all analyzers, calculate scores
└── report_generator.py          # Generate reports
    └── ReportGenerator          # Markdown + HTML output
```

### Analysis Capabilities

#### 1. **Project Structure Analysis**
- File tree scanning with exclusion filters
- Code line counting (total, code, comments, blank)
- File type distribution
- Directory tree visualization
- Git repository information
- Project size calculation

#### 2. **Code Quality Analysis**
- **Cyclomatic Complexity**: Measures code complexity using AST analysis
- **Function Length**: Identifies overly long functions (>50 lines)
- **Code Style**: Checks line length (>100 chars), missing docstrings
- **Best Practices**: Validates presence of tests, README, requirements, .gitignore, LICENSE

#### 3. **Dependency Analysis**
- **Python**: Parses `requirements.txt` and `pyproject.toml`
- **Node.js**: Parses `package.json` (dependencies + devDependencies)
- **Version Analysis**: Identifies pinned vs flexible versions
- **Dependency Tree**: Generates hierarchical dependency view

#### 4. **Metrics Collection & Scoring**
- **Overall Score**: 0-100 points with letter grade (A-F)
- **Score Breakdown**:
  - Structure (30 points): Git repo, code lines, file diversity
  - Quality (40 points): Function length, style issues, complexity
  - Practices (30 points): Tests, docs, dependency management
- **Summary Generation**: Key metrics, highlights, concerns

### Usage Examples

```python
from pathlib import Path
from src.analyzers import ProjectAnalyzer, CodeQualityAnalyzer, ReportGenerator

# Analyze project structure
analyzer = ProjectAnalyzer(Path('/path/to/project'))
result = analyzer.analyze()
print(result.data['code_statistics'])

# Generate full report
generator = ReportGenerator(Path('/path/to/project'))
output_files = generator.generate_report(
    output_path=Path('my_report'),
    format='both'  # 'markdown', 'html', or 'both'
)
```

### Command-Line Interface

```bash
# Basic usage
python analyze_project.py

# Analyze specific project
python analyze_project.py /path/to/project

# Custom output location
python analyze_project.py -o reports/my_analysis

# Generate only Markdown
python analyze_project.py -f markdown

# Verbose mode with error details
python analyze_project.py -v
```

### Report Structure

Generated reports include:

1. **Executive Summary**
   - Overall score and grade
   - Score breakdown by category
   - Key metrics (files, lines, functions, classes)
   - Highlights and concerns

2. **Project Structure**
   - Project metadata (name, size, type)
   - Git information (branch, last commit)
   - File type distribution
   - Code statistics
   - Directory tree

3. **Code Quality**
   - Python code analysis (functions, classes, avg length)
   - Complexity analysis (avg, max, high-complexity functions)
   - Code style issues
   - Best practices checklist

4. **Dependency Analysis**
   - Python dependencies (requirements.txt/pyproject.toml)
   - Node.js dependencies (package.json)
   - Version management analysis
   - Dependency tree

5. **Diagnostic Information**
   - Errors encountered during analysis
   - Warnings and recommendations

### Extending the Analyzers

To add a new analyzer:

1. **Create analyzer class** inheriting from `BaseAnalyzer`:
```python
from .base import BaseAnalyzer, AnalysisResult

class MyCustomAnalyzer(BaseAnalyzer):
    def analyze(self) -> AnalysisResult:
        # Your analysis logic
        self.result.data['my_metric'] = self._calculate_metric()
        return self.result
```

2. **Register in `metrics_collector.py`**:
```python
from .my_custom_analyzer import MyCustomAnalyzer

class MetricsCollector(BaseAnalyzer):
    def analyze(self) -> AnalysisResult:
        # Add your analyzer
        custom_result = MyCustomAnalyzer(self.project_path).analyze()
        self.result.data['custom'] = custom_result.data
        return self.result
```

3. **Update report template** in `report_generator.py` to display new metrics

### Design Principles

- **Extensibility**: Easy to add new analyzers without modifying existing code
- **Modularity**: Each analyzer is independent and can be used standalone
- **Consistency**: All analyzers use `AnalysisResult` for standardized output
- **Error Handling**: Graceful degradation with warnings instead of failures
- **Performance**: File scanning with exclusion filters to avoid large directories

### Integration with Existing Tools

The analyzers module integrates seamlessly with the existing MD2HTML converter:
- `ReportGenerator` uses `HTMLConverter` to create HTML reports
- Generated Markdown reports can be converted using `md2html.py`
- Reports use the `professional` theme by default for technical documentation

---

## Related Documentation

- **Project Analysis**: `PROJECT_ANALYSIS_REPORT.md` - Comprehensive codebase analysis
- **Quick Start**: `QUICK_START_GUIDE.md` - 15-minute setup guide
- **Priority Matrix**: `PRIORITY_MATRIX.md` - Roadmap and task prioritization
- **Legacy Reports**: `legacy/` - Historical VCU project analysis documents

---

## Special Notes

### VCU Project Context
This tool originated from VCU (Vehicle Control Unit) project needs:
- Technical analysis reports (e.g., `VCU-CGT-SwUR-0126-分析报告.md`)
- Quality assurance documentation
- Error analysis templates

The `legacy/` directory contains original VCU reports that drove the tool's requirements.

### Chinese Language Support
- Full UTF-8 support throughout codebase
- Chinese characters in:
  - Markdown content
  - File paths (with proper encoding)
  - Configuration files
  - Error messages and CLI output

### Mermaid Diagram Types
Supported Mermaid diagrams:
- Flowcharts (`graph`, `flowchart`)
- Sequence diagrams (`sequenceDiagram`)
- Gantt charts (`gantt`)
- Class diagrams (`classDiagram`)
- State diagrams (`stateDiagram`)
- ER diagrams (`erDiagram`)
- User journey diagrams (`journey`)

All rendered client-side via Mermaid.js CDN.

---

**Last Updated**: 2025-10-11
**Claude Code Version**: Compatible with Sonnet 4.5
**Project Health Score**: 7.5/10 (see PROJECT_ANALYSIS_REPORT.md for details)
