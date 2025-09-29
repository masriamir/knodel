# Knodel Development Instructions

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Quick Reference Card

**Every PR Must Have:**

- ✅ Zero ruff errors (`uv run ruff check`)
- ✅ All tests passing (`uv run pytest`)
- ✅ Closing keywords (Closes #XX)
- ✅ All issue metadata copied
- ✅ Safety URLs preserved in `uv.lock`

**Never Do:**

- ❌ Change pkgs.safetycli.com URLs
- ❌ Use basic logging setup
- ❌ Manually fix formatting
- ❌ Commit without running tests

## 1. Project Overview

**knodel** Can transpile `Python` code to the appropriate `Haskell` code for running patterns in **Tidal Cycles**.

### Technology Stack

- **Python**: 3.13+ (specified in `.python-version`)
- **Package Management**: `uv` (modern, fast Python package management replacement for `pip`/`pipenv`)
- **Code Quality**: `ruff` (linting, and formatting)
- **Testing**: `pytest` for unit tests and integration tests

### Application Architecture

- **Main Library**: Located in `src/knodel/` package

### Repository Structure

#### Key Directories

- **src/knodel/**: Main library package
- **tests/**: Comprehensive test suite with performance, security, and functional tests

#### Important Files

- **pyproject.toml**: Project configuration and dependencies (uses `uv` for package management)
- **uv.lock**: Dependency lock file (always commit changes, URLs are prefixed with `pkgs.safetycli.com/` which is correct and should NOT be changed to `pypi.org` or `files.pythonhosted.org`)
- **pytest.ini**: Test configuration with markers and coverage settings

## 2. Development Setup

### Bootstrap and Dependencies

- **Install uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$HOME/.local/bin:$PATH"`
- **Install all dependencies**: `uv sync --all-groups` -- takes 3-4 minutes. NEVER CANCEL. Set timeout to 10+ minutes.
- **Verify installation**: `uv run python -c "import knodel; print('✅ Application imports successfully')"`

### Dependency Management with Safety Registry

- **Adding new dependencies**: When adding dependencies to `pyproject.toml`, always sync with the safety registry to preserve URLs
- **Correct sync command**: `uv sync --default-index https://pkgs.safetycli.com/repository/akm-circuits-llc/pypi/simple/ --all-groups`
- **CRITICAL**: The `uv.lock` file URLs must always use `pkgs.safetycli.com/` - never change them to `pypi.org` or `files.pythonhosted.org`
- **When uv.lock changes**: Only commit changes that add the specific new dependency and its direct dependencies - all other entries should preserve safety URLs
- **Verification**: After adding dependencies, confirm safety URLs with `grep "pkgs.safetycli.com" uv.lock | head -3`

## 3. Code Quality Standards

### Formatting Standards (MANDATORY)

**CRITICAL**: These formatting standards are enforced by CI and must be followed:

1. **Line Length**: Maximum 88 characters (`ruff` standard)
2. **Multi-line Formatting**: When breaking long lines:

   ```python
   # CORRECT - Parentheses on separate lines for multi-line
   assert (
       some_long_condition_here
   ), "Error message here"

   # INCORRECT - Don't put opening parenthesis on same line as closing
   assert (some_long_condition_here), "Error message"
   ```

3. **Import Organization**: Let `ruff` handle import sorting - never manually reorder
4. **String Quotes**: Use double quotes consistently (enforced by `ruff`)
5. **Trailing Commas**: Add trailing commas in multi-line structures

### Code Quality Tools

- **Linting (Fix)**: `uv run ruff check --fix .` -- automatically fixes all auto-fixable issues
- **Linting (Verify)**: `uv run ruff check .` -- must pass with zero errors
- **Formatting (Fix)**: `uv run ruff format .` -- fixes all formatting issues
- **Formatting (Verify)**: `uv run ruff format --check .` -- must pass with zero changes needed

### Common Mistakes to Avoid

1. **URL Modifications in uv.lock**
   - ❌ NEVER change `pkgs.safetycli.com` URLs to `pypi.org` or `files.pythonhosted.org`
   - ✅ Always preserve safety registry URLs when running `uv sync`

2. **Code Formatting**
   - ❌ Don't manually fix formatting issues
   - ✅ Always use `uv run ruff format --check .` and `uv run ruff format .`

## 4. Testing Framework

### Testing Overview and Execution

- **Run all tests**: `uv run pytest`
- **Run specific test categories**:
  - `uv run pytest -m unit` -- Unit tests only
  - `uv run pytest -m integration` -- Integration tests
  - `uv run pytest -m api` -- API endpoint tests
  - `uv run pytest -m smoke` -- Critical functionality tests

### Test Creation and Maintenance Guidelines

**MANDATORY**: All code changes must include proper test coverage with appropriate pytest markers. This section defines requirements and best practices for creating, maintaining, and categorizing tests.

#### Test Creation Requirements (MANDATORY)

**All new functionality MUST include tests:**

- **New functions/methods**: Unit tests with `@pytest.mark.unit` (mandatory)
- **New Flask endpoints**: API tests with `@pytest.mark.api` (mandatory)
- **New utilities/transformations**: Unit tests + integration tests for complex workflows
- **Security-related changes**: Security tests with `@pytest.mark.security`
- **Performance-critical code**: Performance tests with `@pytest.mark.load` or `@pytest.mark.concurrent`
- **Unit Tests**: Every new function/method must have dedicated unit tests
- **API Tests**: Every new Flask endpoint must have API tests
- **Integration Tests**: Multi-component features must have integration tests
- **Security Tests**: Authentication/authorization features must have security tests
- **Performance Tests**: Performance-critical code must have performance tests
- **Regression Tests**: Bug fixes must include tests preventing regression
- **Proper Markers**: All tests must use appropriate pytest markers for categorization

**Coverage Requirements:**

- **Minimum 80%** overall coverage (enforced by `pytest` configuration)
- **New code must maintain or improve** coverage percentage
- **All new functions must have dedicated unit tests**
- **All new endpoints must have dedicated API tests**

#### Test Creation Guidelines

**When to Create Tests:**

1. **Before implementation** (TDD approach encouraged) - Plan tests alongside feature design
2. **During implementation** - Create tests as you build functionality
3. **For bug fixes** - Create regression tests to prevent issue recurrence
4. **For refactoring** - Ensure existing behavior is preserved

**Pytest Marker Assignment (MANDATORY):**

- `@pytest.mark.unit` - Isolated unit tests for individual functions/methods (mandatory for all functions)
- `@pytest.mark.integration` - Cross-component tests (required for complex workflows spanning multiple modules)
- `@pytest.mark.api` - Flask endpoint tests
- `@pytest.mark.smoke` - Critical functionality tests (for core features affecting user experience)
- `@pytest.mark.slow` - Tests taking >5 seconds (property-based, large data processing)
- `@pytest.mark.security` - Security validation tests (authentication, input sanitization, vulnerability checks)
- `@pytest.mark.concurrent` - Concurrency/threading tests (for parallel processing features)
- `@pytest.mark.load` - Performance/load tests (for performance optimization work)

**Test Data Management:**

- **Use faker** for dynamic test data generation: `from faker import Faker`
- **Use pytest-datadir** for file-based test data: `@pytest.mark.datadir`
- **Edge cases**: Include tests for empty strings, special characters, unicode, large inputs

#### Test Maintenance Guidelines

**Updating Existing Tests:**

- **When modifying functionality**: Update corresponding tests to match new behavior
- **When fixing bugs**: Add regression tests before implementing the fix
- **When refactoring**: Ensure tests still validate the same behavior contracts
- **When adding features**: Extend existing test classes rather than creating duplicate tests

**Removing Tests:**

- **Remove tests only when** the associated functionality is completely removed
- **Update test markers** if test categorization changes (e.g., unit -> integration)
- **Consolidate redundant tests** to maintain test suite efficiency

**Performance Considerations:**

- **Keep test execution time reasonable** - mark slow tests with `@pytest.mark.slow`

### Coverage Verification and Quality Assurance

**Test Quality Assurance:**

- **Clear test names**: Use descriptive names that explain what is being tested
- **Comprehensive assertions**: Test both positive and negative cases
- **Test isolation**: Each test should be independent and not rely on other tests
- **Mock external dependencies**: Use `pytest-mock` for isolating units under test
- **Document complex tests**: Add docstrings explaining test rationale for complex scenarios

#### Integration with Development Workflow

**Before Starting Work:**

- **Review existing tests** related to the area you're modifying
- **Plan test requirements** alongside feature requirements in Acceptance Criteria
- **Identify test types needed**: Unit, integration, API, security, performance

**During Development:**

- **Create tests incrementally** as you implement functionality
- **Run relevant test subset** frequently: `uv run pytest -m unit` or `uv run pytest tests/test_specific_module.py`
- **Verify test markers** are applied correctly with `uv run pytest --collect-only`

**Before Committing:**

- **Run full test suite**: `uv run pytest`
- **Verify coverage**: Ensure coverage requirements are met
- **Check test categorization**: Confirm proper pytest markers are applied
- **Validate test quality**: Ensure tests have clear assertions and proper structure

## 5. Development Workflow

### Pre-Commit Workflow (MANDATORY)

**CRITICAL**: The following steps are **mandatory** for all pull request submissions. PRs that fail these requirements will be rejected.

#### Code Quality Requirements (MANDATORY)

1. **All linting issues MUST be fixed** (not just identified):
   - Run: `uv run ruff check --fix .` to automatically fix issues
   - Verify: `uv run ruff check .` must pass with zero errors
2. **All formatting issues MUST be fixed** (not just identified):
   - Run: `uv run ruff format .` to fix all formatting issues
   - Verify: `uv run ruff format --check .` must pass with zero changes needed
3. **Test Requirements MUST be met** (MANDATORY):
   - All new functionality must have corresponding tests with proper pytest markers
   - All tests must pass: `uv run pytest`
   - New functions must have unit tests with `@pytest.mark.unit`
   - New endpoints must have API tests with `@pytest.mark.api`
   - Complex workflows must have integration tests with `@pytest.mark.integration`
4. **Verification commands MUST pass** before PR submission
5. **Issue closing keywords MUST be included** in PR description (MANDATORY):
   - Use proper GitHub closing syntax: `Closes #123`, `Fixes #456`, `Resolves #789`
   - Reference all related issues that the PR addresses
   - Ensure issue numbers exist and are related to the PR content
6. **This is a mandatory requirement**, not a suggestion

#### Mandatory Workflow Steps

The required workflow is: **implement → test → fix → verify → close → commit**

- **Step 1**: Implement functionality with corresponding tests
- **Step 2**: Apply proper `pytest` markers and ensure coverage
- **Step 3**: Fix all linting and formatting issues using the fix commands
- **Step 4**: Verify all fixes and test requirements using the verification commands
- **Step 5**: Add proper issue closing keywords to PR description (Closes #123, Fixes #456, Resolves #789)
- **Step 6**: Only then proceed with commit and PR submission

**Note**: PRs with linting, formatting, or test coverage failures will be automatically rejected.

#### Acceptance Criteria Verification

- **When working on issues with Acceptance Criteria, ALWAYS verify each criterion before considering work complete**:
  1. **Review Original Issue**: Confirm you understand all Acceptance Criteria
  2. **Check Off Completed Items**: Mark each verified criterion as complete in the GitHub issue
  3. **Document Verification**: Add comments or evidence showing how each criterion was verified
  4. **Final Validation**: Ensure all criteria are checked off before submitting PR

#### Manual Testing Requirements

- **ALWAYS** test the application after making changes:
  1. Run `uv run python -c "import knodel; print('✅ Import test passed')"`

#### Pre-commit Validation Checklist

- [ ] Ran `uv run ruff check --fix .` to fix all formatting/linting issues
- [ ] Ran `uv run pytest` and all tests pass
- [ ] Updated tests for any new functionality
- [ ] Verified `uv.lock` URLs still use `pkgs.safetycli.com`
- [ ] Checked PR includes closing keywords
- [ ] Copied all metadata from related issues

## 6. Project Management

### Sprint Management and Issue Creation

When creating or managing issues for sprint planning:

#### Issue Creation Standards

- **Title Format**: "Action verb + description - context" (e.g., "Fix all ruff linting errors - code quality foundation")
- **Required Metadata**:
  - **Project**: Always assign to "Knodel" project
  - **Epic**: Categorize appropriately (Code Quality Foundation, Logging Infrastructure, Developer Productivity, etc.)
  - **Story Points**: Use Fibonacci sequence (1, 2, 3, 5, 8)
  - **Time Estimate**: Provide realistic hours estimate
  - **Risk Level**: Low/Medium/High
  - **Priority Labels**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low), P4 (Enhancement)
  - **Version Tags**: v1.0, v1.1, etc.
  - **Sprint Assignment**: Maximum 8 points per one-week sprint

#### Sprint Capacity

- **Sprint Duration**: 1 week
- **Max Capacity**: 8 story points per sprint
- **Velocity Tracking**: Monitor completed points vs planned

#### Dependencies

- **Always document blocking relationships** between issues
- **Use checkboxes** for prerequisites and blocked work
- **Update issue status** when dependencies are resolved

### GitHub Issue Management

When working on issues with Acceptance Criteria, follow this workflow to ensure comprehensive tracking and verification:

#### Before Starting Work

- **Review Acceptance Criteria**: Carefully read all Acceptance Criteria to understand requirements
- **Ask Questions**: If any criteria are unclear, ask for clarification in issue comments
- **Plan Implementation**: Break down work to address each Acceptance Criterion systematically
- **Estimate Effort**: Ensure your time estimate accounts for verifying all criteria

#### During Development

- **Reference Issue**: Include issue number in commit messages (e.g., `git commit -m "Fix transformation bug - addresses #123"`)
- **Update Progress**: Add comments to the issue about your progress and any implementation decisions
- **Check Off Completed Criteria**: As you complete each Acceptance Criterion, check it off in the issue:
  - Navigate to the issue on GitHub
  - Edit the issue description or add a comment
  - Check off completed items in the Acceptance Criteria checklist
- **Document Evidence**: For complex criteria, add comments with evidence of completion (test results, screenshots, etc.)
- **Test Each Criterion**: Create or run tests that specifically validate each Acceptance Criterion
- **Manual Verification**: Manually test functionality to ensure criteria are met in real usage

#### Before Submitting Pull Request

- **Final Verification**: Ensure all Acceptance Criteria are implemented and tested
- **Complete Checklist**: Verify all criteria are checked off in the issue
- **Cross-reference**: Ensure all acceptance criteria are addressed before considering work complete
- **Link to Issue**: Reference the issue in your pull request description
- **Evidence Summary**: Summarize how each major criterion was verified

#### Pull Request Review and Completion

- **Criteria Reference**: Reviewers should verify that all Acceptance Criteria are addressed
- **Testing Evidence**: Confirm that verification evidence is documented
- **Issue Closure**: Issues should only be closed when all criteria are completed and verified
- **Final Status Update**: Add a final comment summarizing completion and verification

This workflow ensures thorough requirement verification, maintains project quality, and provides clear tracking of development progress.

### Pull Request Management

When opening a pull request to address a specific issue, proper metadata inheritance ensures consistent project tracking and maintains sprint management accuracy for the Knodel project.

#### Metadata Inheritance Process

When creating a PR to address an issue, **all metadata from the originating issue must be copied to the PR**:

##### Step-by-Step Metadata Inheritance Instructions

1. **Copy Labels**: Inherit all labels from the originating issue
   - **Priority labels** (P0, P1, P2)
   - **Story point labels** (1, 2, 3, 5, 8, etc.)
   - **Version tags** (v1.0.0, etc.)
   - **Type labels** (bug, enhancement, documentation, etc.)
   - **Component labels** (frontend, backend, testing, etc.)

2. **Copy Milestones**: Assign the same milestone from the originating issue to maintain sprint tracking

3. **Copy Project Assignments**: Ensure the PR is assigned to the same project board(s) as the issue

4. **Copy Custom Field Values**: Inherit any custom field values from the project board:
   - Epic assignments
   - Sprint assignments
   - Risk level indicators
   - Time estimates
   - Any other custom fields used in project management

##### Metadata Inheritance Workflow

- **Before Creating PR**: Review the originating issue and note all metadata
- **During PR Creation**: Apply all relevant metadata from the issue to the PR
- **Verification**: Double-check that all metadata has been properly inherited
- **Documentation**: Reference the issue number in the PR description

This ensures continuous tracking from issue creation through PR completion and maintains accuracy in sprint management, story point tracking, and milestone progress for the Knodel project.

#### Closing Issues with Pull Requests (MANDATORY)

**All pull requests MUST use GitHub's closing keywords to automatically close their associated issues.** This ensures proper issue tracking and prevents issues from remaining open after work completion.

##### Required Closing Keywords

Use one of these GitHub closing keywords in your PR description or commit messages:

- `Closes #123` - Standard closing syntax
- `Fixes #456` - For bug fixes
- `Resolves #789` - For general issue resolution
- `Closes: #123` - Alternative syntax with colon

##### Examples for Single Issues

```markdown
# In PR description:
This PR adds the new text transformation feature.

Closes #45

# In commit message:
git commit -m "Add zalgo text transformation - Fixes #67"
```

##### Examples for Multiple Issues

```markdown
# In PR description:
This PR refactors the transformation engine and fixes several bugs.

Closes #23
Fixes #34
Resolves #45

# Alternative syntax:
Closes #23, #34, #45
```

##### Placement Requirements

- **PR Description**: Include closing keywords in the PR description (recommended)
- **Commit Messages**: Alternative placement in commit messages
- **Issue References**: Always reference specific issue numbers with `#` prefix
- **Verification**: Ensure the referenced issues exist and are related to the PR content

**Note**: This is a mandatory requirement for all PRs. PRs without proper issue closing keywords will be rejected during review.

#### Pull Request Standards

When creating pull requests:

1. **Title**: Clear, action-oriented description
2. **Description MUST include**:
   - Summary of changes
   - Testing performed (with specific commands)
   - Verification steps
   - Related issue references with closing keywords
3. **Metadata**: Copy ALL labels, milestones, and project assignments from related issues
4. **Closing Keywords**: ALWAYS use `Closes #XX`, `Fixes #XX`, or `Resolves #XX`

Example PR description:

```markdown
This PR implements centralized logging configuration for `app.py` and fixes `wsgi.py` log level handling.

## Changes
- Updated `app.py` to use centralized logging from `app.logging_config`
- Fixed `wsgi.py` to properly handle `LOG_LEVEL` environment variable
- Optimized log level processing to avoid redundant string operations

## Testing
- ✅ `uv run ruff check .` - passes cleanly
- ✅ `uv run ruff format --check .` - no formatting issues
- ✅ `uv run pytest` - all tests pass
- ✅ Manual testing with `FLASK_ENV=development uv run python app.py`

## Verification
- Confirmed logging outputs at correct levels
- Verified `LOG_LEVEL` environment variable is respected
- Tested both development and production configurations

Closes #11
```

## 7. Reference Materials

### Common Commands Reference

```bash
# Complete setup from fresh clone
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv sync --all-groups  # 3-4 minutes

# Mandatory pre-commit workflow (implement → test → fix → verify → commit)
# Step 1: Implement functionality with tests
# Step 2: Apply proper pytest markers and ensure coverage
uv run pytest  # Check coverage
uv run pytest --collect-only | grep "@pytest.mark"  # Verify markers

# Step 3: Fix all issues
uv run ruff check --fix .       # Fix linting issues
uv run ruff format .            # Fix formatting issues

# Step 4: Verify all issues are resolved
uv run ruff check .             # Must pass with zero errors
uv run ruff format --check .          # Must pass with zero changes needed

# Step 5: Run tests and commit (only after verification passes)
uv run pytest

# Test execution by category
uv run pytest -m unit  # Unit tests only
uv run pytest -m integration  # Integration tests
uv run pytest -m api  # API endpoint tests
uv run pytest -m smoke  # Critical functionality tests

# Verify safety URLs
grep -c "pkgs.safetycli.com" uv.lock

# Check formatting without fixing
uv run ruff format --check . && uv run ruff check .
```

### Performance Expectations and Timeouts

**Set appropriate timeouts for long-running operations:**

- `uv sync`: 3-4 minutes → Set timeout to 10+ minutes

**When running commands programmatically:**

```python
# Set appropriate timeout
result = subprocess.run(["uv", "sync"], timeout=600)  # 10 minutes
```

### Known Issues and Limitations

#### Test Suite Issues

- **Performance tests**: Require `concurrent` and `load` markers in pytest.ini (already added)

#### Timing Expectations

- **NEVER CANCEL** these operations:
  - `uv sync` -- 3-4 minutes
- **Fast operations** (<10 seconds):
  - Linting with ruff
  - Running tests
  - Application startup

### Maintaining These Instructions

#### Keeping Instructions Current

- **ALWAYS update** `.github/copilot-instructions.md` when implementing new features, tools, or changing development workflows
- **Cross-reference changes** with existing information in this file to ensure consistency
- **Add new commands** with validated timings and proper `uv run` prefixes
- **Document new dependencies** in the Technology Stack and Dependencies section
- **Update known issues** when fixing problems or discovering new ones
- **Include any new test categories** or build processes
- **Update test guidelines** when adding new pytest markers, test types, or coverage requirements
- **Maintain test command accuracy** when modifying test execution workflows or adding new test categories

#### Contributing Guidelines for Issues

When creating new issues, follow the structured format established in issues #7 and #8:

- **Use descriptive titles** following pattern: "Action description - brief context"
- **Include project metadata**: Epic, Story Points, Time Estimate, Risk Level
- **Provide clear description** and user story
- **Add technical analysis** section when relevant
- **Define acceptance criteria** as checkboxes
- **Document dependencies and blocking relationships**
- **Use appropriate labels**: P0/P1/P2 priority, story points (1-8), version tags
- **Assign to appropriate milestone** with sprint context

For detailed workflow on working with issues that have Acceptance Criteria, see the **GitHub Issue Management** section under "Project Management".
