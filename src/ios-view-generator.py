#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from xml.parsers import expat

class Outputter(object):
    state_stack = []
    indent = ''

    def blank(self):
        print

    def write_line(self, line):
        print self.indent + line

    def push_indent(self, indent):
        self.state_stack.append(self.indent)
        self.indent += indent

    def pop_indent(self):
        self.state_stack.pop()

class ParserFactory(object):
    parsers = {}

    def add_parser_creator(self, tag_name, parser_creator):
        self.parsers[tag_name] = parser_creator

    def create(self, tag_name, attrs):
        if tag_name in self.parsers:
            return self.parsers[tag_name](tag_name, attrs)
        else:
            return None

class LayoutXmlParser(object):
    def __init__(self, pf):
        self.pf = pf

        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.handle_start_element

    def parse(self, src):
        self.parser.Parse(src)

    def handle_start_element(self, name, attrs):
        #print name
        #print attrs
        p = self.pf.create(name, attrs)
        if p != None:
            p.handle_start_element(name, attrs)

class View(object):
    def __init__(self, tag_name, attrs):
        self.tag_name = tag_name
        self.attrs = attrs

class TextView(View):
    def handle_start_element(self, name, attrs):
        print name
        print attrs

pf = ParserFactory()
pf.add_parser_creator('TextView', lambda tag_name, attrs: TextView(tag_name, attrs))

parser = OptionParser()
(options, args) = parser.parse_args()

layout_xml_parser = LayoutXmlParser(pf)

with open(args[0], 'rb') as f:
    src = f.read()
    layout_xml_parser.parse(src)
