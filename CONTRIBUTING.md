# Contributing to catpic

Thank you for contributing! This guide keeps things simple so you can focus on writing good code.

## Core Principle

Each language implementation is **self-contained**. Everything needed to build, test, and use an implementation lives in its language directory.

## Directory Structure

```
project-root/
├── docs/              # Shared documentation
├── spec/              # What all implementations must do
├── python/            # Complete Python project
├── c/                 # Complete C project
└── [language]/        # Your new implementation
```

## Basic Requirements

All contributions must:

1. **Follow the spec**: Implement what's defined in `spec/`
2. **Match the API**: Function names, parameters, and behavior should be equivalent across languages
3. **Pass test vectors**: Use the shared tests in `spec/test-vectors.json`
4. **Be self-contained**: Your language directory should build and run independently
5. **Include documentation**: Explain how to build and use your code

### Language-Agnostic API

Users should be able to switch languages with minimal friction. If Python has `calculate(input, options)`, then C should have `calculate()` with equivalent parameters, and Rust should have `calculate()`.

Use language conventions (snake_case vs camelCase, etc.) but keep concepts identical:
- Same function/method names (adjusted for language style)
- Same parameters in the same order
- Same return types (conceptually)
- Same error conditions and handling approach

## Adding a New Language

Create a directory structure like this:

```
rust/
├── README.md          # How to build, test, and use
├── src/               # Your source code
├── tests/             # Your tests (must include test vectors)
└── examples/          # At least one working example
```

Then:
- Add a CI workflow in `.github/workflows/rust.yml`
- Add your language to the table in root `README.md`
- Link to detailed docs in `docs/implementations/rust.md`

**That's it.** Use whatever tools and conventions are standard for your language.

## Modifying Existing Code

- Python changes go in `python/`
- C changes go in `c/`
- Keep changes focused on one thing
- Tests must pass

Language-specific style guides live in each implementation's directory (e.g., `python/README.md`).

## Changing Specifications

Spec changes affect all implementations. Open an issue first to discuss impact.

## Testing

Your implementation must:
- Include its own test suite using standard tooling for your language
- Provide a `test-config.toml` that describes how to run tests
- Pass all test vectors from `spec/test-vectors.json`

### Test Configuration

Create `[language]/test-config.toml`:

```toml
[build]
command = "make"           # How to build (optional)

[test]
command = "make test"      # How to run tests
working_dir = "."          # Relative to language directory

[compliance]
command = "make test-vectors"  # How to run spec compliance tests
expected_exit = 0              # Expected exit code for success
```

Examples:

**Python** (`python/test-config.toml`):
```toml
[test]
command = "uv run pytest"

[compliance]
command = "uv run pytest tests/test_compliance.py"
```

**C** (`c/test-config.toml`):
```toml
[build]
command = "make"

[test]
command = "make test"

[compliance]
command = "make test-vectors"
```

The root `scripts/test-all.sh` uses these configs to validate all implementations automatically.

## Pull Requests

- Use clear PR titles: `[Language] What you changed`
- One logical change per PR
- Update docs if you change behavior
- Make sure tests pass

## Questions?

Open an issue. We'll figure it out together.

---

**Keep it simple. Keep it working. Keep it documented.**
