from distutils.core import setup

setup (
	name='MetaBinner',
	version='0.1.0',
	packages=['data','formats','ncbidb','snippets','utils'],
	scripts=['bin/parse_blast_output.py'],
	install_requires=[
		'MySQL_python == 1.2.4',
		'SQLAlchemy == 0.8.0',
	],
)