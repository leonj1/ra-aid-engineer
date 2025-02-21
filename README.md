# Webhook Application

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