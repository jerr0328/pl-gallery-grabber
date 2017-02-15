from setuptools import (
    setup,
    find_packages,
    os,
)
from io import open


base_directory = os.path.dirname(__file__)


def get_module_name(line):
    filename = line.split('/')[-1]
    module_name = filename.split('.tar.gz')[0]
    return '-'.join(module_name.split('-')[:-1])


def get_requirements(filename):
    content = []
    with open(os.path.join(base_directory, filename)) as f:
        for line in f:
            # Temporary computation needed for planet-common-client and modules installed from GitHub
            if line.startswith('-e'):
                module = line.split("#egg=")[1]
            elif line.startswith(('https://', 'http://')):
                module = get_module_name(line)
            else:
                module = line
            content.append(module)
        return content

dev_requires = []
install_requires = get_requirements('requirements.txt')

COVERAGE_PACKAGES = find_packages(base_directory, exclude=["core", "*_tests", "*.*_tests", "*.migrations"])

if __name__ == "__main__":
    setup(
        name='pl-gallery-grabber',
        version='0.2',
        author='Jeremy Mayeres',
        url='https://github.com/jerr0328/pl-gallery-grabber',
        description='Planet Gallery Image Grabber',
        long_description=open('README.md', encoding='utf-8').read(),
        packages=find_packages(exclude=('*tests', )),
        install_requires=install_requires,
        extras_require={
            'dev': dev_requires,
        },
    )
