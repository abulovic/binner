import setuptools
from distutils.core import setup

setup (
	name='MetaBinner',
	version='0.1.0',
	packages=['data','formats','ncbi','snippets','solver', 'test', 'utils'],
	#scripts=['snippets/run_binner.py'],
	requires=[
		"MySQL_python(==1.2.4)",
		"SQLAlchemy(==0.8.0)",
	],
)