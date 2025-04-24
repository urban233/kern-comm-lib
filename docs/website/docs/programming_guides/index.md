# Introduction

This documentation serves as a companion to the comments within the Kern Python source files, providing a comprehensive overview of the library's functionality and usage. Over time, it will evolve to include detailed examples and documentation for all code within the Kern project.

## Core Concepts

This guide is designed for developers new to the Kern project. 
The primary objective of Kern is to provide a toolset for building robust Python programs that operate without exceptions. 
To achieve this goal, Kern offers several key components:

- The `Status` and `StatusOr` classes, which facilitate communication between functions and methods
- A custom decorator called `@use_status` that simplifies the use of `Status` and `StatusOr` for existing code
- A custom type called `AStatusOrElse`, which enables the communication of a value or a status object to the caller

Currently, Kern also provides:

- A custom wrapper implementation for the `pathlib.Path` class, called `KPath`, which operates without exceptions
- A logger that supports console and file handlers, is exception-free, and can function in multithreaded environments

These components work together to help developers build reliable and efficient Python programs using the Kern library.
The kern library draws inspiration from the C++ library [abseil](https://abseil.io/), which is designed to provide a set of common libraries and tools for C++ developers
and [GLog](https://google.github.io/glog/stable/) which is a C++ logging library that provides a simple and efficient way to log messages from C++ applications.