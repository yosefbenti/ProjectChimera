# Skill: skill_generate_short_video

Purpose
-------
Generate a short social media video from a script, selected assets, and brand context.

Inputs (JSON)
```json
{
  "request_id": "uuid",
  "script": "string",
  "assets": [
    { "type": "image|clip|audio", "object_path": "s3://...", "start": 0, "end": 3 }
  ],
  "brand_context": {
    "tone": "upbeat",
    "logo_path": "s3://bucket/logo.png",
    "theme_color": "#FF6600"
  },
  "target": { "resolution": "720p", "duration_s": 30 }
}
```

Outputs (JSON)
```json
{
  "request_id": "uuid",
  "status": "ok|error",
  "object_path": "s3://bucket/generated_123.mp4",
  "duration_s": 30,
  "thumbnail": "s3://bucket/thumb.jpg",
  "quality_score": 0.81,
  "error": null
}
```

Notes
- The skill must validate asset compatibility (codec, framerate) and gracefully fall back to image-based video if clips are missing.
- Produce logs and a short storyboard (timestamps + asset map) for Judge review.

Errors
- `missing_assets`, `render_failed`, `unsupported_codec`.
