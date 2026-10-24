# Full-repository onboarding

Pin one revision, enumerate every tracked path (including dot-directories), then read every text file in bounded batches. Inspect assets by their appropriate modality; binary bytes are not prose. Use `python tools/ingestion_manifest.py` to inventory paths, hashes, sizes and line counts. It initializes `read_by_model:false`: hashing or downloading never marks files read.

For each complete text batch record path, line range, purpose and key constraint. If output truncates, reread missing ranges. Generated catalog pages and duplicate examples are still files: record them without repeatedly copying them into the final summary. Maintain an ingestion checkpoint before context compaction, with unread paths and a compact index of concepts/interfaces.

Do not promise all files remain verbatim in a finite context. Complete reading may span multiple turns; recover from receipts and retrieve original passages when needed. If the host cannot enumerate/fetch files, ask for a release upload. State unread files, inaccessible assets and any context limitation explicitly. Full ingestion is an onboarding request; ordinary tasks use selective retrieval afterward.
