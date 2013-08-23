from setuptools import setup, find_packages
setup(
    name = 'chefssh',
    version = '0.1',

    install_requires = ['PyChef>=0.2.1'],

    package_dir = {'': 'src'},
    packages = find_packages('src'),

    entry_points =  {
                        'console_scripts': [
                            'chef-ssh=chefssh.entry:ssh',
                            'chef-scp=chefssh.entry:scp'
                        ]
                    },
)
