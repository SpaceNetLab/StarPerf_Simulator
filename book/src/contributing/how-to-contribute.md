# How to Contribute

We welcome and appreciate contributions to StarPerf! This guide will help you get started.

## Ways to Contribute

### 1. Bug Reports 🐛

Found a bug? Help us improve by reporting it!

**Where to report:**
- [GitHub Issues](https://github.com/SpaceNetLab/StarPerf_Simulator/issues)

**What to include:**
- Clear, descriptive title
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- Error messages and stack traces
- Screenshots if applicable

**Template:**
```markdown
**Description**
Clear description of the bug

**To Reproduce**
1. Step one
2. Step two
3. See error

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: macOS 13.0
- Python: 3.10.5
- StarPerf: 2.0

**Additional Context**
Any other relevant information
```

### 2. Feature Requests 💡

Have an idea for a new feature?

**Submit via:**
- GitHub Issues with `[Feature Request]` label

**Include:**
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if you have ideas)
- Alternative solutions considered

### 3. Code Contributions 💻

Ready to write code? Great!

**Process:**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

See [Development Workflow](#development-workflow) below for details.

### 4. Documentation 📚

Help make StarPerf easier to use!

**Areas:**
- User guides and tutorials
- API documentation
- Code examples
- README improvements
- Typo fixes

### 5. Constellation Designs 🛰️

Contribute new constellation configurations!

**What we need:**
- New XML constellation configs
- Real TLE data for additional constellations
- Validation data and benchmarks
- Ground station and POP configurations

### 6. Test Cases 🧪

Improve code quality with tests!

**Types:**
- Unit tests for individual functions
- Integration tests for workflows
- Performance benchmarks
- Edge case scenarios

## Development Workflow

### Step 1: Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/StarPerf_Simulator.git
cd StarPerf_Simulator

# Add upstream remote
git remote add upstream https://github.com/SpaceNetLab/StarPerf_Simulator.git
```

### Step 2: Set Up Environment

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Verify installation
uv run python StarPerf.py
```

### Step 3: Create Branch

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch with descriptive name
git checkout -b feature/add-new-routing-plugin
# or
git checkout -b fix/satellite-position-bug
# or
git checkout -b docs/improve-api-reference
```

**Branch naming conventions:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `test/description` - Test additions

### Step 4: Make Changes

Write your code following our [Code Style Guide](./code-style.md).

**Guidelines:**
- Write clear, self-documenting code
- Add comments for complex logic
- Include docstrings for all functions
- Follow existing patterns in the codebase

**Example:**
```python
def calculate_satellite_coverage(
    satellite: Satellite,
    h3_resolution: int = 2,
    minimum_elevation: float = 25.0
) -> List[str]:
    """
    Calculate H3 cells covered by satellite.

    Args:
        satellite: Satellite object to analyze
        h3_resolution: H3 grid resolution (0-4)
        minimum_elevation: Minimum elevation angle in degrees

    Returns:
        List of H3 cell IDs covered by satellite

    Raises:
        ValueError: If resolution is not in range 0-4
    """
    if not 0 <= h3_resolution <= 4:
        raise ValueError(f"Resolution must be 0-4, got {h3_resolution}")

    # Implementation
    covered_cells = []
    # ...
    return covered_cells
```

### Step 5: Test Your Changes

```bash
# Run existing tests (if available)
uv run python -m pytest tests/

# Test your specific changes
uv run python samples/your_test_case.py

# Manual testing
uv run python StarPerf.py
```

### Step 6: Commit Changes

Write clear, descriptive commit messages:

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "Add: New routing plugin for shortest path with QoS

- Implement QoS-aware shortest path algorithm
- Add tests for QoS routing
- Update documentation with usage example
- Fixes #123"
```

**Commit message format:**
```
Type: Brief description (50 chars or less)

More detailed explanation if needed. Wrap at 72 characters.

- Bullet points for multiple changes
- Reference issues: Fixes #123, Relates to #456
```

**Commit types:**
- `Add:` New features
- `Fix:` Bug fixes
- `Update:` Updates to existing features
- `Remove:` Removal of code
- `Refactor:` Code refactoring
- `Docs:` Documentation changes
- `Test:` Test additions/changes

### Step 7: Push and Create PR

```bash
# Push to your fork
git push origin feature/add-new-routing-plugin
```

Then on GitHub:
1. Navigate to your fork
2. Click "Compare & pull request"
3. Fill out the PR template
4. Submit the pull request

**PR Title Format:**
```
[Type] Brief description

Examples:
[Feature] Add QoS-aware routing plugin
[Fix] Correct satellite position calculation
[Docs] Improve installation guide
```

**PR Description Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tested locally
- [ ] Added new tests
- [ ] All existing tests pass

## Related Issues
Fixes #123
Relates to #456

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Review Process

### What Happens Next

1. **Automated Checks**
   - CI/CD pipeline runs (if configured)
   - Code quality checks
   - Test execution

2. **Code Review**
   - Maintainer reviews your code
   - May request changes
   - Discussion and iteration

3. **Approval and Merge**
   - Once approved, PR is merged
   - Your contribution is part of StarPerf!

### Review Timeline

- **Initial review**: Within 1 week
- **Follow-up**: 2-3 business days
- **Approval**: When all feedback is addressed

### Responding to Feedback

```bash
# Make requested changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Update: Address review feedback

- Fix variable naming as suggested
- Add error handling
- Improve documentation"

# Push updates
git push origin feature/add-new-routing-plugin
```

The PR automatically updates with your new commits.

## Contribution Standards

### Code Quality

- ✅ Follow PEP 8 style guide
- ✅ Include type hints
- ✅ Write docstrings
- ✅ Add comments for complex logic
- ✅ Keep functions focused and small
- ✅ Use descriptive variable names

### Testing

- ✅ Test your changes thoroughly
- ✅ Add automated tests if possible
- ✅ Verify existing tests still pass
- ✅ Test edge cases

### Documentation

- ✅ Update relevant documentation
- ✅ Add docstrings to new functions
- ✅ Include usage examples
- ✅ Update CHANGELOG (if applicable)

## Communication

### Be Respectful

- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Clear

- Provide context in issues and PRs
- Explain your reasoning
- Ask questions if something is unclear
- Respond to feedback promptly

## Getting Help

Stuck? Need guidance?

1. **Check Documentation**
   - Read relevant sections
   - Review examples
   - Check API reference

2. **Search Existing Issues**
   - Someone may have asked before
   - Check closed issues too

3. **Ask Questions**
   - Open a GitHub Discussion
   - Email the development team
   - Be specific about your problem

4. **Join the Community**
   - Engage in discussions
   - Help others
   - Share your experiences

## Recognition

Contributors are recognized through:

- 🏆 GitHub contributors list
- 📝 Acknowledgments in documentation
- 🎯 Mentions in release notes
- 🌟 Featured on contributors page

Significant contributors may be invited to join as maintainers!

## License

By contributing, you agree that your contributions will be licensed under the BSD-2-Clause License. See [License](../about/license.md) for details.

## Questions?

Have questions about contributing?

- 📧 Email: houyn24@mails.tsinghua.edu.cn
- 💬 GitHub Discussions
- 📝 Open an issue

---

**Thank you for contributing to StarPerf!** 🚀

---

[Next: Writing Plugins →](./writing-plugins.md)
