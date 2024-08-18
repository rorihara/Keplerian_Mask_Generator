from setuptools import setup, find_packages

setup(
    name="KeplerianMaskGenerator",
    version="1.0.0",
    packages=["KeplerianMaskGenerator"],
    install_requires=[
        'numpy',
        'matplotlib',
        'astropy',
        'opencv-python'
    ],
    author="Ryuta Orihara",
    author_email="roriharaiba@gmail.com",
    description="Tool for generating Keplerian mask",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)
