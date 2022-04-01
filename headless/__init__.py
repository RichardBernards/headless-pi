#!/usr/bin/env python

import headless.app

import logging

def main():
	logging.basicConfig(level=logging.INFO)
	headless.app.HeadlessPiApp().run()
	print("nice")
