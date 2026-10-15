# Repository instructions

This repository manages Lezi handoffs and UI assets. Game implementation lives in jieqi-engine.

- Read CURRENT_HANDOFF.json and the selected workline CURRENT_STATE before editing.
- Maintain stable worklines/ui and worklines/standard. Do not create another cumulative date-version handoff directory.
- Reuse immutable assets/ui content and existing Git blob SHAs. Do not duplicate font, background, preview, or prior snapshot bytes.
- Preserve approved artwork, exact scopes and source bodies. Candidate/approved/withdrawn are distinct. UI refinement uses frozen baselines and independent layers; one actual candidate at a time.
- Use GitHub connector reads and incremental writes. Verify the current HEAD; publish with expected_sha and no force. Reconcile concurrent changes instead of overwriting them.
- Keep historical recovery via archive/INDEX.json and immutable commits. Do not rewrite Git history or purge old objects without a separate explicit task.
- UI method and verification cadence are in worklines/ui/UI_WORK_AGREEMENT.md. Do not turn file checks into product/runtime acceptance.
- No game rule changes, scoring thaw, NET resume, APK, game merge, deployment, or automatic messages are authorized by a handoff/cleanup task.

- GitHub connector is the default two-way handoff channel for all four worklines. Update fixed workline files and a phase return record; do not ask the user to relay ordinary packages.
- Follow docs/WORKFLOW.md for RETURN_TO_MAIN.json and receiver-owned READ_RECEIPTS.json. Never fabricate another account's capabilities, reading, or adoption. Unpublished main/half_chaos sources remain unpublished until their actual content is committed.
- Receipts identify the immutable source commit and actual read/adopted scope. Keep history by ordinary commits; restore selected files rather than resetting the shared branch.
