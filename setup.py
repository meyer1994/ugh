from setuptools import find_packages, setup

setup(
    name='ugh',
    version='0.1.0',
    description='Use JSON templates to create terminal UI with urwid.',
    url='https://github.com/meyer1994/ugh',
    author='João Vicente Meyer',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
         'License :: OSI Approved :: GPL-3.0 License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.6-dev',
        'Programming Language :: Python :: 3.7-dev',
        'Programming Language :: Python :: nightly'],
    keywords='ugh urwid terminal curses development ui interface',
    packages=find_packages(exclude=['tests']),
    install_requires=['urwid'],
    python_requires='>=3.6',
    )
