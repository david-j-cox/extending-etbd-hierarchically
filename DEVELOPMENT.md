# Development Workflow

This document outlines the development workflow for the ETBD project.

## Branching Strategy

### **Main Branch (`main`)**
- **Purpose**: Production-ready, stable code
- **When to use**: Only for completed features that have been tested
- **Protection**: Should be protected from direct pushes

### **Development Branch (`dev`)**
- **Purpose**: Active development and feature integration
- **When to use**: For ongoing development work, feature branches, and testing
- **Current status**: Active development branch

## Development Workflow

### **Starting New Work**

1. **Ensure you're on the dev branch:**
   ```bash
   git checkout dev
   git pull origin dev
   ```

2. **Create a feature branch for your work:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit regularly:**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

### **Completing Work**

1. **Push your feature branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** from your feature branch to `dev`

3. **After review and testing, merge to `dev`**

### **Releasing to Production**

1. **When `dev` is stable and ready:**
   ```bash
   git checkout main
   git merge dev
   git push origin main
   ```

2. **Create a release tag:**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

## Current Development Focus

### **Planned Features:**
- [ ] Hierarchical ETBD extensions
- [ ] Additional reinforcement schedules
- [ ] Advanced analysis tools
- [ ] Parameter optimization
- [ ] Visualization improvements

### **Code Standards:**
- Follow PEP 8 for Python code
- Add docstrings to all functions
- Include type hints where appropriate
- Write tests for new features

## Testing

### **Running Tests:**
```bash
cd scripts_notebooks
python test_etbd.py
```

### **Running Examples:**
```bash
cd scripts_notebooks
python example_usage.py
python quick_demo.py
```

## File Organization

- **`scripts_notebooks/`** - All Python code
- **`figures/`** - Generated plots (gitignored)
- **`data/`** - Generated data (gitignored)
- **`venv/`** - Virtual environment (gitignored)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request to `dev`
