import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Djangogramm',  # Replace with your own username
    version='0.0.1',
    author="Maksim Shavrin",
    author_email="nutmegraw@gmail.com",
    description="Social network like the Instagramm.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/orahmudri/task-12-create-basic-application",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Environment :: Web',
        'Intended Audience :: Education',
        'License :: Freeware',
        'Natural Language :: English',
    ],
    python_requires='>=3.6',
)
