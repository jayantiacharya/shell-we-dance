#!/bin/bash
# setup-hooks.sh — Install git hooks for this repository
#
# Run once after cloning:
#   bash scripts/setup-hooks.sh
#
# What this installs:
#   commit-msg  — enforces the Conventional Commits format

set -euo pipefail

HOOKS_DIR="$(git rev-parse --git-dir)/hooks"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# commit-msg hook — enforces Conventional Commits format
# ---------------------------------------------------------------------------
COMMIT_MSG_HOOK="$HOOKS_DIR/commit-msg"

cat > "$COMMIT_MSG_HOOK" << 'HOOK'
#!/bin/bash
# commit-msg hook: enforce Conventional Commits format
#
# Allowed types: feat fix docs test chore refactor style perf ci build
# Format: <type>(<optional scope>): <description>
# Examples:
#   feat(parser): add JSON log detection
#   fix: handle missing config file gracefully
#   docs(readme): update setup instructions
#   test(monitor): add edge case for empty directory

commit_msg=$(cat "$1")

# Allow merge commits and revert commits through without validation
if echo "$commit_msg" | grep -qE "^(Merge|Revert) "; then
    exit 0
fi

pattern="^(feat|fix|docs|test|chore|refactor|style|perf|ci|build)(\(.+\))?: .{1,100}$"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo ""
    echo "  ✗ Commit message does not follow Conventional Commits format."
    echo ""
    echo "  Required format:  <type>(<scope>): <description>"
    echo "  Example:          feat(parser): add JSON log detection"
    echo ""
    echo "  Allowed types: feat  fix  docs  test  chore  refactor  style  perf  ci  build"
    echo ""
    echo "  Your message: $commit_msg"
    echo ""
    exit 1
fi

exit 0
HOOK

chmod +x "$COMMIT_MSG_HOOK"
echo "✓ Installed commit-msg hook at $COMMIT_MSG_HOOK"

# ---------------------------------------------------------------------------
# Done
# ---------------------------------------------------------------------------
echo ""
echo "Git hooks installed successfully."
echo "Your commits will now be validated against the Conventional Commits format."
echo ""
echo "Test it:"
echo "  git commit --allow-empty -m 'feat(test): verify hook works'   # should pass"
echo "  git commit --allow-empty -m 'did some stuff'                  # should fail"
