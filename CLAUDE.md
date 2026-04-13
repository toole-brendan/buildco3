# BuildCo3

Federal defense procurement research project analyzing U.S. Navy and Coast Guard ship construction and maintenance spending.

## Project Structure

```
analysis/        Research docs, taxonomies, lessons learned, contract award analysis
output/          Deliverables: Excel financial models, key programs list, HTML briefing
scripts/         Python transformation scripts (mekko edits, FY27 columns, v1.22 updates)
data_pull/       FPDS Atom Feed extraction scripts, JSON output, aggregation
subaward_data/   USAspending subaward pulls by PIID, JSON output
sources/         Extracted text from Navy/CG budget books (PDFs excluded from git)
FY2027_numbers/  FY2027 budget document extracts
```

## Key Data Sources

- **FPDS Atom Feed** — contract modifications by PIID (`data_pull/fpds_per_mod_pull.py`)
- **USAspending API** — subaward data by prime contract (`subaward_data/fetch_subawards.py`)
- **SAM API** — requires `SAM_API_KEY` in `.env`

## Commands

- `python3 build/build_from_data.py` — rebuild market-sizing sheets from `build/data_v2.xlsx`. **Always ask the user before running this** — it creates a new versioned output file and archives the previous version.
- `./push_to_drive.sh` — dry run: preview what would push to Google Drive
- `./push_to_drive.sh --go` — push `output/` to `gdrive:buildco3`
- Edit `.rclone-filters` to change which folders get pushed

## Notes

- PDFs (~130MB) are gitignored; only extracted `.txt` versions are tracked
- `.env` contains `SAM_API_KEY` — never commit
- Excel models are versioned by filename (v1.20, v1.21, v1.22)
- Build script auto-archives the previous minor version to `output/archive/` when creating a new one
