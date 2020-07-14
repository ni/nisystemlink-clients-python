# -*- coding: utf-8 -*-

"""Sphinx extension to clean up autodoc output."""

import inspect
import re

import docutils.nodes as nodes


def _skip_member(app, what, name, obj, skip, options):
    # When ":meta private:" or ":meta public:" is explicitly included in the docstr,
    # obey it, regardless of what autodoc otherwise wants to do.
    doc = getattr(obj, "__doc__", None) or ""
    if ":meta private:" in doc:
        return True
    elif ":meta public:" in doc:
        return False

    # Don't include the docstring inherited from object.__init__ (for classes that have
    # no __init__ method).
    if obj is object.__init__:
        return True

    # Don't inherit a docstring for __init__ methods that have no docstring of their
    # own.
    if name == "__init__" and not obj.__doc__:
        return True

    # Don't include __init__ in the docs if the class is abstract.
    if name == "__init__":
        mod = inspect.getmodule(obj)
        class_name = obj.__qualname__.rsplit(".", 1)[0]
        if mod is not None:
            klass = getattr(mod, class_name)
            if inspect.isabstract(klass):
                return True


def _process_docstring(app, what, name, obj, options, lines):
    for i, line in enumerate(lines):
        # Modify the import path of public modules to appear as members of the package,
        # rather than the _module, as they're documented as being members of the
        # package. This makes intra-project links work, given the way we import classes
        # into the containing package.
        line = modify_systemlink_paths(line)

        # Sphinx errors if it tries to reference a TypeVar variable.
        # (https://github.com/agronholm/sphinx-autodoc-typehints/issues/39)
        # So for now we'll need to handle them ourselves.
        line = line.replace("\\[\\~_Any]", "")
        line = re.sub(r"\b_Any\b", "typing.Any", line)

        # Don't abbreviate external classes (via "~"), except typing.* classes.
        line = re.sub(r"~(?!typing\.|systemlink\.)(?=[a-z]\w*\.)", "", line)

        lines[i] = line


def modify_systemlink_paths(s: str) -> str:
    """Modify systemlink.* paths in the given string to hide implementation modules.

    Examples:
        >>> # Basic usage
        >>> modify_systemlink_paths("systemlink.foo._abc.Abc")
        'systemlink.foo.Abc'

        >>> # Modify all paths in the string
        >>> modify_systemlink_paths(" systemlink.f._abc.Abc systemlink.f._xyz.Xyz ")
        ' systemlink.f.Abc systemlink.f.Xyz '

        >>> # Don't change _internal or _core paths
        >>> modify_systemlink_paths("systemlink.foo._internal._abc.Abc")
        'systemlink.foo._internal._abc.Abc'
        >>> modify_systemlink_paths("systemlink.foo._core._abc.Abc")
        'systemlink.foo._core._abc.Abc'
    """
    return re.sub(r"(?<!\._internal)(?<!\._core)\._(?!internal|core)\w+.", ".", s)


def _missing_reference(app, env, node, contnode):
    target = node["reftarget"]
    if target.startswith("systemlink."):
        # For types that are parameters of overloaded functions, the process-docstring
        # code above will not have seen them; so do the appropriate string replacements
        # here, too.
        refid = modify_systemlink_paths(target)
        if refid == target:
            # If the rename didn't change the string, there must be some other issue.
            # Let the calling code raise a warning/error.
            return None

        # Use just the class name (as if the "~" prefix were applied).
        name = target.rsplit(".", 1)[1]

        return nodes.reference(contnode.rawsource, name, refid=refid)


def setup(app):
    """Entry point for Sphinx extensions."""
    app.connect("autodoc-skip-member", _skip_member)
    app.connect("autodoc-process-docstring", _process_docstring)
    app.connect("missing-reference", _missing_reference, priority=1000)
