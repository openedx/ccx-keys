import ddt
from bson.objectid import ObjectId
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey
from opaque_keys.edx.locator import CourseLocator
from opaque_keys.edx.tests import LocatorBaseTest, TestDeprecated

from ccx_keys.locator import CCXLocator


@ddt.ddt
class TestCCXKeys(LocatorBaseTest, TestDeprecated):
    """
    Tests of :class:`.CCXKey` and :class:`.CCXLocator`
    """

    def test_ccx_constructor_package_id(self):
        """Verify a locator constructed without branch or version is correct"""
        org = 'mit.eecs'
        course = '6002x'
        run = '2014_T2'
        ccx = '1'
        testurn = '{}+{}+{}+{}@{}'.format(
            org, course, run, CCXLocator.CCX_PREFIX, ccx
        )
        testobj = CCXLocator(org=org, course=course, run=run, ccx=ccx)

        self.check_course_locn_fields(
            testobj, org=org, course=course, run=run
        )
        self.assertEqual(testobj.ccx, ccx)
        # Allow access to _to_string
        # pylint: disable=protected-access
        self.assertEqual(testobj._to_string(), testurn)

    def test_ccx_constructor_version_guid(self):
        """Verify a locator constructed with only version_guid is correct"""
        test_id_loc = '519665f6223ebd6980884f2b'
        ccx = '1'
        expected_urn = '{}@{}+{}@{}'.format(
            CCXLocator.VERSION_PREFIX, test_id_loc,
            CCXLocator.CCX_PREFIX, ccx
        )
        testobj = CCXLocator(version_guid=test_id_loc, ccx=ccx)

        self.check_course_locn_fields(
            testobj,
            version_guid=ObjectId(test_id_loc),
        )
        self.assertEqual(testobj.ccx, ccx)
        # Allow access to _to_string
        # pylint: disable=protected-access
        self.assertEqual(testobj._to_string(), expected_urn)

    def test_ccx_constructor_package_id_separate_branch(self):
        """Verify a locator constructed with branch is correct"""
        org = 'mit.eecs'
        course = '6002x'
        run = '2014_T2'
        test_branch = 'published'
        ccx = '1'
        expected_urn = '{}+{}+{}+{}@{}+{}@{}'.format(
            org, course, run,
            CCXLocator.BRANCH_PREFIX, test_branch,
            CCXLocator.CCX_PREFIX, ccx
        )
        testobj = CCXLocator(
            org=org, course=course, run=run, branch=test_branch, ccx=ccx
        )

        self.check_course_locn_fields(
            testobj,
            org=org,
            course=course,
            run=run,
            branch=test_branch,
        )
        self.assertEqual(testobj.ccx, ccx)
        # Allow access to _to_string
        # pylint: disable=protected-access
        self.assertEqual(testobj._to_string(), expected_urn)

    def test_ccx_constructor_package_id_branch_and_version_guid(self):
        """Verify a locator constructed with branch and version is correct"""
        test_id_loc = '519665f6223ebd6980884f2b'
        org = 'mit.eecs'
        course = '~6002x'
        run = '2014_T2'
        branch = 'draft-1'
        ccx = '1'
        expected_urn = '{}+{}+{}+{}@{}+{}@{}+{}@{}'.format(
            org, course, run,
            CCXLocator.BRANCH_PREFIX, branch,
            CCXLocator.VERSION_PREFIX, test_id_loc,
            CCXLocator.CCX_PREFIX, ccx
        )
        testobj = CCXLocator(
            org=org,
            course=course,
            run=run,
            branch=branch,
            version_guid=test_id_loc,
            ccx=ccx
        )

        self.check_course_locn_fields(
            testobj,
            org=org,
            course=course,
            run=run,
            branch=branch,
            version_guid=ObjectId(test_id_loc)
        )
        self.assertEqual(testobj.ccx, ccx)
        # Allow access to _to_string
        # pylint: disable=protected-access
        self.assertEqual(testobj._to_string(), expected_urn)

    @ddt.data(
        ('version_guid'),
        ('org', 'course', 'run'),
        ('org', 'course', 'run', 'branch'),
        ('org', 'course', 'run', 'version_guid'),
        ('org', 'course', 'run', 'branch', 'version_guid'),
    )
    def test_missing_ccx_id(self, fields):
        """Verify that otherwise valid arguments fail without ccx"""
        available_fields = {
            'version_guid': '519665f6223ebd6980884f2b',
            'org': 'mit.eecs',
            'course': '6002x',
            'run': '2014_T2',
            'branch': 'draft-1',
        }
        use_fields = dict(
            (k, v) for k, v in available_fields.items() if k in fields
        )
        with self.assertRaises(InvalidKeyError) as cm:
            CCXLocator(**use_fields)

        self.assertTrue(str(CCXLocator) in str(cm.exception))

    @ddt.unpack
    @ddt.data(
        {'fields': ('version_guid',),
         'url_template': '{CANONICAL_NAMESPACE}:{VERSION_PREFIX}@{version_guid}+{CCX_PREFIX}@{ccx}',
         },
        {'fields': ('org', 'course', 'run'),
         'url_template': '{CANONICAL_NAMESPACE}:{org}+{course}+{run}+{CCX_PREFIX}@{ccx}',
         },
        {'fields': ('org', 'course', 'run', 'branch'),
         'url_template': '{CANONICAL_NAMESPACE}:{org}+{course}+{run}+{BRANCH_PREFIX}@{branch}+{CCX_PREFIX}@{ccx}',
         },
        {'fields': ('org', 'course', 'run', 'version_guid'),
         'url_template': '{CANONICAL_NAMESPACE}:{org}+{course}+{run}+{VERSION_PREFIX}@{version_guid}+{CCX_PREFIX}@{ccx}',
         },
        {'fields': ('org', 'course', 'run', 'branch', 'version_guid'),
         'url_template': '{CANONICAL_NAMESPACE}:{org}+{course}+{run}+{BRANCH_PREFIX}@{branch}+{VERSION_PREFIX}@{version_guid}+{CCX_PREFIX}@{ccx}',},
    )
    def test_locator_from_good_url(self, fields, url_template):
        available_fields = {
            'version_guid': '519665f6223ebd6980884f2b',
            'org': 'mit.eecs',
            'course': '6002x',
            'run': '2014_T2',
            'branch': 'draft-1',
            'ccx': '1',
            'CANONICAL_NAMESPACE': CCXLocator.CANONICAL_NAMESPACE,
            'VERSION_PREFIX': CCXLocator.VERSION_PREFIX,
            'BRANCH_PREFIX': CCXLocator.BRANCH_PREFIX,
            'CCX_PREFIX': CCXLocator.CCX_PREFIX,
        }
        this_url = url_template.format(**available_fields)
        testobj = CourseKey.from_string(this_url)
        use_keys = dict(
            (k, v) for k, v in available_fields.items() if k in fields
        )

        if 'version_guid' in use_keys:
            use_keys['version_guid'] = ObjectId(use_keys['version_guid'])
        self.check_course_locn_fields(testobj, **use_keys)
        self.assertEqual(testobj.ccx, available_fields['ccx'])

    @ddt.data(
        ('version_guid'),
        ('org', 'course', 'run'),
        ('org', 'course', 'run', 'branch'),
        ('org', 'course', 'run', 'version_guid'),
        ('org', 'course', 'run', 'branch', 'version_guid'),
    )
    def test_from_course_locator_constructor(self, fields):
        available_fields = {
            'version_guid': '519665f6223ebd6980884f2b',
            'org': 'mit.eecs',
            'course': '6002x',
            'run': '2014_T2',
            'branch': 'draft-1',
        }
        ccx = '1'
        use_fields = dict((k, v) for k, v in available_fields.items() if k in fields)
        course_id = CourseLocator(**use_fields)
        testobj = CCXLocator.from_course_locator(course_id, ccx)

        if 'version_guid' in use_fields:
            use_fields['version_guid'] = ObjectId(use_fields['version_guid'])
        self.check_course_locn_fields(testobj, **use_fields)
        self.assertEqual(testobj.ccx, ccx)
