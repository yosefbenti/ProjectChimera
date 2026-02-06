from typing import Dict


def run(request: Dict) -> Dict:
	"""Minimal transcription placeholder matching `skill_transcribe_audio.md`.
	"""
	if not isinstance(request, dict) or "request_id" not in request:
		return {"request_id": None, "status": "error", "error": "invalid_request"}

	return {
		"request_id": request.get("request_id"),
		"status": "ok",
		"transcript": "(placeholder transcript)",
		"segments": [{"start": 0.0, "end": 1.0, "text": "Hello"}],
		"confidence": 0.9,
		"error": None,
	}

