#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module for grid plotting canvas.
"""

import numpy as np
import matplotlib.pyplot as plt

from catplot.canvas import Canvas
from catplot.grid_components.nodes import Node2D


class Grid2DCanvas(Canvas):
    """ Canvas for 2D grid plotting.
    """
    def __init__(self, **kwargs):
        super(Grid2DCanvas, self).__init__(**kwargs)

        # Attributes for 2D grid canvas.
        self.nodes = []
        self.edges = []

        # Initial path collection.
        self.collection = self.axes.scatter([], [])

    def add_node(self, node):
        """ Add a node to grid canvas.
        """
        # Check node.
        if not isinstance(node, Node2D):
            raise ValueError("node must be a Node2D object")

        self.nodes.append(node)

    @property
    def node_coordinates(self):
        """ Coordinates for all nodes.
        """
        return np.array([node.coordinate.tolist() for node in self.nodes])

    @property
    def node_edgecolors(self):
        """ Color codes for node edges.
        """
        return [node.edgecolor for node in self.nodes]

    @property
    def node_colors(self):
        """ Colors for all nodes.
        """
        return [node.color for node in self.nodes]

    def _get_data_limits(self):
        """ Private helper function to get the limits of data.
        """
        x = self.node_coordinates[:, 0]
        max_x, min_x = np.max(x), np.min(x)

        y = self.node_coordinates[:, 1]
        max_y, min_y = np.max(y), np.min(y)

        return self._limits(max_x, min_x, max_y, min_y)

    def draw(self):
        """ Draw all nodes and edges on canvas.
        """
        if not any([self.nodes, self.edges]):
            self._logger.warning("Attempted to draw in an empty canvas")
            return

        # Add nodes to canvas.
        self.collection.set_offsets(self.node_coordinates)
        self.collection.set_facecolor(self.node_colors)
        self.collection.set_edgecolor(self.node_edgecolors)

        # Set axes limits.
        limits = self._get_data_limits()
        self.axes.set_xlim(limits.min_x, limits.max_x)
        self.axes.set_ylim(limits.min_y, limits.max_y)

