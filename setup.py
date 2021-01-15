#!/usr/bin/env python
"""
Package metadata for edx-ccx-keys.
"""

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

setup(
    name='edx-ccx-keys',
    version='1.2.0',
    author='edX',
    author_email='oscm@edx.org',
    description='Opaque key support custom courses on edX',
    url='https://github.com/edx/ccx-keys',
    license='AGPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
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
