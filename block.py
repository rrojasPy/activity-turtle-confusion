# -*- coding: utf-8 -*-
#Copyright (c) 2010 Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

from constants import *
from sprite_factory import *
import sprites
from gettext import gettext as _

#
# A class for the list of blocks and everything they share in common
#
class Blocks:
    def __init__(self):
        self.list = []

    def get_block(self, i):
        if i < 0 or i > len(self.list)-1:
            return(None)
        else:
            return(self.list[i])

    def length_of_list(self):
        return(len(self.list))

    def append_to_list(self,block):
        self.list.append(block)

    def remove_from_list(self, block):
        if block in self.list:
            self.list.remove(block)

    def print_list(self):
        for i, block in enumerate(self.list):
            print "%d: %s" % (i, block.name)


    #
    # sprite utilities
    #
    def spr_to_block(self, spr):
        for b in self.list:
            if spr == b.spr:
                return b
        return None

#
# A class for the individual blocks
#
class Block:
    def __init__(self, block_list, sprite_list, proto_name, x, y, labels=[], 
                 colors=["#00FF00","#00A000"], scale=2.0):
        self.spr = None
        self.shape = None
        self.selected_shape = None
        self.name = proto_name
        self.docks = None
        self.connections = None
        self._new_block_from_prototype(sprite_list, proto_name, labels, colors,
                                       scale, x, y)
        block_list.append_to_list(self)
        #
        # TODO:
        # Logo code
        # HTML code
        # debug code
        # etc.

    def _new_block_from_prototype(self, sprite_list, name, labels, colors,
                                  scale, x, y):
        if len(labels) == 0:
            print "new block: %s (%d %d)" % (name, x, y)
        else:
            print "new block: %s %s (%d %d)" % (name, labels[0], x, y)

        svg = SVG()
        if name in TURTLE_PALETTE:
            svg.set_colors(TURTLE_COLORS)
        elif name in PEN_PALETTE:
            svg.set_colors(PEN_COLORS)
        elif name in NUMBER_PALETTE:
            svg.set_colors(NUMBER_COLORS)
        elif name in BLOCKS_PALETTE:
            svg.set_colors(BLOCKS_COLORS)
        elif name in MISC_PALETTE:
            svg.set_colors(MISC_COLORS)
        elif name in FLOW_PALETTE:
            svg.set_colors(FLOW_COLORS)
        elif name in PORTFOLIO_PALETTE:
            svg.set_colors(PORTFOLIO_COLORS)
        svg.set_scale(scale)
        svg.set_gradiant(True)
        svg.set_innie([False])
        svg.set_outie(False)
        svg.set_tab(True)
        svg.set_slot(True)
        xoff = INNIE*scale-2
        yoff = SLOTY*scale-1
        if name in BASIC_STYLE:
            svg.expand(40,0)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2),('flow',False,0,self.height-yoff))
        elif name in BASIC_STYLE_HEAD:
            svg.expand(40,0)
            svg.set_slot(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('start',True,0,2),('flow',False,0,self.height-yoff))
        elif name in BASIC_STYLE_HEAD_1ARG:
            svg.expand(40,0)
            svg.set_slot(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('start',True,0,0), ('string',False,self.width,12),
                          ('flow',False,0,self.height-yoff))
        elif name in BASIC_STYLE_TAIL:
            svg.expand(40,0)
            svg.set_tab(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2),('unavailable',False,0,0))
        elif name in BASIC_STYLE_1ARG:
            svg.expand(25,0)
            svg.set_innie([True])
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2), ('num',False,self.width-xoff,12),
                          ('flow',False,0,self.height-yoff))
        elif name in BASIC_STYLE_2ARG:
            svg.expand(25,0)
            svg.set_innie([True,True])
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2), ('num',False,self.width-xoff,12),
                          ('num',False,self.width-xoff,54), 
                          ('flow',False,0,self.height-yoff))
        elif name in BOX_STYLE:
            svg.expand(60,0)
            self._make_basic_box(sprite_list, svg, x, y)
            self.docks = (('num',True,0,12),('unavailable',False,0,12))
        elif name in NUMBER_STYLE:
            svg.expand(25,0)
            svg.set_innie([True,True])
            svg.set_outie(True)
            svg.set_tab(False)
            svg.set_slot(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('num',True,0,12), ('num',False,self.width-xoff,12),
                          ('num',False,self.width-xoff,54)) 
        elif name in NUMBER_STYLE_1ARG:
            svg.expand(25,0)
            svg.set_innie([True])
            svg.set_outie(True)
            svg.set_tab(False)
            svg.set_slot(False)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('num',True,0,12),('num',False,self.width-xoff,12)) 
        elif name in NUMBER_STYLE_PORCH:
            svg.expand(25,0)
            svg.set_innie([True,True])
            svg.set_outie(True)
            svg.set_tab(False)
            svg.set_slot(False)
            svg.set_porch(True)
            self._make_basic_block(sprite_list, svg, x, y)
            xoff += svg._porch
            self.docks = (('num',True,0,12), ('num',False,self.width-xoff,12),
                          ('num',False,self.width-xoff,54)) 
        elif name in COMPARE_STYLE:
            self._make_boolean_compare(sprite_list, svg, x, y)
            self.docks = (('bool',True,0,self.height-12),
                          ('num',False,self.width-xoff,12),
                          ('num',False,self.width-xoff,54)) 
        elif name in BOOLEAN_STYLE:
            self._make_boolean_and_or(sprite_list, svg, x, y)
            self.docks = (('bool',False,0,self.height-12),
                          ('bool',False,self.width-xoff,12))
        elif name in NOT_STYLE:
            self._make_boolean_not(sprite_list, svg, x, y)
            self.docks = (('bool',True,0,self.height-12),
                          ('bool',False,self.width-xoff,12))
        elif name in FLOW_STYLE:
            svg.expand(25,0)
            svg.set_slot(True)
            self._make_basic_flow(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2),
                          ('flow',False,self.width/2, self.height-yoff))
        elif name in FLOW_STYLE_1ARG:
            svg.expand(25,0)
            svg.set_slot(True)
            svg.set_tab(True)
            svg.set_innie([True])
            self._make_basic_flow(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2),
                          ('num',False,self.width-xoff,12),
                          ('flow',False, 0, self.height-yoff)
                          ('flow',False,self.width/2, self.height-yoff))
        elif name in FLOW_STYLE_BOOLEAN:
            svg.expand(25,0)
            svg.set_slot(True)
            svg.set_tab(True)
            svg.set_boolean(True)
            self._make_basic_flow(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2),
                          ('bool',False,self.width-xoff,12),
                          ('flow',False, 0, self.height-yoff)
                          ('flow',False,self.width/2, self.height-yoff))
        else:
            svg.expand(40,0)
            self._make_basic_block(sprite_list, svg, x, y)
            self.docks = (('flow',True,0,2),('flow',False,0,self.height-yoff))
            print "don't know how to create a block for %s" % (name)

        if len(labels) > 0:
            if BLOCK_NAMES.has_key(name):
                self.spr.set_label(BLOCK_NAMES[name])
            for i, label in enumerate(labels):
                if i > 0:
                    self.spr.set_label(label, labels[i])

        self.type = 'block'
        if DEFAULTS.has_key(name):
            self.defaults = DEFAULTS[name]
        else:
            self.defaults = []

    def _make_basic_block(self, sprite_list, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.basic_block())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_block())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

    def _make_basic_box(self, sprite_list, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.basic_box())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_box())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

    def _make_basic_flow(self, sprite_list, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.basic_flow())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.basic_flow())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

    def _make_boolean_compare(self, sprite_list, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.boolean_compare())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.boolean_compare())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

    def _make_boolean_and_or(self, sprite_list, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.boolean_and_or())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.boolean_and_or())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)

    def _make_boolean_not(self, sprite_list, svg, x, y):
        self.shape = svg_str_to_pixbuf(svg.boolean_not())
        self.width = svg.get_width()
        self.height = svg.get_height()
        svg.set_stroke_width(SELECTED_STROKE_WIDTH)
        svg.set_stroke_color(SELECTED_COLOR)
        self.selected_shape = svg_str_to_pixbuf(svg.boolean_not())
        self.spr = sprites.Sprite(sprite_list, x, y, self.shape)
