from setuptools import setup

setup(
    name='capd_short',
    version='0.1',
    packages=['gams_', 'gams_.abstract', 'gams_.with_imports', 'gams_.without_imports',
              'gams_.example_scripting_and_plots', 'tutorial_'],
    url='',
    license='',
    author='David Thierry',
    author_email='dmolinat@andrew.cmu.edu',
    description='pyomo models for the capd_short_course'
)
