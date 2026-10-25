# Evidence from deliberately broken variants

Use only when a regression check relies on an intentional defect. Ordinary tests
do not all need mutation testing. Work in an isolated task-owned copy or patch;
preserve the user's working tree and do not execute destructive variants against
shared data or services.

1. Identify the pristine candidate by commit plus relevant content identity for
   uncommitted files. Run the meaningful check against that baseline.
2. Apply one plausible wrong behavior. Inspect the actual diff against the pristine
   baseline and confirm the intended symbol/branch changed. A successful edit
   command, attempted replacement or changed filename is insufficient.
3. Run the same check. Confirm it fails because of the intended behavioral defect,
   not syntax, unavailable fixtures, timeouts, missing dependencies or another edit.
4. Restore the task-owned variant and verify the intended candidate still passes.
   Record the mutation, diff identity, command and decisive pass/fail evidence.

If the mutation did not land, correct the experiment; it supplies no sensitivity
evidence. If it landed but passed, investigate a coverage gap or equivalent
mutation. Do not change expected results merely to produce a red test.

Example: replace a bounded polling sleep with the full interval in an isolated
copy. A five-second timeout with a sixty-second interval should fail an elapsed-
time assertion. A compile failure does not demonstrate that deadline coverage works.
