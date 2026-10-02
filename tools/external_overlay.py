"""Third-party locations and strict filesystem access for overlay gates."""

import stat


class InputError(Exception):
    """An in-scope path could not be audited."""

    def __init__(self, path, error):
        self.path = path
        super().__init__(str(error))


def path_stat(path, *, missing_ok=False):
    try:
        return path.stat()
    except FileNotFoundError as exc:
        if missing_ok:
            try:
                path.lstat()
            except FileNotFoundError:
                return None
            except OSError as error:
                raise InputError(path, error) from error
        raise InputError(path, exc) from exc
    except OSError as exc:
        raise InputError(path, exc) from exc


def directory_entries(path):
    # Materialize inside the try: iteration itself can fail partway through.
    try:
        return sorted(path.iterdir())
    except OSError as exc:
        raise InputError(path, exc) from exc


def read_utf8(path):
    try:
        if not stat.S_ISREG(path_stat(path).st_mode):
            raise OSError("Expected a regular file")
        return path.read_bytes().decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(path, exc) from exc


def walk_files(root, *, exclude=lambda path: False, ancestors=frozenset()):
    """Walk explicitly: pathlib globbing can suppress access errors."""
    info = path_stat(root)
    identity = (info.st_dev, info.st_ino)
    if identity in ancestors:
        raise InputError(root, "Directory cycle prevents a complete audit")
    for path in directory_entries(root):
        if exclude(path):
            continue
        info = path_stat(path)
        if stat.S_ISDIR(info.st_mode):
            yield from walk_files(path, exclude=exclude,
                                  ancestors=ancestors | {identity})
        else:
            yield path


ADDYOSMANI_SKILLS = (
    "addyosmani-ci-cd-and-automation",
    "addyosmani-code-review-and-quality",
    "addyosmani-context-engineering",
    "addyosmani-security-and-hardening",
    "addyosmani-using-agent-skills",
)

# These retain Markdown content after leaving Claude rule discovery. Content
# gates must keep scanning them even though their discovery suffix is now .txt.
RULE_PROVENANCE_PATHS = (
    ".claude/rules/external/kariedo/PROVENANCE.txt",
    ".claude/rules/external/tikitribe/PROVENANCE.txt",
)
