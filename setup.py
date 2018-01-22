from setuptools import find_packages, setup

setup(
    name='ugh',
    version='0.1.0',
    description='Use JSON templates to create terminal UI with urwid.',
    url='https://github.com/meyer1994/ugh',
    download_url='https://github.com/meyer1994/ugh/archive/v0.1.0.tar.gz',
    author='João Vicente Meyer',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools'],
    keywords='ugh urwid terminal curses development ui interface',
    packages=find_packages(exclude=['tests']),
    install_requires=['urwid'],
    python_requires='>=3.6',
)
