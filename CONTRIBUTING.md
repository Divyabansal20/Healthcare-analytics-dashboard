# Contributing to Healthcare Analytics Dashboard

Thank you for your interest in contributing! This document provides guidelines and steps for contributing.

## How to Contribute

### 1. Fork the Repository
```bash
git clone https://github.com/divyabansal/healthcare-dashboard.git
cd healthcare-dashboard
```

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Follow PEP 8 style guide
- Add docstrings to new functions
- Update README if needed

### 4. Test Your Changes
```bash
pip install -r requirements.txt
streamlit run app.py
```

### 5. Commit Your Changes
```bash
git add .
git commit -m "Add: description of your changes"
```

### 6. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 7. Create a Pull Request
- Go to the original repository
- Click "New Pull Request"
- Select your branch
- Add a clear title and description

## Reporting Issues

- Use the GitHub issue tracker
- Include steps to reproduce the issue
- Include expected and actual behavior
- Include Python version and OS

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use meaningful variable names
- Add comments for complex logic
- Keep functions under 50 lines

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
