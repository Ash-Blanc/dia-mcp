# Contributing to dia-mcp 🎨

First off, thank you for considering contributing to the UX Inspo Engine! It's people like you who make this a great tool for the design community.

## 🚀 Getting Started

1. **Fork the repo** and clone it locally.
2. **Install `uv`**: We use `uv` for lightning-fast dependency management.
3. **Setup environment**:
   ```bash
   uv sync
   cp .env.example .env
   # Add your FIRECRAWL_API_KEY and TINYFISH_API_KEY
   ```
4. **Run the server**:
   ```bash
   uv run dia-mcp
   ```

## 🛠️ Code Style & Standards

We maintain high engineering standards to keep the engine reliable and fast.

- **Formatting**: We use [Ruff](https://github.com/astral-sh/ruff). Run `uv run ruff format src/` before committing.
- **Linting**: Run `uv run ruff check src/`.
- **Type Checking**: We use [Pyright](https://github.com/microsoft/pyright). Run `uv run pyright src/`.
- **Imports**: Always use `from __future__ import annotations`. Group imports as: stdlib -> third-party -> local.

## 🏹 Building New Tools

If you're adding a new capability to the engine:

1. Create a new module in `src/dia/tools/`.
2. Use the `@mcp.tool` decorator.
3. **Persona-Driven Goals**: When using TinyFish or Firecrawl agents, always provide a clear, expert persona (e.g., "Senior Interaction Designer").
4. **Structured Data**: Prefer JSON schemas for extraction to ensure results are machine-readable and consistent.
5. **Emoji in Docs**: Add a representative emoji at the start of your tool's docstring.

## 🧪 Testing

Every new feature or bug fix must include tests.

- **Mocking**: Never hit real APIs in CI. Use `unittest.mock` to mock Firecrawl and TinyFish responses.
- **Run tests**:
  ```bash
  uv run pytest
  ```

## 📝 Documentation

- Update `README.md` if you add a new tool.
- Update `EXAMPLES.md` with a best-practice prompt for your new feature.
- Use clear, Google-style docstrings for all functions.

## 📮 Pull Request Process

1. Create a new branch: `git checkout -b feat/your-feature-name`.
2. Make your changes and add tests.
3. Ensure all checks pass: `uv run ruff check src/ && uv run pyright src/ && uv run pytest`.
4. Submit a PR using our template.

---

By contributing, you agree that your contributions will be licensed under the project's MIT License.
