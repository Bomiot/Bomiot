# Support

## Getting Help

If you need help with Bomiot, here are several ways to get support:

### 📚 Documentation
- [Bomiot Wiki](https://github.com/Bomiot/Bomiot/wiki)
- [API Documentation](https://github.com/Bomiot/Bomiot/wiki/API-Documentation)
- [YouTube Tutorials](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)

### 🐛 Bug Reports
If you found a bug, please:
1. Check if it's already reported in [Issues](https://github.com/Bomiot/Bomiot/issues)
2. Create a new issue using our [Bug Report Template](https://github.com/Bomiot/Bomiot/issues/new?template=bug_report.md)

### 💡 Feature Requests
Have an idea for a new feature? Please:
1. Check if it's already requested in [Issues](https://github.com/Bomiot/Bomiot/issues)
2. Create a new issue using our [Feature Request Template](https://github.com/Bomiot/Bomiot/issues/new?template=feature_request.md)

### 🔒 Security Issues
Found a security vulnerability? Please:
- **DO NOT** create a public issue
- Create a [Security Advisory](https://github.com/Bomiot/Bomiot/security/advisories/new)
- Contact [@Singosgu](https://github.com/Singosgu) directly
- See our [Security Policy](SECURITY.md) for more details

### 💬 Community Support
- **GitHub Discussions**: [Bomiot Discussions](https://github.com/Bomiot/Bomiot/discussions)
- **Issues**: [GitHub Issues](https://github.com/Bomiot/Bomiot/issues)
- **YouTube**: [Bomiot Channel](https://www.youtube.com/channel/UCPW1wciGMIEh7CYOdLnsloA)

### 📧 Direct Contact
- **GitHub**: [@Singosgu](https://github.com/Singosgu)
- **Project**: [Bomiot/Bomiot](https://github.com/Bomiot/Bomiot)

## Common Issues

### Installation Problems
```bash
# Make sure you have the right Python version
python --version  # Should be 3.9+

# Make sure you have the right Node.js version
node --version  # Should be 18.19.1+

# Try upgrading pip
python -m pip install --upgrade pip

# Install in a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install frontend dependencies
cd bomiot/templates
yarn install
```

### Configuration Issues
- Check your `setup.ini` or `bomiotconf.ini` file exists and has correct values
- Verify database connection settings
- Ensure all required environment variables are set
- Check Bomiot initialization: `bomiot init`

### Database Issues
```bash
# Check database connection
bomiot dbshell

# Run migrations
bomiot makemigrations
bomiot migrate

# Check for pending migrations
bomiot showmigrations

# Reset database (if needed)
bomiot flush
```

### Frontend Issues
```bash
# Install dependencies
cd bomiot/templates
yarn install

# Build frontend
yarn build

# Development mode
yarn dev
```

### Performance Issues
- Check system resources (CPU, memory, disk)
- Review database query performance
- Monitor network connectivity
- Check Bomiot logs in `logs/` directory

## Troubleshooting

### Logs
Enable debug logging by setting:
```bash
export LOG_LEVEL=DEBUG
bomiot run --log-level debug
```

### Health Check
Run the health check endpoint:
```bash
curl http://localhost:8000/health
```

### Reset Admin Password
```bash
bomiot initpwd
```

### Plugin Issues
```bash
# List installed plugins
bomiot plugins list

# Install plugin from market
bomiot market <plugin_name>

# Create new plugin
bomiot plugins <plugin_name>
```

## Version Compatibility

| Component | Minimum Version | Recommended Version |
|-----------|----------------|-------------------|
| Python    | 3.9            | 3.11              |
| Node.js   | 18.19.1        | 18.19.1           |
| Django    | 4.2            | 4.2+              |
| Vue       | 3.4.18         | 3.4.18+           |
| Quasar    | 2.4.1          | 2.4.1+            |
| Database  | SQLite (default) | PostgreSQL/MySQL |

## Deployment Support

### Development Environment
```bash
bomiot run --host 0.0.0.0 --port 8000
```

### Production Environment
```bash
# Using Gunicorn
gunicorn bomiot.server.server.asgi:application -w 4 -k uvicorn.workers.UvicornWorker

# Using Docker
docker build -t bomiot .
docker run -p 8000:8000 bomiot
```

## Contributing

Want to help improve Bomiot? See our [Contributing Guide](CONTRIBUTING.md).

## Acknowledgments

Thanks to all our contributors and users for their support and feedback! 