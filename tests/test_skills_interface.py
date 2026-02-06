import importlib


def test_skills_modules_provide_expected_entrypoint():
    """Assert that each documented skill exposes a callable entrypoint.

    Based on `skills/*.md`, each skill SHOULD provide a top-level
    `run(request: dict) -> dict` or `handle(request: dict) -> dict`.

    This test intentionally expects modules that do not yet exist and
    therefore SHOULD fail until the skill modules are implemented.
    """
    skill_names = [
        "skill_generate_short_video",
        "skill_transcribe_audio",
        "skill_download_youtube",
    ]

    for name in skill_names:
        module_path = f"skills.{name}"
        module = importlib.import_module(module_path)

        # Accept any of the common entrypoint names
        assert any(hasattr(module, fn) for fn in ("run", "handle", "execute")), (
            f"{module_path} must expose `run`/`handle`/`execute` entrypoint"
        )

        # If an entrypoint exists, it should be callable
        for fn in ("run", "handle", "execute"):
            if hasattr(module, fn):
                assert callable(getattr(module, fn))

