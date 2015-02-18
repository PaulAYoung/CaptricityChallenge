#!/usr/bin/env python
# -*- coding: utf-8 -*-

from captricity.models import Base, engine

Base.metadata.create_all(engine)
