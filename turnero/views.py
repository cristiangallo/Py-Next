# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404


def index(request):
    args = {}
    return render(request, 'default/index.html', args)