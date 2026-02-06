from typing import Dict


def run(request: Dict) -> Dict:
	"""Minimal YouTube downloader placeholder matching `skill_download_youtube.md`.
	"""
	if not isinstance(request, dict) or "request_id" not in request:
		return {"request_id": None, "status": "error", "error": "invalid_request"}

	return {
		"request_id": request.get("request_id"),
		"video_id": request.get("video_id"),
		"status": "ok",
		"object_path": "s3://bucket/placeholder.mp4",
		"metadata": {"duration_s": 30, "resolution": "720p", "size_bytes": 12345},
		"error": None,
	}

