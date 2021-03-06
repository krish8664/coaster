# -*- coding: utf-8 -*-

import unittest

from coaster.db import db
from coaster.sqlalchemy import BaseMixin, CoordinatesMixin

from test_models import app1, app2


class CoordinatesData(BaseMixin, CoordinatesMixin, db.Model):
    __tablename__ = 'coordinates_data'


# -- Tests --------------------------------------------------------------------


class TestCoordinatesColumn(unittest.TestCase):
    app = app1

    def setUp(self):
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        db.create_all()
        self.session = db.session

    def tearDown(self):
        self.session.rollback()
        db.drop_all()
        self.ctx.pop()

    def test_columns_created(self):
        table = CoordinatesData.__table__
        self.assertTrue(isinstance(table.c.latitude.type, db.Numeric))
        self.assertTrue(isinstance(table.c.longitude.type, db.Numeric))

    def test_columns_when_null(self):
        data = CoordinatesData()
        self.assertEqual(data.coordinates, (None, None))

    def test_column_set_value(self):
        data = CoordinatesData()
        data.coordinates = (12, 73)
        self.assertEqual(data.coordinates, (12, 73))
        db.session.add(data)
        db.session.commit()

        readdata = CoordinatesData.query.first()
        self.assertEqual(readdata.coordinates, (12, 73))


class TestCoordinatesColumn2(TestCoordinatesColumn):
    app = app2
