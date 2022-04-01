#!/usr/bin/env python
import logging


def show_line(screen, text):
	logging.info('Drawing line for screen')
	screen.clear()
	screen.draw.rectangle((1, 1, screen.width-2, screen.height-2), outline=255, fill=0)
	screen.draw.text((1, 11), "  " + text, font=screen.font, fill=255)
	screen.paint()

def show_two_lines(screen, line1, line2):
	logging.info('Drawing two lines for screen')
	screen.clear()
	screen.draw.rectangle((1, 1, screen.width-2, screen.height-2), outline=255, fill=0)
	screen.draw.text((1, 6), " " + line1, font=screen.font, fill=255)
	screen.draw.text((1, 16), " " + line2, font=screen.font, fill=255)
	screen.paint()
