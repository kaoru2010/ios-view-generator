# -*- coding: utf-8 -*-


class ViewParser(object):
    def __init__(self, tag_name, attrs):
        self.tag_name = tag_name
        self.attrs = attrs

    def handle_start_element(self, name, attrs):
        pass

    def handle_end_element(self, name):
        pass

class TextViewParser(ViewParser):
    def handle_start_element(self, name, attrs):
        print 'UIView *v = CreateView([[' + name + ' alloc] init], ^(UIView *p) {'
        #print attrs

    def handle_end_element(self, name):
        print '});   // End of ' + name
        print '[p addSubView:v];'
