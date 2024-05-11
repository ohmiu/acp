# Advanced Cross-Platform Packager


Advanced cross-platform packer is a software for creating user-friendly packages for different operating systems with built-in data compression. The acp project uses only native libraries.

These systems are currently supported:

`Windows` - tested on Windows 10 x64

`Linux` - untested

`MacOS / Darwin` - untested

Usage:

`./acp blank` - Create an empty package project in this directory

`./acp build` - Build the package in the current directory

`./acp install <package.acpe>` - Install the package from the file

`./acp all` - Add all files in all folders in the "." directory to package.json

### Warning
It is not possible to write too much data into a packet due to technical reasons, which may be fixed in the future.
