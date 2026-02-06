from typing import Dict


def run(request: Dict) -> Dict:
	"""Minimal implementation that validates keys and returns a sample response.

	This placeholder follows `skills/skill_generate_short_video.md` contract.
	"""
	# Basic validation
	if not isinstance(request, dict) or "request_id" not in request:
		return {"request_id": None, "status": "error", "error": "invalid_request"}

	return {
		"request_id": request.get("request_id"),
		"status": "ok",
		"object_path": "s3://bucket/generated_placeholder.mp4",
		"duration_s": request.get("target", {}).get("duration_s", 30),
		"thumbnail": "s3://bucket/thumb_placeholder.jpg",
		"quality_score": 0.5,
		"error": None,
	}

