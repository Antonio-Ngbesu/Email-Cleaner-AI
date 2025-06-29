from setuptools import setup, find_packages

setup(
    name='email-cleaner-ai',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='An AI agent tool that cleans up unnecessary emails to free up space.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'some-email-library',  # Replace with actual email handling library
        'some-ai-library'      # Replace with actual AI library
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)