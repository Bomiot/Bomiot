# Contributing to Bomiot

We love your input! We want to make contributing to Bomiot as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github
We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)
We use GitHub Flow, so all code changes happen through Pull Requests. Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## We Use [Conventional Commits](https://www.conventionalcommits.org/)
We use Conventional Commits for commit messages. This helps with automated changelog generation and semantic versioning.

### Commit Message Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools such as documentation generation

### Scopes
- `backend`: Django/Python backend changes
- `frontend`: Vue.js/Quasar frontend changes
- `cli`: Command line interface changes
- `plugin`: Plugin system changes
- `docs`: Documentation changes
- `config`: Configuration changes

## Any contributions you make will be under the Software License
In short, when you submit code changes, your submissions are understood to be under the same [APLv2](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issue tracker](https://github.com/Bomiot/Bomiot/issues)
We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/Bomiot/Bomiot/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected to happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License
By contributing, you agree that your contributions will be licensed under its APLv2 License.

## References
This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918afde44dea68b5f9f39b7d9b00/CONTRIBUTING.md).

## Development Setup

### Prerequisites
- Python 3.9+
- Node.js 18.19.1+
- Git

### Local Development
1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   cd bomiot/templates
   yarn install
   ```
5. Initialize Bomiot:
   ```bash
   bomiot init
   bomiot makemigrations
   bomiot migrate
   bomiot initadmin
   ```
6. Set up pre-commit hooks:
   ```bash
   pip install pre-commit
   pre-commit install
   ```
7. Run tests:
   ```bash
   pytest
   ```

### Code Style
We use:
- **Black** for Python code formatting
- **isort** for import sorting
- **flake8** for linting
- **pre-commit** for git hooks
- **ESLint** for JavaScript/TypeScript linting
- **Prettier** for frontend code formatting

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Test both backend and frontend components

### Documentation
- Update documentation for any API changes
- Add docstrings for new functions/classes
- Update README if needed
- Keep Wiki pages up to date

### Plugin Development
If you're developing plugins:
1. Create your plugin using `bomiot plugins <plugin_name>`
2. Follow the plugin development guidelines
3. Test your plugin thoroughly
4. Document your plugin's features and usage

## Getting Help
- Check existing issues and discussions
- Join our [GitHub Discussions](https://github.com/Bomiot/Bomiot/discussions)
- Watch our [YouTube tutorials](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)
- Contact maintainers directly

Thank you for contributing to Bomiot! 🎉 