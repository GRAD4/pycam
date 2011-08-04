# -*- coding: utf-8 -*-
"""
$Id$

Copyright 2011 Lars Kruse <devel@sumpfralle.de>

This file is part of PyCAM.

PyCAM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCAM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCAM.  If not, see <http://www.gnu.org/licenses/>.
"""

import pycam.Plugins
import pycam.Geometry.Point


GTK_COLOR_MAX = 65535.0


class OpenGLViewModel(pycam.Plugins.PluginBase):

    DEPENDS = ["OpenGLWindow", "Models"]
    CATEGORIES = ["Model", "Visualization", "OpenGL"]

    def setup(self):
        import gtk
        import OpenGL.GL
        self._gtk = gtk
        self._GL = OpenGL.GL
        self.core.register_event("visualize-items", self.draw_model)
        self.core.emit_event("visual-item-updated")
        self._cache = {}
        return True

    def teardown(self):
        self.core.unregister_event("visualize-items", self.draw_model)
        self.core.emit_event("visual-item-updated")

    def _get_cache_key(self, model, *args, **kwargs):
        if hasattr(model, "uuid"):
            return "%s - %s - %s" % (model.uuid, repr(args), repr(kwargs))
        else:
            return None

    def draw_model(self):
        GL = self._GL
        if self.core.get("show_model") \
                and not (self.core.get("show_simulation") \
                    and self.core.get("simulation_toolpath_moves")):
            for model in self.core.get("models").get_visible():
                color_str = self.core.get("models").get_attr(model, "color")
                alpha = self.core.get("models").get_attr(model, "alpha")
                col = self._gtk.gdk.color_parse(color_str)
                color = (col.red / GTK_COLOR_MAX, col.green / GTK_COLOR_MAX,
                        col.blue / GTK_COLOR_MAX, alpha / GTK_COLOR_MAX)
                GL.glColor4f(*color)
                # reset the material color
                GL.glMaterial(GL.GL_FRONT_AND_BACK,
                        GL.GL_AMBIENT_AND_DIFFUSE, color)
                # we need to wait until the color change is active
                GL.glFinish()
                key = self._get_cache_key(model, color=color,
                        show_directions=self.core.get("show_directions"))
                do_caching = not key is None
                if do_caching and not key in self._cache:
                    # Rendering a display list takes less than 5% of the time for a
                    # complete rebuild.
                    list_index = GL.glGenLists(1)
                    if list_index > 0:
                        # somehow "GL_COMPILE_AND_EXECUTE" fails - we render it later
                        GL.glNewList(list_index, GL.GL_COMPILE)
                    else:
                        do_caching = False
                    # next: compile an OpenGL display list
                if not do_caching or (not key in self._cache):
                    self.core.call_chain("draw_models", [model])
                if do_caching:
                    if not key in self._cache:
                        GL.glEndList()
                        GL.glCallList(list_index)
                        self._cache[key] = list_index
                    else:
                        # render a previously compiled display list
                        GL.glCallList(self._cache[key])


class OpenGLViewModelTriangle(pycam.Plugins.PluginBase):

    DEPENDS = ["OpenGLViewModel"]
    CATEGORIES = ["Model", "Visualization", "OpenGL"]

    def setup(self):
        import OpenGL.GL
        self._GL = OpenGL.GL
        self.core.register_chain("draw_models", self.draw_triangle_model, 10)
        return True

    def teardown(self):
        self.core.unregister_chain("draw_models", self.draw_triangle_model)

    def draw_triangle_model(self, models):
        if not models:
            return
        GL = self._GL
        removal_list = []
        for index in range(len(models)):
            model = models[index]
            if not hasattr(model, "triangles"):
                continue
            get_coords = lambda p: (p.x, p.y, p.z)
            def calc_normal(main, normals):
                suitable = pycam.Geometry.Point.Vector(0, 0, 0)
                for normal, weight in normals:
                    dot = main.dot(normal)
                    if dot > 0:
                        suitable = suitable.add(normal.mul(weight * dot))
                return suitable.normalized()
            vertices = {}
            for t in model.triangles():
                for p in (t.p1, t.p2, t.p3):
                    coords = get_coords(p)
                    if not coords in vertices:
                        vertices[coords] = []
                    vertices[coords].append((t.normal.normalized(), t.get_area()))
            GL.glBegin(GL.GL_TRIANGLES)
            for t in model.triangles():
                # The triangle's points are in clockwise order, but GL expects
                # counter-clockwise sorting.
                for p in (t.p1, t.p3, t.p2):
                    coords = get_coords(p)
                    normal = calc_normal(t.normal.normalized(), vertices[coords])
                    GL.glNormal3f(normal.x, normal.y, normal.z)
                    GL.glVertex3f(p.x, p.y, p.z)
            GL.glEnd()
            removal_list.append(index)
        # remove all models that we processed
        removal_list.reverse()
        for index in removal_list:
            models.pop(index)


class OpenGLViewModelGeneric(pycam.Plugins.PluginBase):

    DEPENDS = ["OpenGLViewModel"]
    CATEGORIES = ["Model", "Visualization", "OpenGL"]

    def setup(self):
        self.core.register_chain("draw_models", self.draw_generic_model, 100)
        return True

    def teardown(self):
        self.core.unregister_chain("draw_models", self.draw_generic_model)

    def draw_generic_model(self, models):
        removal_list = []
        for index in range(len(models)):
            model = models[index]
            for item in model.next():
                # ignore invisble things like the normal of a ContourModel
                if hasattr(item, "to_OpenGL"):
                    item.to_OpenGL(show_directions=self.core.get("show_directions"))
            removal_list.append(index)
        removal_list.reverse()
        for index in removal_list:
            removal_list.pop(index)
