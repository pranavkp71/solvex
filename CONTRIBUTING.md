# Contributing to Solvex

Thank you for considering contributing to Solvex. This document will guide you through the contribution process.

---

## Ways to Contribute

We welcome contributions in many forms:

- **Bug reports** - Help us identify and fix issues
- **Feature requests** - Suggest new algorithms or improvements
- **Documentation** - Improve guides, examples, or API docs
- **Code contributions** - Add features, fix bugs, optimize performance
- **Tests** - Improve test coverage
- **Examples** - Add real-world use case examples

---

## Quick Start

### Prerequisites

- Python 3.11+
- uv installed (pip install uv or use installer)

**Fork the repository and clone your fork**


### Setup Development Environment
   You have two options: using a virtual environment (recommended) or letting `uv` manage isolation.
   
**Option 1: With virtual environment (recommended)**  
```bash
git clone <your repo link>

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install uv 
pip install uv
uv sync
```

**Option 2: Without virtual environment** 
```bash
git clone <your repo link>

# Install uv globally or in your Python environment
pip install uv
uv sync      # Install all project dependencies in uv-managed environment


```


**Run the development server**
````bash
   uv run uvicorn main:app --reload
````


**Linting & Formatting**
````bash
   uv run ruff check .
   uv run ruff check . --fix   # Automatically fix simple issues
````


**Run tests to verify setup**
````bash
   uv run pytest -v
````

---

## 🔄 Contribution Workflow

### 1. Create a Branch

````bash
git checkout -b feature/your-feature
````

### 2. Make changes & test

````bash
uv run pytest
````
### 3. Run lint and format

````bash
uv run ruff check .
uv run ruff format .
````
### 4. Commit & push

### 5. Open a Pull Request
  Explain your changes clearly and link related issues

---

**Before submitting a PR**
- Code passes Ruff checks
- Tests pass (uv run pytest)
- Updated docs if needed

---

## Code Review 

All PRs are reviewed for clarity, correctness, and consistency.
Small, focused PRs are preferred over large ones.

---

## Communication

### Where to Ask Questions

- **Bug reports** - [GitHub Issues](https://github.com/pranavkp71/solvex/issues)
- **Feature requests** - [GitHub Issues](https://github.com/pranavkp71/solvex/issues)
- **General questions** - [GitHub Discussions](https://github.com/pranavkp71/solvex/discussions)
- **Private inquiries** - pranavkp170@gmail.com

### Code of Conduct

Be respectful, inclusive, and constructive. We're all here to learn and build something useful together.

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in project updates
---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You

Every contribution, no matter how small, makes Solvex better. Thank you for being part of this project.

**Questions?** Open a discussion or reach out at pranavkp170@gmail.com

---

**Happy Contributing**
