# -*- coding: utf-8 -*-
# ###################################################
# Copyright (C) 2011 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################
from fife.extensions import pychan

from horizons.gui.widgets  import TooltipButton
from horizons.gui.tabs import OverviewTab
from horizons.i18n import load_xml_translated
from horizons.util import Callback
from horizons.util import Rect, Circle, Point
from horizons.util.shapes.radiusshape import RadiusRect
from horizons.world.building.nature import Field

class BuildingRelatedFieldsTab(OverviewTab):
	relatedfields_gui_xml = "relatedfields.xml"

	def  __init__(self, instance, icon_path='content/gui/icons/tabwidget/production/related_%s.png'):
		super(BuildingRelatedFieldsTab, self).__init__(
			widget = 'overview_buildingrelatedfields.xml',
			instance = instance, 
			icon_path='content/gui/icons/tabwidget/production/related_%s.png'
		)
		self.tooltip = _("Building related Fields")

	def refresh(self):
		"""This function is called by the TabWidget to redraw the widget."""
		
		# remove old field data
		parent_container = self.widget.child_finder('related_fields')
		while len(parent_container.children) > 0:
			parent_container.removeChild(parent_container.children[0])

		# Load all related Fields of this Farm
		providers = self.instance.island.get_providers_in_range(RadiusRect(self.instance.position, self.instance.radius), 
																	reslist=self.instance.get_needed_resources())
		providers = [ p for p in providers if isinstance(p, Field) ]

		for p in sorted(providers):
			gui = load_xml_translated(self.relatedfields_gui_xml)
			container = gui.findChild(name="fields_container")
			
			# Display Informations
			if p.name.lower().find("potato") > -1:
				container.findChild(name="image").image = "content/gui/icons/buildmenu/potatoes.png"
			else:
				container.findChild(name="image").image = "content/gui/icons/buildmenu/"+p.name.lower().replace(" ", "")+".png"
			
			container.findChild(name="name").text = unicode(p.name)
			
			container.stylize('menu_black')
			parent_container.addChild(container)

		super(BuildingRelatedFieldsTab, self).refresh()

