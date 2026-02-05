# Skill: skill_transcribe_audio

Purpose
-------
Transcribe audio from an audio file or video asset to a timestamped text transcript.

Inputs (JSON)
```json
{
  "request_id": "uuid",
  "object_path": "s3://bucket/key.mp4",
  "language": "en",
  "model": "whisper-small",
  "timestamps": true
}
```

Outputs (JSON)
```json
{
  "request_id": "uuid",
  "status": "ok|error",
  "transcript": "Full text...",
  "segments": [
    { "start": 0.0, "end": 2.3, "text": "Hello" }
  ],
  "confidence": 0.92,
  "error": null
}
```

Notes
- Provide language detection fallback if `language` is null.
- Persist transcripts to a text store and reference via metadata in `video_asset`.

Errors
- `unsupported_format`, `transcription_failed`, `quota_exceeded`.
