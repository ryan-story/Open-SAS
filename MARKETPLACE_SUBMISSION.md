# VS Code Marketplace Submission Guide

This guide provides step-by-step instructions for submitting the Open-SAS extension to the VS Code Marketplace.

## Prerequisites

1. **Microsoft Account**: You need a Microsoft account to publish extensions
2. **Visual Studio Code**: Install VS Code and the VS Code Extension Manager (vsce)
3. **Node.js**: Required for building the extension

## Installation Steps

### 1. Install VS Code Extension Manager (vsce)

```bash
npm install -g vsce
```

### 2. Install Dependencies

```bash
cd vscode-extension
npm install
```

### 3. Build the Extension

```bash
npm run compile
```

### 4. Package the Extension

```bash
vsce package
```

This creates a `.vsix` file that can be installed locally or published to the marketplace.

## Publishing to Marketplace

### 1. Create Publisher Account

1. Go to [Visual Studio Marketplace](https://marketplace.visualstudio.com/manage)
2. Sign in with your Microsoft account
3. Create a new publisher account
4. Use publisher ID: `ryan-story`

### 2. Get Personal Access Token

1. Go to [Azure DevOps](https://dev.azure.com)
2. Sign in with your Microsoft account
3. Go to User Settings → Personal Access Tokens
4. Create a new token with "Marketplace" scope
5. Copy the token (you'll need it for publishing)

### 3. Login to vsce

```bash
vsce login ryan-story
```

Enter your Personal Access Token when prompted.

### 4. Publish the Extension

```bash
vsce publish
```

## Extension Details

### Basic Information
- **Name**: Open-SAS
- **Publisher**: ryan-story
- **Version**: 0.1.0
- **Description**: SAS syntax highlighting and execution support for .osas files with Python backend

### Categories
- Programming Languages
- Snippets
- Other

### Keywords
- sas
- statistics
- data-analysis
- python
- open-source

### Supported File Types
- `.osas` - Open-SAS files
- `.sas` - SAS files
- `.osasnb` - Open-SAS notebooks

## Marketplace Listing

### Short Description
"SAS syntax highlighting and execution support for .osas files with Python backend"

### Long Description
```markdown
# Open-SAS VS Code Extension

SAS syntax highlighting and execution support for VS Code with Python backend.

## Features

- **Syntax Highlighting**: Full SAS syntax highlighting for `.osas` and `.sas` files
- **Code Snippets**: Common SAS patterns and procedures
- **File Execution**: Run Open-SAS files directly from VS Code
- **Notebook Support**: Interactive SAS notebooks with `.osasnb` files
- **IntelliSense**: Code completion and syntax checking
- **Integrated Terminal**: View results in VS Code's integrated terminal

## Supported SAS Features

- DATA Steps with DATALINES support
- PROC MEANS with CLASS variables and OUTPUT statements
- PROC FREQ with cross-tabulations and options
- PROC SORT with ascending/descending order
- PROC PRINT for data display
- Macro variables (%LET, %PUT)
- Library (LIBNAME) functionality

## Installation

1. Install this extension
2. Install the Open-SAS Python package: `pip install open-sas`
3. Install the Jupyter kernel: `python -m open_sas.kernel install`

## Usage

Create `.osas` files and use `Ctrl+Shift+P` → "Open-SAS: Run File" to execute your SAS code.

## Demo

Check out the comprehensive demo in the project repository: [osas_walkthrough.ipynb](https://github.com/ryan-story/Open-SAS/blob/main/osas_walkthrough.ipynb)

## Requirements

- Python 3.8 or higher
- Open-SAS Python package
- VS Code 1.60.0 or higher

## Links

- [GitHub Repository](https://github.com/ryan-story/Open-SAS)
- [Documentation](https://github.com/ryan-story/Open-SAS/wiki)
- [Issue Tracker](https://github.com/ryan-story/Open-SAS/issues)
```

## Post-Publication

### 1. Update Version
After publishing, update the version in `package.json` for future releases.

### 2. Monitor Reviews
Check the marketplace for user reviews and feedback.

### 3. Update Documentation
Keep the README and documentation updated based on user feedback.

## Troubleshooting

### Common Issues

1. **Build Errors**: Make sure all dependencies are installed
2. **Publishing Errors**: Verify your Personal Access Token has the correct permissions
3. **Version Conflicts**: Ensure version numbers are incremented for each release

### Support

For issues with the extension or marketplace submission:
- Check the [VS Code Extension Documentation](https://code.visualstudio.com/api)
- Review the [Marketplace Publishing Guide](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- Contact: ryan@stryve.com

## Release Checklist

- [ ] Update version in package.json
- [ ] Update CHANGELOG.md
- [ ] Test extension locally
- [ ] Build and package extension
- [ ] Publish to marketplace
- [ ] Update documentation
- [ ] Announce release
