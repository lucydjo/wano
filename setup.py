from setuptools import setup, find_packages

setup(
    name='wano',
    version='0.5',
    packages=find_packages(),  # Trouver tous les packages y compris 'wano', 'wano.templates', 'wano.static', etc.
    entry_points={
        'console_scripts': [
            'wano = wano.main:main',
        ],
    },
    install_requires=[
        'pyngrok',
        'uuid',
        'flask'
    ],
)