from setuptools import setup

setup(
    name="ccx_keys",
    version="0.1",
    packages=[
        "ccx_keys",
    ],
    install_requires=[
        "opaque_keys",
    ],
    entry_points={
        'course_key': [
            'ccx-v1 = ccx_keys.locator.CCXLocator',
        ],
    }

)
