from setuptools import setup

setup(name='video_collage',
      version='0.1',
      description='Dynamically record and generate video from tiled sub-videos.',
      url='https://github.com/aaronvd/video_collage',
      author='Aaron V. Diebold',
      author_email='diebolav@gmail.com',
      license='MIT',
      packages=['video_collage'],
      zip_safe=False,
      install_requires=[
            'numpy==1.21.2',
            'opencv==4.0.1',
            'pyqt==5.9.2'
      ])






