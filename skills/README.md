# Skills Directory — Project Chimera

This folder contains formal specifications for the runtime "Skills" that Chimera agents will expose and consume. A Skill is a focused capability package with a clearly defined Input/Output contract and minimal operational notes.

Structure
- `skills/skill_<name>.md` — one file per skill describing purpose, inputs, outputs, and basic error handling.

Core skills included (drafts):
- `skill_download_youtube.md` — download or fetch video metadata and asset URIs.
- `skill_transcribe_audio.md` — convert audio/video to text transcripts.
- `skill_generate_short_video.md` — assemble short social video from script + assets.

Usage
- Agents will call skills via local function calls or HTTP endpoints depending on deployment model. Each skill must be idempotent and produce machine-readable logs for traceability.
