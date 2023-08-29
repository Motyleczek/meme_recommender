#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
from ..database import *

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


# here we are ensuring that the values in .env are imported into Website, nice
class Website(metaclass=SingletonMeta):
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.environ["APP_SECRET"]
        self.app.config[
            'SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'

        self.db = SQLAlchemy(self.app)

        # register all models here
        # self.TestTable = createTestTable(self.db)
        # self.Clients = create_clients(self.db)
        # self.Products = create_products(self.db)
        # self.Prices = create_prices(self.db)
        # self.PriceQuotations = create_price_quotations(self.db)
        # self.SalesProposals = create_sales_proposals(self.db)
        # self.Sales = create_sales(self.db)
        # self.Reviews = create_reviews(self.db)
        # self.Suppliers = create_suppliers(self.db)
        # self.SupplierOffers = create_supplier_offers(self.db)
        # self.Stock = create_stock(self.db)
        # self.UnitConversion = create_unit_conversion(self.db)
        # self.Status = create_status(self.db)
        # self.Unit = create_unit(self.db)

        with self.app.app_context():
            self.db.create_all()
            #self.set_initial_values()
            print('Database schema has been synchronized')

    