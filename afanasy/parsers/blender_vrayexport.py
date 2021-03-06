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

from parsers import parser
import re
#automatic scripts are disabled

#Exporting data for frame 110 done
#Exporting data for frame 1...

#Traceback (most recent call last):

CONFIGMISING = 'automatic scripts are disabled'
TRACEBACK = "Traceback (most recent call last):"

re_frame = re.compile(
    r'Exporting data for frame ([0-9]*)'
)

class blender_vrayexport(parser.parser):
    'VrayExport based on simple generic parser'
    def __init__( self):
        parser.parser.__init__( self)
        self.count=0

    def do( self, data, mode):
        txt_pos = data.rfind(CONFIGMISING)
        if txt_pos > -1:
            #print ("CONFIGMISING")
            self.error = True

        txt_pos = data.rfind(TRACEBACK)
        if txt_pos > -1:
            #print ("TRACEBACK")
            self.error = True

        match = re_frame.findall(data)
        if len(match):
            #nframe = int(match[-1])
            self.count +=1
            self.percent = (self.count*100) / (self.numframes*100)

