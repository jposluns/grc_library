"""Strict file-system access helpers shared by the corpus-management gates.

Every helper fails closed: an in-scope path that cannot be stat'ed, listed,
decoded or walked raises :class:`InputError` naming the path, so a gate
reports it instead of skipping it. Directory walks are explicit because
pathlib globbing can suppress access errors.

A symlink whose target resolves outside the scanned root is refused, not
followed, and a file larger than ``MAX_READ_BYTES`` is refused, not read.

Standard library only; no project or overlay configuration lives here.
"""

import stat

# The default read limit of read_utf8. When it was set, the largest file
# gate 82 scanned was under 1 MiB.
MAX_READ_BYTES = 16 * 1024 * 1024


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


def require_inside(path, root):
    """Refuse a path whose real location is outside the real location of root."""
    try:
        real = path.resolve(strict=True)
        real_root = root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise InputError(path, exc) from exc
    if not real.is_relative_to(real_root):
        raise InputError(path, f"Resolves to {real}, outside the scanned root {real_root}")


def read_utf8(path, *, root=None, max_bytes=MAX_READ_BYTES):
    """Read a regular file as strict UTF-8.

    When root is given, a path that resolves outside root is refused. A file
    larger than max_bytes is refused, checked by its size before the read and
    by the bytes read after it. The read stops 1 byte past max_bytes, so a
    file that grows after the size check is never read whole.
    """
    if root is not None:
        require_inside(path, root)
    try:
        info = path_stat(path)
        if not stat.S_ISREG(info.st_mode):
            raise OSError("Expected a regular file")
        if info.st_size > max_bytes:
            raise OSError(f"Larger than the {max_bytes}-byte read limit")
        with path.open("rb") as handle:
            data = handle.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise OSError(f"Larger than the {max_bytes}-byte read limit")
        return data.decode("utf-8", errors="strict")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(path, exc) from exc


def walk_files(root, *, exclude=lambda path: False, ancestors=frozenset(), top=None):
    """Walk explicitly: pathlib globbing can suppress access errors.

    A symlink to a file or a folder whose target resolves outside the first
    root walked (top) is refused.
    """
    if top is None:
        top = root
    info = path_stat(root)
    identity = (info.st_dev, info.st_ino)
    if identity in ancestors:
        raise InputError(root, "Directory cycle prevents a complete audit")
    for path in directory_entries(root):
        if exclude(path):
            continue
        try:
            link = stat.S_ISLNK(path.lstat().st_mode)
        except OSError as exc:
            raise InputError(path, exc) from exc
        if link:
            require_inside(path, top)
        info = path_stat(path)
        if stat.S_ISDIR(info.st_mode):
            yield from walk_files(path, exclude=exclude,
                                  ancestors=ancestors | {identity}, top=top)
        else:
            yield path
