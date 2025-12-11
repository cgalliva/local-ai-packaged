# N8N Workflows & Credentials Backup

This folder contains n8n workflows and credentials that are **automatically imported** when n8n starts for the first time.

## Structure

```
/n8n/backup/
  /workflows/          → n8n workflow JSON files
  /credentials/        → n8n credentials JSON files (optional)
```

## How It Works

### 🔄 One-Way Import (Automatic)
When you run `python start_services.py`, the `n8n-import` service automatically imports:
- All workflows from `/workflows/` folder
- All credentials from `/credentials/` folder (if any)

This happens **once** before the main n8n container starts.

### ⚠️ No Auto-Sync Back
**Important**: Editing workflows in the n8n UI does NOT automatically update these files!

### 📥 Automated Export (Recommended!)

Use the sync script to export all workflows back to this folder:

```bash
# From the project root
python sync_n8n_workflows.py
```

This will automatically:
- Export all workflows from n8n to `/workflows/`
- List all exported files
- Preserve your work in version control

**For credentials:**
```bash
python sync_n8n_workflows.py --with-credentials
```
⚠️ Be careful not to commit sensitive credentials to git!

### 📥 Manual Export (Alternative)

If you prefer manual control:

To save your work back to this repo after editing in n8n:

**For Workflows:**
1. Open workflow in n8n UI
2. Click "..." (three dots menu)
3. Click "Download"
4. Save to: `/n8n/backup/workflows/Your_Workflow_Name.json`

**For Credentials:**
1. In n8n, go to Credentials page
2. Click "..." on a credential
3. Export and save to: `/n8n/backup/credentials/`

### 💡 Best Practice Workflow

1. **Build** your workflow in n8n UI (http://localhost:5678)
2. **Test** it thoroughly
3. **Sync** back to repo: `python sync_n8n_workflows.py`
4. **Review** changes: `git diff n8n/backup/`
5. **Commit** to git: `git add n8n/backup/ && git commit -m "Update workflows"`
6. **Repeat** whenever you make significant changes

## Current Files

- `Reference_Local_Agentic_RAG.json` - Example RAG workflow for reference (read-only)
- Your new demo workflows will go here!

## Tips

- Use descriptive names: `SC_AI_Demo_Main_Flow.json`
- Export after each major milestone
- Keep credentials separate (don't commit sensitive data to git)
- Consider adding `.gitignore` for `/credentials/*.json` if they contain secrets

