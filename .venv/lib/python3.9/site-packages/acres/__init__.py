# Copyright The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
#
# This package was adapted from the fmriprep.data module released in 24.0.0,
# which evolved from an implementation in the Nibabies project,
# introduced in the following commit: https://github.com/nipreps/nibabies/commit/45a63a6
#
# Changes as of the fork (2024 July 15):
#   - This implementation uses a global ExitStack and resource cache,
#     to avoid `Loader` instances from containing self-references and
#     potentially leaking memory.
#
# Future modifications will be tracked in the change log.
"""Data loading utility for Python packages.

This module provides a class that wraps :mod:`importlib.resources` to
provide resource retrieval functions with commonly-needed scoping,
including interpreter-lifetime caching.
"""

from __future__ import annotations

import atexit
import sys
from contextlib import AbstractContextManager, ExitStack
from functools import cached_property
from pathlib import Path
from types import ModuleType

from functools import cache

if sys.version_info >= (3, 11):
    from importlib.resources import as_file, files
    from importlib.resources.abc import Traversable
else:
    from importlib_resources import as_file, files
    from importlib_resources.abc import Traversable

__all__ = ['Loader']


# Use one global exit stack
EXIT_STACK = ExitStack()
atexit.register(EXIT_STACK.close)


@cache
def _cache_resource(anchor: str | ModuleType, segments: tuple[str]) -> Path:
    # PY310(importlib_resources): no-any-return, PY311+(importlib.resources): unused-ignore
    return EXIT_STACK.enter_context(as_file(files(anchor).joinpath(*segments)))  # type: ignore[no-any-return,unused-ignore]


class Loader:
    """A loader for package files relative to a module

    This class wraps :mod:`importlib.resources` to provide a getter
    function with an interpreter-lifetime scope. For typical packages
    it simply passes through filesystem paths as :class:`~pathlib.Path`
    objects. For zipped distributions, it will unpack the files into
    a temporary directory that is cleaned up on interpreter exit.

    This loader accepts a fully-qualified module name or a module
    object.

    Expected usage::

        '''Data package

        .. autofunction:: load_data

        .. automethod:: load_data.readable

        .. automethod:: load_data.as_path

        .. automethod:: load_data.cached
        '''

        from acres import Loader

        load_data = Loader(__spec__.name)

    :class:`~Loader` objects implement the :func:`callable` interface
    and generate a docstring, and are intended to be treated and documented
    as functions.

    For greater flexibility and improved readability over the ``importlib.resources``
    interface, explicit methods are provided to access resources.

    +---------------+----------------+------------------+
    | On-filesystem | Lifetime       | Method           |
    +---------------+----------------+------------------+
    | `True`        | Interpreter    | :meth:`cached`   |
    +---------------+----------------+------------------+
    | `True`        | `with` context | :meth:`as_path`  |
    +---------------+----------------+------------------+
    | `False`       | n/a            | :meth:`readable` |
    +---------------+----------------+------------------+

    It is also possible to use ``Loader`` directly::

        from acres import Loader

        Loader(other_package).readable('data/resource.ext').read_text()

        with Loader(other_package).as_path('data') as pkgdata:
            # Call function that requires full Path implementation
            func(pkgdata)

        # contrast to

        from importlib_resources import files, as_file

        files(other_package).joinpath('data/resource.ext').read_text()

        with as_file(files(other_package) / 'data') as pkgdata:
            func(pkgdata)

    .. automethod:: readable

    .. automethod:: as_path

    .. automethod:: cached
    """

    def __init__(self, anchor: str | ModuleType):
        self._anchor = anchor
        self.files = files(anchor)
        # Allow class to have a different docstring from instances
        self.__doc__ = self._doc

    @cached_property
    def _doc(self) -> str:
        """Construct docstring for instances

        Lists the public top-level paths inside the location, where
        non-public means has a `.` or `_` prefix or is a 'tests'
        directory.
        """
        top_level = sorted(
            f'{p.name}/' if p.is_dir() else p.name
            for p in self.files.iterdir()
            if p.name[0] not in ('.', '_') and p.name != 'tests'
        )
        doclines = [
            f'Load package files relative to ``{self._anchor}``.',
            '',
            'This package contains the following (top-level) files/directories:',
            '',
            *(f'* ``{path}``' for path in top_level),
        ]

        return '\n'.join(doclines)

    def readable(self, *segments: str) -> Traversable:
        """Provide read access to a resource through a Path-like interface.

        This file may or may not exist on the filesystem, and may be
        efficiently used for read operations, including directory traversal.

        This result is not cached or copied to the filesystem in cases where
        that would be necessary.
        """
        # PY310(importlib_resources): no-any-return, PY311+(importlib.resources): unused-ignore
        return self.files.joinpath(*segments)  # type: ignore[no-any-return,unused-ignore]

    def as_path(self, *segments: str) -> AbstractContextManager[Path]:
        """Ensure data is available as a :class:`~pathlib.Path`.

        This method generates a context manager that yields a Path when
        entered.

        This result is not cached, and any temporary files that are created
        are deleted when the context is exited.
        """
        # PY310(importlib_resources): no-any-return, PY311+(importlib.resources): unused-ignore
        return as_file(self.files.joinpath(*segments))  # type: ignore[no-any-return,unused-ignore]

    def cached(self, *segments: str) -> Path:
        """Ensure data resource is available as a :class:`~pathlib.Path`.

        Any temporary files that are created remain available throughout
        the duration of the program, and are deleted when Python exits.

        Results are cached so that multiple calls do not unpack the same
        data multiple times, but directories and their contents being
        requested separately may result in some duplication.
        """
        # Use self._anchor and segments to ensure the cache does not depend on id(self.files)
        # PY310(importlib_resources): unused-ignore, PY311+(importlib.resources) arg-type
        return _cache_resource(self._anchor, segments)  # type: ignore[arg-type,unused-ignore]

    __call__ = cached
