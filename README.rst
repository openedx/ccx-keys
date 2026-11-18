ccx-keys |build-status|
=======================

**ccx-keys has been merged into opaque-keys.** The ``ccx_keys`` module, which provides the Opaque Key
implementations specific to Custom Courses for edX (CCX), is now developed in and distributed by
`the opaque-keys package`_ (``edx-opaque-keys>=5``). Please open issues and pull requests there.

As of version 3, ``edx-ccx-keys`` is an empty package whose only purpose is to depend on
``edx-opaque-keys>=5``. It installs no code.

Migrating
---------

Remove ``edx-ccx-keys`` from your requirements and depend on ``edx-opaque-keys>=5`` instead. Import
paths (``ccx_keys.key`` and ``ccx_keys.locator``) and the ``ccx-v1`` and ``ccx-block-v1`` key
namespaces are unchanged, so no code changes are needed.

Leaving ``edx-ccx-keys>=3`` in your requirements is harmless.

Both ``edx-ccx-keys<3`` and ``edx-opaque-keys>=5`` install the ``ccx_keys`` module. Uninstalling or
upgrading ``edx-ccx-keys<3`` in an existing environment therefore deletes the copy of ``ccx_keys``
that ``edx-opaque-keys`` provides. If you see ``ModuleNotFoundError: No module named 'ccx_keys'``
after upgrading, rebuild the environment or run::

    pip install --force-reinstall --no-deps edx-opaque-keys

.. |build-status| image:: https://github.com/openedx/ccx-keys/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/openedx/ccx-keys/actions/workflows/ci.yml

.. _`the opaque-keys package`: https://github.com/openedx/opaque-keys
