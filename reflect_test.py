#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 17:49:44 2018

@author: Lee
"""

import pandas as pd
from sqlalchemy import create_engine, MetaData
from config.SQL_connect import enginestr
from dbutils import de_dup_tables, inc_strikes, msg_to_log, to_sql_k



df = pd.read_sql_table('bsh-test', engine, parse_dates=True)


