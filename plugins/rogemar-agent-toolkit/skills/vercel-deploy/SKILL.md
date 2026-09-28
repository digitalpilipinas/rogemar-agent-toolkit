---
name: vercel-deploy
description: Deploy applications and websites to Vercel using the bundled `scripts/deploy.sh` claimable-preview flow. Use when the user asks to deploy to Vercel, wants a preview URL, or says to push a project live on Vercel.
---

# Vercel Deploy

This entry describes a claimable-preview workflow. Inspect the actual upload endpoint, bundled script, account/claim behavior, permitted source and publication scope before using it; the absence of a login step is not a privacy or trust guarantee.

## Prerequisites

- A network or sandbox failure does not authorize escalation or a repeated deployment. Reconcile the outcome first, preserve declined access, and use only supported native permission controls within the exact deployment authority.
- The deployment might take a few minutes. Use appropriate timeout values.

## How It Works

1. Packages your project into a `.tar.gz` (excludes `node_modules` and `.git`)
2. Auto-detects framework from `package.json`
3. Uploads to deployment service
4. Returns **Preview URL** (live site) and **Claim URL** (transfer to your Vercel account)

## Usage

```bash
bash scripts/deploy.sh [path]
```

**Arguments:**

- `path` - Directory to deploy, or a `.tgz` file (defaults to current directory)

If you pass a directory, the script will create a `.tar.gz` before upload.

**Examples:**

```bash
# Deploy current directory
bash scripts/deploy.sh

# Deploy specific project
bash scripts/deploy.sh /path/to/project

# Deploy existing tarball
bash scripts/deploy.sh /path/to/project.tgz
```

## Packaging Rules

- Exclude `node_modules`, `.git`, and `.env*`
- If no `package.json`, keep `framework` as `null`
- For static HTML with a single `.html` file, rename it to `index.html` before packaging

## Output

```
Preparing deployment...
Creating deployment package...
Deploying...
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

The script also outputs JSON to stdout for programmatic use.

```json
{
  "previewUrl": "https://skill-deploy-abc123.vercel.app",
  "claimUrl": "https://vercel.com/claim-deployment?code=...",
  "deploymentId": "dpl_...",
  "projectId": "prj_..."
}
```

## Framework Detection

The script auto-detects frameworks from `package.json`. Supported frameworks include:

- **React**: Next.js, Gatsby, Create React App, Remix, React Router
- **Vue**: Nuxt, Vitepress, Vuepress, Gridsome
- **Svelte**: SvelteKit, Svelte, Sapper
- **Other Frontend**: Astro, Solid Start, Angular, Ember, Preact, Docusaurus
- **Backend**: Express, Hono, Fastify, NestJS, Elysia, h3, Nitro
- **Build Tools**: Vite, Parcel
- **And more**: Blitz, Hydrogen, RedwoodJS, Storybook, Sanity, etc.

For static HTML projects (no `package.json`), framework is set to `null`.

## Static HTML Projects

For projects without a `package.json`:

- If there's a single `.html` file not named `index.html`, it gets renamed automatically
- This ensures the page is served at the root URL (`/`)

## Present Results to User

Return the preview URL only after verifying the actual result. Treat a claim URL as a potentially sensitive transfer capability: disclose it only to the authorized owner in the intended channel, not public logs. The following is an example format, not execution evidence:

```
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...

View your site at the Preview URL.
To transfer this deployment to your Vercel account, visit the Claim URL.
```

## Troubleshooting

### Escalated Network Access

For a timeout or reset, inspect authorized provider status and reconcile any uncertain remote outcome before retrying. Do not transplant Codex-only permission arguments into another harness or retry declined access. Use only the active host permission flow when additional authority is genuinely required; preserve already granted scope.

Example guidance to the user:

```
The deploy needs escalated network access to deploy to Vercel. I can rerun the command with escalated permissions—want me to proceed?
```
