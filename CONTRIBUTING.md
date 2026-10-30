# Contributing to Mouse Pilot

Thank you for considering contributing to Mouse Pilot! This document provides guidelines and instructions for contributing.

---

## 🌟 Ways to Contribute

### Bug Reports
- Check if the issue already exists
- Use a clear, descriptive title
- Provide steps to reproduce
- Include system information (Windows version, Python version)
- Attach screenshots if relevant

### Feature Requests
- Search existing feature requests first
- Clearly describe the feature and its benefits
- Explain use cases
- Consider implementation complexity

### Code Contributions
- Fix bugs
- Add new features
- Improve documentation
- Write tests
- Optimize performance

### Documentation
- Fix typos or clarify instructions
- Add usage examples
- Create tutorials or guides
- Improve code comments

---

## 🚀 Getting Started

### 1. Fork and Clone

```powershell
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/mouse-pilot.git
cd mouse-pilot
```

### 2. Set Up Development Environment

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### 3. Create a Branch

```powershell
# Create and switch to feature branch
git checkout -b feature/my-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

---

## 💻 Development Workflow

### Project Structure

```
mouse-pilot/
├── main.py              # Entry point
├── ui/                  # GUI components
│   ├── main_window.py   # Main window & dialogs
│   └── styles.py        # Themes & stylesheets
├── services/            # Business logic
│   ├── mouse_controller.py
│   ├── scheduler.py
│   ├── keep_awake.py
│   ├── settings_manager.py
│   └── tray_manager.py
└── tests/               # Unit tests
```

### Coding Standards

#### Python Style
- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for classes and public methods

#### Example:
```python
def move_cursor(self, distance: int = 5) -> None:
    """
    Move cursor by specified distance and return to original position.
    
    Args:
        distance: Number of pixels to move (default: 5)
    """
    pass
```

### Writing Tests

Always add tests for new features:

```python
# tests/test_new_feature.py
import pytest
from services.new_feature import NewFeature


def test_new_feature():
    """Test that new feature works correctly"""
    feature = NewFeature()
    result = feature.do_something()
    assert result == expected_value
```

### Running Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=ui

# Run specific test
pytest tests/test_scheduler.py -v
```

### Code Quality

```powershell
# Format code with Black
black main.py services/ ui/ tests/

# Check style with Flake8
flake8 main.py services/ ui/ tests/ --max-line-length=100
```

---

## 🔧 Making Changes

### 1. Make Your Changes
- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update docstrings

### 2. Add Tests
- Write tests for new functionality
- Ensure existing tests still pass
- Aim for good test coverage

### 3. Update Documentation
- Update README.md if needed
- Update USAGE.md for new features
- Add docstrings to new functions
- Comment complex code

### 4. Test Your Changes

```powershell
# Run tests
pytest

# Test the application
python main.py

# Build executable (if changing build process)
.\build.ps1

# Test executable
.\dist\MousePilot.exe
```

---

## 📤 Submitting Changes

### 1. Commit Your Changes

```powershell
# Stage files
git add .

# Commit with descriptive message
git commit -m "Add feature: configurable movement patterns"
```

#### Commit Message Format:
- **Add**: New feature
- **Fix**: Bug fix
- **Update**: Existing feature improvement
- **Docs**: Documentation changes
- **Test**: Test additions or changes
- **Refactor**: Code restructuring
- **Style**: Formatting, no code change

#### Examples:
```
Add: Multi-pattern cursor movement (circle, figure-8)
Fix: Crash when minimizing to tray
Update: Improve settings dialog layout
Docs: Add usage examples for keep-awake mode
Test: Add tests for scheduler pause/resume
```

### 2. Push to Your Fork

```powershell
git push origin feature/my-feature-name
```

### 3. Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Select base: `main` ← compare: `feature/my-feature-name`
4. Fill out the PR template:
   - **Description**: What does this PR do?
   - **Motivation**: Why is this change needed?
   - **Testing**: How did you test this?
   - **Screenshots**: If UI changes, include before/after

---

## 🎯 Feature Ideas

### High Priority
- [ ] Start with Windows support
- [ ] User activity detection for auto-pause
- [ ] Operating hours restrictions
- [ ] Configurable movement patterns

### Medium Priority
- [ ] Activity logging
- [ ] Multi-language support
- [ ] Portable mode
- [ ] Keyboard shortcuts

### Low Priority
- [ ] Update checker
- [ ] Advanced scheduling rules
- [ ] Themes customization
- [ ] Statistics dashboard

---

## 🐛 Bug Fix Guidelines

### Investigation
1. Reproduce the bug consistently
2. Identify root cause
3. Check if it affects other areas
4. Consider edge cases

### Fix Implementation
1. Fix the root cause, not just symptoms
2. Add test to prevent regression
3. Verify fix doesn't break other features
4. Test on clean environment

### Bug Fix PR Checklist
- [ ] Bug is consistently reproducible
- [ ] Root cause identified
- [ ] Fix implemented and tested
- [ ] Regression test added
- [ ] No new bugs introduced
- [ ] Documentation updated if needed

---

## 📋 PR Review Process

### What to Expect
1. **Initial Review**: Maintainer reviews within 3-7 days
2. **Feedback**: May request changes or improvements
3. **Discussion**: Open dialogue about implementation
4. **Approval**: Once approved, PR will be merged
5. **Thanks**: Contributor credited in release notes

### Review Criteria
- Code quality and style
- Test coverage
- Documentation completeness
- No breaking changes (unless discussed)
- Performance impact
- Security considerations

---

## 🔐 Security

### Reporting Security Issues
- **DO NOT** open public issues for security bugs
- Email security concerns privately
- Allow time for fix before public disclosure

### Security Considerations
- Never log sensitive data
- Validate all user inputs
- Use secure Windows APIs
- Follow least privilege principle
- No network communications without explicit reason

---

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discriminatory language
- Personal attacks
- Trolling or insulting comments
- Publishing others' private information

---

## ❓ Questions?

- **General questions**: GitHub Discussions
- **Bug reports**: GitHub Issues
- **Feature requests**: GitHub Issues with `enhancement` label
- **Security concerns**: Private email (see SECURITY.md)

---

## 🎉 Recognition

Contributors will be:
- Listed in release notes
- Credited in CONTRIBUTORS.md (coming soon)
- Thanked publicly in project

---

**Thank you for contributing to Mouse Pilot! 🚀**
