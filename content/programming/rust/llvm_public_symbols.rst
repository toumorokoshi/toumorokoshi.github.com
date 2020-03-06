Using Rust functions in LLVM's JIT
===================================
:date: 2018-09-30
:category: programming
:tags: rust
:author: Yusuke Tsutsumi

`LLVM <http://llvm.org/>`_ is an amazing framework for building high-performance programming languages,
and Rust has some great bindings with `llvm-sys <https://crates.io/crates/llvm-sys>`_. One challenge
was getting functions authored in Rust exposed to LLVM. To make this happen, there's a few steps to walk through.

1. Exposing the Rust functions as C externs
*******************************************

When LLVM interfaces with shared libraries, it uses the C ABI protocol to do so. Rust provides a way to build do this, out of the box, using the 'extern "C"' declaration:

.. code-block:: rust

    extern "C" pub fn foo() {
      println!("foo");
    }

This instructs the Rust compiler that this should be exposed in a way where it can be found and used as a library. In the case of an executable binary, this is still the case.

The big gotcha here is ensuring that you are declaring the function as public, AND you are declaring it as public in the main module too. If the function was located in a child module, you will need to re-export in the main file:

.. code-block:: Rust

  // src/my_mod.rs

  extern "C" pub fn foo() {
    println!("I'm a shared library call");
  }

  // main.rs
  mod my_mod
  // note the pub here.
  pub use self::my_mod::foo;
