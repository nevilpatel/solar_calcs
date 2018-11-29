from setuptools import setup, find_packages

setup(
    name='solar_calcs',
    version='0.1',
    # todo exclude not working in setup packages
    packages=find_packages(exclude=['solar_calcs.gas', 'solar_calcs.gas.bill', 'solar_calcs.gas.usage']),

    # data_files=[('solar_calcs\sample', ['solar_calcs\sample\yearly_electric.csv'])],
    url='http://solar_calcs',
    license='Open',
    author='Nevil Patel',
    author_email='nevil.patel@gmail.com',
    description='package to calculate solar installation',
    install_requires=['numpy'],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers'
    ],
    include_package_data=True,
    entry_points={  # Optional
        'console_scripts': [
            'analyze=solar_calcs.electric.bill.pge:main',
        ],
    },

)
