from setuptools import setup

setup(
    name="ccx_keys",
    version="0.1.1",
    packages=[
        "ccx_keys",
    ],
    install_requires=[
        "edx-opaque-keys>=0.2.1,<1.0.0",
    ],
    entry_points={
        'course_key': [
            'ccx-v1 = ccx_keys.locator:CCXLocator',
        ],
        'usage_key': [
            'ccx-block-v1 = ccx_keys.locator:CCXBlockUsageLocator',
        ]
    }
)
