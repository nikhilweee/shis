import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shis",
    version="0.1",
    author="Nikhil Verma",
    author_email="nikhilweee@gmail.com",
    description="Simple HTTP Image Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nikhilweee/shis/",
    packages=setuptools.find_packages(),
    package_data={'shis': ['templates/*', 'templates/*/*']},
    license="MIT",
    install_requires=['Pillow>=7.0.0', 'Jinja2', 'tqdm', 'imagesize'],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://shis.readthedocs.io/',
        'Source': 'https://github.com/nikhilweee/shis/',
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Framework :: Sphinx",
        "Natural Language :: English",
        "Typing :: Typed"
    ]
)