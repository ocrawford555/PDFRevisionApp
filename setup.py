from distutils.core import setup

install_requires = [
    'aiohttp>=2.3.5',
    'gunicorn~=19.7.1',
    'jira~=2.0.0',
    'dnspython>=1.15,<2.1',
    "PyJWT==1.6.4",
    'aws-requests-auth~=0.4.1',
    "elasticsearch>=6.0.0,<7.0.0",
    "elasticsearch-dsl>=6.0.0,<7.0.0",
    "beautifulsoup4>=4.6.3",
    "halflife>=1.0.0",
    "numpy~=1.15.2",
]

setup(
    name='PDFRevisionApp',
    version='1',
    packages=[''],
    url='https://github.com/ocrawford555/PDFRevisionApp',
    license='',
    author='Oliver Crawford',
    author_email='o.crawford@hotmail.co.uk',
    description='See Github for more details: https://github.com/ocrawford555/PDFRevisionApp', requires=['PyPDF2',
                                                                                                         'flask']
)
