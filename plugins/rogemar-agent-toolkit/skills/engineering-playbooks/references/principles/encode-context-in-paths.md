# Context in file paths

A file's name can say what its code must obey, so a lint rule can enforce it
without anyone reading a comment. Examples: `*.hot.ts` for code that runs every
frame, where a rule bans allocation (object literals, closures, `new`);
`*.server.ts` for code that must never ship to the client, where a rule bans
importing it from client code; `*.pure.ts` for code that must not do I/O.

Use it when a constraint applies to a set of files, breaking it is costly or hard
to see in review, and the project's linter can match on paths. Name the
convention once in the project's instructions, add the rule in the same change,
and show it failing on a real violation. Do not invent a convention for a single
file or for a rule that needs judgment. Existing project naming wins.
