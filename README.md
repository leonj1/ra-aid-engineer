![Webhook Application](image.jpg)

# Git Project Assistant

A FastAPI application that listens to GitHub and GitLab webhook events and provides automated assistance for project management and code review.

## Purpose

This project serves as an automated assistant for git-based projects by:

1. **Monitoring Project Changes**
   - Listens to Pull Request and Merge Request events
   - Processes issue creation and updates
   - Tracks comments and discussions

2. **Automated Code Review**
   - Analyzes proposed code changes using AI
   - Provides detailed feedback on:
     - Code quality and best practices
     - Potential bugs and security issues
     - Performance implications
     - Suggested improvements

3. **Issue Resolution**
   - Processes incoming issues
   - Suggests solutions based on codebase analysis
   - Links related issues and pull requests
   - Provides automated responses with helpful context

4. **Project Management**
   - Tracks project activity through webhooks
   - Maintains context across related changes
   - Helps prioritize and categorize issues
   - Facilitates code review workflow

## Features

- GitHub and GitLab webhook integration
- AI-powered code review
- Automated issue triage
- Contextual response generation
- Semantic versioning automation

## Semantic Versioning

This project uses semantic versioning through GitHub Actions. Version numbers are automatically incremented based on conventional commit messages.

### Version Format
`vMAJOR.MINOR.PATCH`

### Commit Message Format
The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Where `type` determines how the version is incremented:

- `BREAKING CHANGE:` or commits with `!` - Increment **MAJOR** version
  - Example: `feat!: remove deprecated API endpoints`
  - Example: `BREAKING CHANGE: change authentication flow`

- `feat:` - Increment **MINOR** version
  - Example: `feat: add new webhook endpoint`
  - Example: `feat(auth): implement JWT authentication`

- `fix:`, `docs:`, `style:`, `refactor:` - Increment **PATCH** version
  - Example: `fix: handle null payload in webhook`
  - Example: `docs: update API documentation`

### Automatic Versioning
The GitHub Action will:
1. Trigger on pushes to master/main or merged PRs
2. Analyze commit messages since last tag
3. Determine version increment based on conventional commits
4. Create and push new tag
5. Generate release notes

### Development Workflow
1. Use conventional commit messages
2. Push changes or merge PR to master/main
3. GitHub Action automatically:
   - Creates new version tag
   - Generates release
   - Updates documentation

### Example Version Increments
- Current: `v1.2.3`
- After `feat: new feature` → `v1.3.0`
- After `fix: bug fix` → `v1.2.4`
- After `feat!: breaking change` → `v2.0.0`

## Getting Started

1. Install dependencies:
```bash
make setup
```

2. Configure webhook endpoints in your git repositories:
   - GitHub: `http://your-domain/webhook/github`
   - GitLab: `http://your-domain/webhook/gitlab`

3. Set environment variables:
```bash
ANTHROPIC_API_KEY=your-api-key
```

4. Run the application:
```bash
cd app && uvicorn main:app --reload
```

## Development

- Run tests: `make test`
- Clean up: `make clean`
- View commands: `make help`

The pre-push hook ensures all tests pass before pushing changes.