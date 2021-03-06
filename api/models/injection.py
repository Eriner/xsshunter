# -*- coding: utf-8 -*-
"""
@author: mandatory, moloch
Copyright 2016
"""

from sqlalchemy import Column, ForeignKey, and_
from sqlalchemy.types import BigInteger, String, Text, Unicode

from libs.sql_datatypes import UUIDType
from models import DBSession
from models.base import DatabaseObject


class Injection(DatabaseObject):

    owner_id = Column(UUIDType(), ForeignKey('user._id'), nullable=False)

    content_type = Column(Unicode(100))  # JavaScript/Image
    vulnerable_page = Column(Unicode(3000))
    victim_ip = Column(Unicode(100))
    referer = Column(Unicode(3000))
    user_agent = Column(Unicode(3000))
    cookies = Column(Unicode(5000))
    dom = Column(Text())
    origin = Column(Unicode(300))
    screenshot = Column(String(300))
    browser_time = Column(BigInteger())
    correlated_request = Column(Text())

    @classmethod
    def by_owner(cls, owner, limit=100, offset=0):
        return DBSession().query(cls).filter_by(
            owner_id=owner.id
        ).order_by(
            cls.created.desc()
        ).limit(limit).offset(offset)

    @classmethod
    def by_owner_and_id(cls, owner, injection_id):
        return DBSession.query(cls).filter(and_(
            cls.owner_id == owner.id,
            cls.id == injection_id
        )).first()

    def to_dict(self):
        return {
            "id": self.id,
            "created": str(self.created),
            "vulnerable_page": self.vulnerable_page,
            "victim_ip": self.victim_ip,
            "referer": self.referer,
            "user_agent": self.user_agent,
            "cookies": self.cookies,
            "dom": self.dom,
            "origin": self.origin,
            "screenshot": self.screenshot,
            "correlated_request": self.correlated_request,
            "browser_time": self.browser_time
        }

    def __str__(self):
        return self.vulnerable_page
