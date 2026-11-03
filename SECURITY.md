# Security

This policy covers Rust-in-One's instructions, installable files, and repository automation. Security issues in an application generated with the Skill belong with that application's maintainers as well.

## Report a sensitive issue

Use GitHub's **Report a vulnerability** option on this repository's Security page when it is available. If that option is absent, open an issue asking the maintainer for a private reporting channel, without including exploit details, credentials, or affected users' data. Do not post sensitive findings in a public issue or pull request.

Include the affected commit, client/version, a minimal reproduction, and the possible impact through the agreed private channel. There is no guaranteed response time or bug bounty. Fixes target the current `main`; historical snapshots are retained for reference, not maintained as separate release lines.

## Using the Skill

The installed package contains instructions and references, with no bundled executable code or hooks. The host agent can still execute commands while following those instructions. Review the revision you install, retain your host's normal permissions and isolation, and inspect generated software before relying on it. Validation and an independent review reduce some risks but do not certify security.
