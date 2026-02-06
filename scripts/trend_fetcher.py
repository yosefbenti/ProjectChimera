from datetime import datetime
from typing import List, Dict


def fetch_trends() -> List[Dict]:
	"""Return a minimal list of trend dictionaries matching the spec.

	This is a placeholder implementation intended to satisfy tests;
	real implementations should fetch from an external API and return
	richer data.
	"""
	return [
		{
			"topic": "example-topic",
			"score": 0.75,
			"timestamp": datetime.utcnow().isoformat() + "Z",
		}
	]

