# Skill: skill_download_youtube

Purpose
-------
Fetch video metadata and obtain a downloadable asset URI (or record the original platform URI) for downstream processing.

Inputs (JSON)
```json
{
  "request_id": "uuid",
  "platform": "youtube",
  "video_id": "string",
  "preferred_formats": ["mp4_720", "mp4_480"],
  "download": true
}
```

Outputs (JSON)
```json
{
  "request_id": "uuid",
  "video_id": "string",
  "status": "ok|error|not_found",
  "object_path": "s3://bucket/key.mp4", 
  "metadata": {
    "duration_s": 30,
    "resolution": "720p",
    "size_bytes": 12345678
  },
  "error": null
}
```

Notes
- If `download` is false, skill returns canonical platform URI and metadata without creating an S3 object.
- Respect platform TOS; include rate-limiting and caching. Use a temporary working directory and clean artifacts on completion.

Errors
- `not_found` when video_id invalid; `rate_limited` for throttling; `forbidden` when access restricted.
