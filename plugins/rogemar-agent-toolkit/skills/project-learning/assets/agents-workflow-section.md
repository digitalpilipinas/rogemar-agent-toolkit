<!-- BEGIN PROJECT LEARNING -->
## Project learning

- Consult relevant accepted entries in `docs/project-learning/lessons.md`; current instructions, contracts, tests and verified evidence take precedence. Pending candidates are never guidance.
- This project explicitly enrolls workflow capture. At verified task/sprint completion, assess at most one durable lesson per source turn using the installed `project-learning` skill. Capture only verified or reinforced evidence; otherwise omit the candidate.
- Use the existing candidate store with `capture --workflow --permission-mode execution --request -`. Keep capture nonblocking, deduplicate settled lessons, and remind only when `review_due` is true. Do not run a dedicated learning task or install hooks automatically.
- Plan Mode, no-write, no-learning and disabled tasks persist nothing, including request files. Pass the appropriate guards; never promote or activate lessons without user approval.
- Keep summaries local and structured; never persist transcripts, hidden reasoning, tool output, secrets, credentials, personal data or conversation quotations.
- Capture cannot edit product code, delivery status, accepted lessons, shared skills, global instructions or Codex memory. Global proposals require accepted source evidence and a recorded target scope; publication and edits remain separately authorized.
<!-- END PROJECT LEARNING -->
