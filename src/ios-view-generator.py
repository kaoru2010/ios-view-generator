#!/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
from xml.parsers import expat
from ios_view_gen import os_view_parsers

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
    current_parser = None
    parser_stack = []

    def __init__(self, pf):
        self.pf = pf

        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.handle_start_element
        self.parser.EndElementHandler = self.handle_end_element

    def parse(self, src):
        self.parser.Parse(src)

    def handle_start_element(self, name, attrs):
        #print name
        #print attrs
        p = self.pf.create(name, attrs)
        if p is None:
            p = os_view_parsers.ViewParser(name, attrs)
        self.current_parser = p
        self.parser_stack.append(p)
        p.handle_start_element(name, attrs)

    def handle_end_element(self, name):
        p = self.parser_stack.pop()
        p.handle_end_element(name)
        self.current_parser = p

pf = ParserFactory()
pf.add_parser_creator('TextView', lambda tag_name, attrs: os_view_parsers.TextViewParser(tag_name, attrs))

parser = OptionParser()
(options, args) = parser.parse_args()

layout_xml_parser = LayoutXmlParser(pf)

with open(args[0], 'rb') as f:
    src = f.read()
    layout_xml_parser.parse(src)
