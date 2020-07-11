import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lumber_data", # Replace with your own username
    version="0.0.1",
    author="CG Lumberjack, Inc.",
    author_email="tom@cglumberjack.com",
    description="Convenience Package for gathering meta-data for all types of files (images, videos, audio)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cglumberjack/cgl_metadata",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)