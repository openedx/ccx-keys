# -*- coding: utf-8 -*-
import re

from opaque_keys import InvalidKeyError
from opaque_keys.edx.locator import CourseLocator, BlockUsageLocator
from opaque_keys.edx.keys import UsageKey

from ccx_keys.key import CCXKey


class CCXLocator(CourseLocator, CCXKey):
    """Concrete implementation of an Opaque Key for CCX courses"""

    CANONICAL_NAMESPACE = 'ccx-v1'
    KEY_FIELDS = CourseLocator.KEY_FIELDS + ('ccx', )
    __slots__ = KEY_FIELDS
    CHECKED_INIT = False
    CCX_PREFIX = 'ccx'

    # pep8 and pylint don't agree on the indentation in this block; let's make
    # pep8 happy and ignore pylint as that's easier to do.
    # pylint: disable=bad-continuation
    URL_RE_SOURCE = r"""
        ((?P<org>{ALLOWED_ID_CHARS}+)\+(?P<course>{ALLOWED_ID_CHARS}+)(\+(?P<run>{ALLOWED_ID_CHARS}+))?{SEP})??
        ({BRANCH_PREFIX}@(?P<branch>{ALLOWED_ID_CHARS}+){SEP})?
        ({VERSION_PREFIX}@(?P<version_guid>[A-F0-9]+){SEP})?
        ({CCX_PREFIX}@(?P<ccx>\d+){SEP})
        ({BLOCK_TYPE_PREFIX}@(?P<block_type>{ALLOWED_ID_CHARS}+){SEP})?
        ({BLOCK_PREFIX}@(?P<block_id>{ALLOWED_ID_CHARS}+))?
        """.format(
        ALLOWED_ID_CHARS=CourseLocator.ALLOWED_ID_CHARS,
        BRANCH_PREFIX=CourseLocator.BRANCH_PREFIX,
        VERSION_PREFIX=CourseLocator.VERSION_PREFIX,
        BLOCK_TYPE_PREFIX=CourseLocator.BLOCK_TYPE_PREFIX,
        BLOCK_PREFIX=CourseLocator.BLOCK_PREFIX,
        CCX_PREFIX=CCX_PREFIX,
        SEP=r'(\+(?=.)|$)',  # Separator: requires a non-trailing '+' or end of string
    )

    URL_RE = re.compile(
        '^' + URL_RE_SOURCE + '$', re.IGNORECASE | re.VERBOSE | re.UNICODE
    )

    def __init__(
        self,
        org=None,
        course=None,
        run=None,
        branch=None,
        version_guid=None,
        deprecated=False,
        **kwargs
    ):
        """constructor for a ccx locator"""
        # for a ccx locator we require a ccx id to be passed.
        if 'ccx' not in kwargs:
            raise InvalidKeyError(self.__class__, "ccx must be set")

        super(CCXLocator, self).__init__(
            org=org,
            course=course,
            run=run,
            branch=branch,
            version_guid=version_guid,
            deprecated=deprecated,
            **kwargs
        )

    @classmethod
    def from_course_locator(cls, course_locator, ccx):
        """Construct a CCXLocator given a CourseLocator and a ccx id"""
        new_obj = cls(
            org=course_locator.org,
            course=course_locator.course,
            run=course_locator.run,
            branch=course_locator.branch,
            version_guid=course_locator.version_guid,
            deprecated=course_locator.deprecated,
            ccx=ccx,
        )
        return new_obj

    def _to_string(self):
        """
        Return a string representing this location.
        """
        parts = []
        if self.course and self.run:
            parts.extend([self.org, self.course, self.run])
            if self.branch:
                parts.append(
                    # pylint: disable=no-member
                    u"{prefix}@{branch}".format(
                        prefix=self.BRANCH_PREFIX, branch=self.branch
                    )
                )
        if self.version_guid:
            parts.append(
                # pylint: disable=no-member
                u"{prefix}@{guid}".format(
                    prefix=self.VERSION_PREFIX, guid=self.version_guid
                )
            )
        parts.append(
            u"{prefix}@{ccx}".format(
                prefix=self.CCX_PREFIX, ccx=self.ccx)
        )
        return u"+".join(parts)
