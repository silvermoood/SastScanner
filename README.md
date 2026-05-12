# SAST Scanner

## Overview

SAST Scanner is a static application security testing (SAST) tool designed to analyze source code and identify potential security vulnerabilities and code quality issues during the development process.

The primary goal of this project is to assist developers in detecting weaknesses early, reducing risks, and improving overall software security and reliability.

---

## Key Features

* Static code analysis without execution
* Detection of common security vulnerabilities
* Identification of code quality issues and bad practices
* Fast and lightweight scanning process
* Extensible architecture for adding new rules and checks

---

## 1. Architecture Overview

Source Code
    ↓
AST Parser
    ↓
Pattern Analyzer
    ↓
Context Analyzer
    ↓
DataFlow Analyzer
    ↓
Severity Engine
    ↓
Findings Report

## 2. Detection Pipeline

1. Python source code is parsed into AST
2. Function calls and patterns are extracted
3. Security rules are matched
4. Context analysis reduces false positives
5. Dataflow analysis tracks tainted input
6. Severity engine calculates risk level
7. Findings are generated
