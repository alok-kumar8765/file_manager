<!-- ===================== -->
<!-- File Organizer README -->
<!-- ===================== -->

<p align="center">
  <img src="https://raw.githubusercontent.com/alok-kumar8765/file_manager/blob/main/unnamed.jpg" alt="File Organizer Banner" width="700"/>
</p>

# 📂 File Organizer

![Python Version](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-brightgreen)

> **Organize your files automatically and efficiently** – from basic sorting to advanced rules, undo, and logging.

---

## Table of Contents

<details>
<summary>Click to expand</summary>

1. [Introduction](#introduction)  
2. [Versions & Features](#versions--features)  
   - [v1 - Basic](#v1---basic)  
   - [v2.1 - Pro](#v21---pro)  
   - [v3 - Ultimate Pro](#v3---ultimate-pro)  
3. [Architecture & Diagrams](#architecture--diagrams)  
4. [Use Cases](#use-cases)  
5. [Pros and Cons](#pros-and-cons)  
6. [Installation](#installation)  
7. [Contribution](#contribution)  
8. [Support](#support)  
9. [License](#license)  

</details>

---

## Introduction

File Organizer is a Python-based **GUI application** for automatically organizing files on your system. It evolves from a **basic sorter** to a **professional, feature-rich mini file manager**.  

Features include **category sorting, recursive folder organization, file preview, selective moves, undo functionality, drag-and-drop support, and advanced rules based on date, size, and more**.

---

## Versions & Features

### v1 - Basic

<details>
<summary>Click to expand</summary>

**Description:**  
The first version of File Organizer allows users to **select a folder and automatically sort files by predefined categories**: Images, Docs, Videos, Audio, and Code.

**Key Features:**
- Select folder via GUI
- Sort files into predefined categories
- Recursive support not included
- Status updates

**Pros:**
- Simple and lightweight
- Easy to use

**Cons:**
- No undo functionality
- Cannot customize categories or extensions
- No progress feedback

**Real-Life Example:**  
Organize your "Downloads" folder into Images, Documents, and Videos in one click.

</details>

---

### v2.1 - Pro

<details>
<summary>Click to expand</summary>

**Description:**  
The Pro version introduces **multi-level undo, file preview, selective move, recursive sorting, and customizable categories**. Now users can have more control over organization.

**Key Features:**
- Multi-level undo
- File preview and selective move
- Drag-and-drop folder selection
- Recursive folder sorting
- Customizable categories and extensions
- Progress bar and status updates

**Pros:**
- More control and safety
- Flexible customization
- Suitable for large directories

**Cons:**
- Slightly heavier than v1
- Requires GUI familiarity

**Real-Life Example:**  
Sort a project folder while previewing which files to move, and undo if needed.

</details>

---

### v3 - Ultimate Pro

<details>
<summary>Click to expand</summary>

**Description:**  
Ultimate Pro adds **advanced rules, filtering, permanent logs, and dark/light theme support**. It is ideal for professional use.

**Key Features:**
- Organize files by category, date, or size
- Search/filter files by extension or modification date
- Multi-level undo
- File preview & selective move
- Dark/light theme toggle
- Drag-and-drop folder selection
- Permanent logging of all file moves
- Progress bar and status updates

**Pros:**
- Powerful professional organizer
- Flexible rules and filters
- Persistent logs for tracking
- User-friendly GUI

**Cons:**
- Heavier than previous versions
- Requires Python and dependencies installed

**Real-Life Example:**  
Organize thousands of downloaded files into date-based folders while keeping a log for reference.

</details>

---

## Architecture & Diagrams

<details>
<summary>Click to expand</summary>

### Architecture Overview

```text
+--------------------+
|  File Organizer GUI|
|  (Tkinter)         |
+---------+----------+
          |
          v
+--------------------+
| File Handling      |
| - Sorting          |
| - Moving           |
| - Undo             |
+---------+----------+
          |
          v
+--------------------+
| Logging & Rules    |
| - Category rules   |
| - Date/Size rules  |
| - Persistent logs  |
+--------------------+
