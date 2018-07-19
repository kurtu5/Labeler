# -*- coding: utf-8 -*-

class BaseInteractor(object):
    def __init__(self):
        self.view = None
        self.presenter = None

    def start(self, presenter, view):
        self.presenter = presenter
        self.view = view
