# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

#Authors: CGRU-Afanasy / Eibriel

#Note: Set vray debugging level to 3

from parsers import parser

import re

"""re_frame = re.compile(
	r'SCEN.*(progr: begin scene preprocessing for frame )([0-9]+)'
)"""
re_frame = re.compile(
	r'Starting frame ([0-9]+)'
)

#re_number = re.compile(r'[0-9]+')
re_percent = re.compile(
	r'Rendering image...:([ ]{,})([0-9]{1,2}.*)(%[ ]{,}).*'
)

#re_percent = re.compile(
#    r'warning: Bitmap file "" failed to load:'
#}

#failed to load

#Closing log - 0 error(s), 0 warning(s)

#Preparing scene for rendering...: 90.00%
#Starting frame 5
#Preparing scene for frame...: 65.57%
#Building static raycast accelerator...: 32.36%
#Compiling geometry...: 10.66%
#Prepass 1 of 4
#Building light cache...:  5.32%
#Prefiltering light cache...: 55.00%

#Violacion de segmento

class vrayfull(parser.parser):
    """VRay Standalone (Modified for Kiribati)
    """

    def __init__(self):
        parser.parser.__init__(self)
        self.act = ''
        self.fdone = 0
        self.prev = ''

    def do(self, data, mode):
        """Missing DocString

        :param data:
        :param mode:
        :return:
        """

        if len(data) < 1:
            return

        totaldata = "%s%s" % (self.prev, data)
        self.prev = data
        data = totaldata

        match = re_percent.findall(data)
        if len(match):
            #print (match[-1][1])
            percentframe = float(match[-1][1])
            self.percent = int(percentframe/self.numframes+((100./self.numframes)*(self.fdone-1)))
            self.percentframe = int(percentframe)
            
        match = re_frame.findall(data)
        if len(match):
            frame = float(match[-1])
            self.frame = int(frame)
            self.percentframe = 0.
            self.fdone +=1

        txt_pos = data.rfind('Traceback (most recent call last):')
        if txt_pos > -1:
            #print ("TRACEBACK")
            self.error = True

        txt_pos = data.rfind('warning: Bitmap file')
        if txt_pos > -1:
            self.warning = True
        
        txt_pos = data.rfind('Prefiltering light cache')
        if txt_pos > -1:
            self.act="pflc"
        if txt_pos < 0:
            txt_pos = data.rfind('Building light cache')
            if txt_pos > -1:
                self.act="blc"
        if txt_pos < 0:
            txt_pos = data.rfind('Prepass')
            if txt_pos > -1:
                self.act="ppass"
        if txt_pos < 0:
            txt_pos = data.rfind('Compiling geometry')
            if txt_pos > -1:
                self.act="compg"
        if txt_pos < 0:
            txt_pos = data.rfind('Building static raycast accelerator')
            if txt_pos > -1:
                self.act="bsra"
        if txt_pos < 0:
            txt_pos = data.rfind('Starting')
            if txt_pos > -1:
                self.act="start"
        if txt_pos < 0:
            txt_pos = data.rfind('Preparing scene for rendering')
            if txt_pos > -1:
                self.act="ps"
        if txt_pos < 0:
            txt_pos = data.rfind('Rendering image')
            if txt_pos > -1:
                self.act="ri"
         
        self.activity = "F%s:%s" % (self.frame, self.act)
			

