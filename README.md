[![Build Status](https://travis-ci.org/SebKuzminsky/pycam.svg?branch=master)](https://travis-ci.org/SebKuzminsky/pycam)

# PyCAM: a toolpath generator

PyCAM generates toolpaths (GCode) based on 2D or 3D models for 3-axis CNC machining.


## Dependencies
Dependencies are located in `requirements.txt`. They can be installed with Pip:
```
pip install -r requirements.txt
```

You would also need [freeglut](http://freeglut.sourceforge.net/) installed (`pacman -S freeglut` on Arch-based distributions).

It is recommended to install and run dependencies in a virtual environment when developing.

## Running

Extract the archive or clone the repository.

Graphical Interface: `pycam/run_gui.py`

Scripted Toolpath Processing: `pycam/run_cli.py FLOW_SPECIFICATION_FILE.yml`

JSON files can be converted to YAML configuration with `pycam/json2yml.py`

Feel free to use `--help` option with CLI scripts.

## Resources

See the [documentation](http://pycam.sourceforge.net/introduction/) for a short introduction.

* [Website / Documentation](http://pycam.sf.net/)
* [Getting started](http://pycam.sf.net/getting-started.md)
* [FAQ](http://pycam.sf.net/faq.md)
* [Video tutorials](http://vimeo.com/channels/pycam)
* [Screenshots](http://pycam.sourceforge.net/screenshots/)
* [Mailing lists](https://sourceforge.net/p/pycam/mailman/)


## Development

* [Code Repository](https://github.com/SebKuzminsky/pycam)
* [Issue Tracker](https://github.com/SebKuzminsky/pycam/issues)


## Contributors

* Lode Leroy: initiated the project; developed the toolpath generation,
  collision detection, geometry, Tk interface, ...
* Lars Kruse: GTK interface and many features
* Paul: GCode stepping precision
* Arthur Magill: distutils packaging
* Sebastian Kuzminsky: debian packaging
* Nicholas Humfrey: documentation, recovery of old sourceforge-wiki
* Piers Titus van der Torren: documentation
* Reuben Rissler: gtk3 migration
