# -*- coding: utf-8 -*-
"""
setuptools>=40.1.0
"""
from setuptools import setup, find_namespace_packages

#
#
#
package_name = "ageha"
version = "0.0.0.1"

setup(
    name=package_name,
    version=version,
    
    packages=find_namespace_packages(exclude=['tests', 'tests.*']),
    
    license='MIT',
    
    install_requires=[],
    
    author='Goro Sakata',
    author_email='gorosakata@ya.ru',
    url='',
    
    description='A set of parser and text function for Japanese',
    long_description="""
    ageha is a set of parser and text function for Japanese.
    """,
)



