import shutil
import subprocess
import sys
import os
import gym_retro
from setuptools import setup
from setuptools.command.build_ext import build_ext

# Import the game ROM
# Ensure the path is correct (use raw string for Windows paths)
rom_path = r'C:\Users\yoshi.DESKTOP-A29FSN9\PycharmProjects\ReinforcementGamingLearning\roms\Final Fantasy Tactics Advance (Europe) (En,Fr,De,Es,It).gba'
gym_retro.data.import_game(rom_path)

class BuildExt(build_ext):
    def run(self):
        # Find the correct compiler for PyCharm or system
        cmake_exe = shutil.which('cmake')
        if cmake_exe is None:
            raise RuntimeError('CMake is not found. Please install CMake and ensure it is in the PATH.')

        # Check if we're using MinGW or MSVC for the compiler
        compiler = os.environ.get('CXX', None)

        # Set the build type (Release or Debug)
        build_type = "Release"  # Change this to "Debug" if needed

        # Define paths related to the Python environment
        python_executable = sys.executable
        pyext_suffix = ".pyd"  # Windows extension suffix for Python
        pylib_dir = os.path.join(self.build_lib, "pyext")

        # Build CMake command using MinGW (for non-MSVC systems)
        cmake_command = [
            cmake_exe, '.', '-G', 'MinGW Makefiles', f'-DCMAKE_BUILD_TYPE={build_type}',
            f'-DPYEXT_SUFFIX={pyext_suffix}', f'-DPYLIB_DIRECTORY={pylib_dir}', f'-DPYTHON_EXECUTABLE={python_executable}'
        ]

        # If MSVC is detected, modify the CMake command for MSVC
        if compiler and "MSVC" in compiler:
            cmake_command = [
                cmake_exe, '.', '-G', 'Visual Studio 16 2019', f'-DCMAKE_BUILD_TYPE={build_type}',
                f'-DPYEXT_SUFFIX={pyext_suffix}', f'-DPYLIB_DIRECTORY={pylib_dir}', f'-DPYTHON_EXECUTABLE={python_executable}'
            ]

        # Run the CMake command to configure and build the extension
        subprocess.check_call(cmake_command)

        # Call the parent class's run method to continue the setup process
        super().run()


# Running the setup function with the custom build_ext command
setup(
    name="gym-retro",
    version="1.0",
    description="Gym Retro integration",
    packages=["gym_retro"],
    ext_modules=[],
    cmdclass={'build_ext': BuildExt},  # Override build_ext with custom logic
)
