#!/usr/bin/env python
# -*- coding: utf-8 -*-

from captricity import app
from captricity import config

app.config.from_object(config.ConfigDev)
app.run(debug=True)
