# -*- coding: utf-8 -*-
from abc import abstractproperty
from opaque_keys.edx.keys import CourseKey


class CCXKey(CourseKey):

    @abstractproperty
    def ccx(self):
        """The id of the ccx for this key"""
        raise NotImplementedError()
