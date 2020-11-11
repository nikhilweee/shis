import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shis",
    version="0.0.7",
    author="Nikhil Verma",
    author_email="nikhilweee@gmail.com",
    description="Simple HTTP Image Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikhilweee/shis",
    packages=setuptools.find_packages(),
    package_data={'shis': ['templates/*', 'templates/*/*']},
    license="MIT",
    install_requires=['Pillow', 'Jinja2', 'tqdm'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing"
    ]
)