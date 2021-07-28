#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import io
import os
import subprocess
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# root dir
root = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = "EthTx"
DESCRIPTION = "EthTx transaction decoder."
URL = "https://github.com/EthTx/ethtx"
EMAIL = "karol@tfi.team, tomek@tfi.team, piotr.rudnik@tfi.team"
AUTHOR = "Karol Chojnowski, Tomasz Mierzwa, Piotr Rudnik"
REQUIRES_PYTHON = ">=3.7.0"

REQUIRED = []
REQUIRED_TEST = []

about = {
    "__version__": subprocess.check_output(
        ["git", "describe", "--tags"], universal_newlines=True
    ).strip()
}

try:
    with io.open(os.path.join(root, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION


def load_requirements(fname):
    """Load requirements from file."""
    with open(fname) as file:
        return file.read().splitlines()


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(root, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# *************** INSTALL *****************
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    license="Apache-2.0 License",
    packages=find_packages(exclude=["tests"]),
    tests_require=load_requirements("requirements_test.txt"),
    install_requires=load_requirements("requirements.txt"),
    include_package_data=True,
    test_suite="tests",
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    # $ setup.py publish support.
    cmdclass={"upload": UploadCommand},
)
