# Contributing to Rift Protocol

Thank you for your interest in contributing to Rift Protocol! 🚀

## 📚 Getting Started

1. **Read the Documentation**
   - Start with [Technical Overview](docs/TECHNICAL_OVERVIEW.md)
   - Review [Architecture](docs/architecture.md)
   - Check [Getting Started](docs/getting_started.md)

2. **Set Up Development Environment**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd rift-core-internal

   # Create virtual environment
   python3 -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Build Contracts**
   ```bash
   cd contracts
   scarb build
   ```

## 🐛 Reporting Bugs

Please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots/logs if applicable

## 💡 Feature Requests

We welcome feature requests! Please:
1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Feature description
   - Use case / problem it solves
   - Proposed implementation (optional)

## 🔧 Pull Requests

We love your input! To contribute code:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
   - Run the demo: `./watcher/run-hackathon-demo.sh`
   - Build contracts: `scarb build`
   - Run tests if available
5. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
6. **Push to your branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

### PR Guidelines

- **Clear title and description**
- **Reference issues** (e.g., "Closes #123")
- **Include tests** if applicable
- **Update documentation** if needed
- **Follow existing code style**
- **Keep PRs focused** (one feature per PR)

## 📝 Code Style

### Python
- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Write meaningful variable names

### Cairo
- Follow Cairo best practices
- Use interface-implementation pattern
- Add comments for complex logic
- Include events for state changes

## 🧪 Testing

Before submitting a PR:
- ✅ Demo runs successfully
- ✅ Contracts compile without errors
- ✅ Existing tests pass
- ✅ New features have tests (if applicable)

## 📖 Documentation

Good documentation is crucial! When contributing:
- Update README if features change
- Add inline code comments
- Update relevant docs in `/docs`
- Include examples for new features

## 🎯 Areas We Need Help

### High Priority
- [ ] Executor contract implementation (Phase 4)
- [ ] Real Bitcoin node integration
- [ ] Frontend dashboard
- [ ] Comprehensive test suite

### Nice to Have
- [ ] Docker deployment
- [ ] CI/CD pipeline
- [ ] Monitoring/logging
- [ ] Performance optimizations

## 💬 Questions?

- **General questions**: Open a [Discussion](../../discussions)
- **Bug reports**: Create an [Issue](../../issues)
- **Contact**: See [README.md](README.md) for contact info

## 🏆 Contributors

We appreciate all contributions, big or small! Every PR helps make Rift Protocol better.

---

<div align="center">

**⚡ Making Bitcoin Instant**

Built with ❤️ by the Rift Protocol Team

</div>
