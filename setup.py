#!/usr/bin/env python
"""
Package metadata for edx-ccx-keys.
"""
import os
import re

from setuptools import setup

def load_requirements(*requirements_paths):
    """
    Load all requirements from the specified requirements files.

    Returns:
        list: Requirements file relative path strings
    """
    requirements = set()
    for path in requirements_paths:
        with open(path) as reqs:
            requirements.update(
                line.split('#')[0].strip() for line in reqs
                if is_requirement(line.strip())
            )
    return list(requirements)


def is_requirement(line):
    """
    Return True if the requirement line is a package requirement.

    Returns:
        bool: True if the line is not blank, a comment, a URL, or an included file
    """
    return line and not line.startswith(('-r', '#', '-e', 'git+', '-c'))


def get_version(file_path):
    """
    Extract the version string from the file at the given relative path fragments.
    """
    filename = os.path.join(os.path.dirname(__file__), file_path)
    with open(filename, encoding='utf-8') as opened_file:
        version_file = opened_file.read()
        version_match = re.search(r"(?m)^__version__ = ['\"]([^'\"]+)['\"]", version_file)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


VERSION = get_version("ccx_keys/__init__.py")


setup(
    name='edx-ccx-keys',
    version=VERSION,
    author='edX',
    author_email='oscm@edx.org',
    description='Opaque key support custom courses on edX',
    long_description='Opaque key support custom courses on edX',
    long_description_content_type='text/x-rst',
    url='https://github.com/openedx/ccx-keys',
    license='AGPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
    packages=[
        'ccx_keys',
    ],
    install_requires=load_requirements('requirements/base.in'),
    entry_points={
        'context_key': [
            'ccx-v1 = ccx_keys.locator:CCXLocator',
        ],
        'usage_key': [
            'ccx-block-v1 = ccx_keys.locator:CCXBlockUsageLocator',
        ]
    }
)
