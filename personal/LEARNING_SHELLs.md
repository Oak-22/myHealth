# Shell Learning Notes


## What Is a Shell?

A shell is a user-space command-line interpreter that acts as an interface between the user and the operating system kernel using systems calls. It reads text-based commands, interprets them according to its grammar rules, and executes programs or built-in operations, serving as an orchestrator of system-level tasks/processes. The shell is not the operating system itself — it is a user-space program that launches other programs. It excels at launching programs, connecting programs (pipes), redirection IO, iterating over files, environment manipulation, and automation glue. It's "thin" and OS-centric

At a high level, the shell performs:

1. Command parsing (understanding syntax)
2. Expansion (globbing, variable expansion, substitution)
3. Redirection (stdin, stdout, stderr handling)
4. Process control (forking, backgrounding, pipelines)
5. Execution (running built-ins or external binaries)

---

## Kernel vs Shell vs Programs

- Kernel → Core of the operating system (manages memory, CPU, filesystem, devices)
- Shell → User-facing command-line interpreter that sends instructions to the kernel
- Programs → Executables launched by the shell (e.g., `ls`, `grep`, `python`)

When you type a command like:

```
ls -l
```

The shell:
1. Parses `ls` as a command
2. Parses `-l` as an argument
3. Searches `$PATH` for the `ls` binary
4. Asks the kernel to execute it
5. Handles its output

---

## Interactive vs Non-Interactive Shells

Interactive Shell:
- Accepts user input in real time
- Displays prompts
- Reads configuration files (e.g., `.zshrc`, `.bashrc`)
- Used during terminal sessions

Non-Interactive Shell:
- Executes scripts
- May skip certain startup files
- Often runs in automation (cron, CI/CD, system scripts)

---

## Login Shell vs Non-Login Shell

Login Shell:
- Starts when you log into a system (SSH, console login)
- Reads login configuration files (e.g., `.profile`, `.bash_profile`)

Non-Login Shell:
- Started from within an existing session
- Typically reads `.bashrc` or `.zshrc`

Important: Login behavior affects environment variables and PATH configuration.

---

## What Happens When You Run a Script?

If a script begins with:

```
#!/bin/sh
```

The operating system:
1. Reads the shebang line
2. Launches the specified interpreter (`/bin/sh`)
3. Passes the script file to that interpreter

The script does NOT automatically run in your current interactive shell unless you explicitly invoke it that way.

---

## The POSIX Standard

POSIX is a specification that defines a portable subset of shell behavior. It ensures scripts behave consistently across compliant systems.

POSIX defines:
- Basic grammar
- Built-in commands
- Parameter expansion rules
- Redirection syntax

Shells like `bash` and `zsh` extend POSIX with additional features. Writing POSIX-compliant scripts maximizes portability.

---

## Builtins vs External Commands

Builtins:
- Implemented inside the shell process
- Examples: `cd`, `echo`, `export`, `exit`
- Faster (no new process required)

External Commands:
- Separate executable files
- Found via `$PATH`
- Examples: `ls`, `grep`, `sed`

---

## Process Model

The shell creates new processes using fork/exec:

- fork() → duplicates the current process
- exec() → replaces the process with a new program

Pipelines:

```
ls | grep txt
```

The shell creates two processes and connects stdout of the first to stdin of the second.

---

## Environment Variables

Environment variables store configuration values inherited by child processes.

Examples:

```
echo $HOME
echo $PATH
```

Exporting makes variables available to child processes:

```
export MY_VAR=value
```

---

## Expansion Order (Critical Concept)

Before executing a command, the shell performs expansions in order:

1. Brace expansion (bash/zsh feature)
2. Tilde expansion
3. Parameter expansion
4. Command substitution
5. Arithmetic expansion
6. Word splitting
7. Globbing (wildcard expansion)

Understanding expansion order explains many shell “gotchas.”

---

## Shell Ecosystem Overview

Shells exist in a lineage:

- Bourne Shell (sh)
- POSIX sh (standardized behavior)
- ksh (Korn shell)
- bash (Bourne Again Shell)
- zsh (extended interactive shell)
- fish (independent design)

Interactive shells prioritize usability.
Script shells prioritize portability and predictability.

---

## Practical Strategy

- Use zsh or bash interactively for productivity.
- Use POSIX-compliant syntax in portable scripts.
- Explicitly declare bash in scripts when using bash-specific features:

```
#!/usr/bin/env bash
```

Shebang determines execution interpreter. Interactive shell determines your session environment.

---

Types of shells

	•	Login shell = how your session begins
	•	Interactive shell = the shell process currently handling your commands
	•	Shebang shell = the interpreter chosen to execute a script file




## Flags & Options

### `-a` flag (files)
Lists all files, including hidden ones starting with `.`

### `-l` flag (long format)
Detailed list view with permissions, owner, size, date

### `-h` flag (human-readable format)
Formats content with less machine-interpreted characters/symbols


            Bourne shell (sh)
                    |
               POSIX sh (spec)
                    |
        --------------------------------
        |                              |
      ksh                            bash
                                        |
                                       zsh
                                        
         (separate branch: fish)

## xxx

### `grep` 
Global Regular Expression Print
It searches text line-by-line for lines matching a pattern, then prints matching lines to output.
Global - search all files in the filesystem
Regular Expression - Pattern matching (wildcards, character classes, etc.)
Print - output matching lines


## Redirection

| Symbol | Meaning |
|--------|---------|
| `>` | Redirect stdout to file (overwrite) |
| `>>` | Append stdout to file |
| `2>` | Redirect stderr |


## Common Commands

- `grep -i pattern file` → case-insensitive search
    Ex: - `grep --color=auto -iw 'the' *.txt` → case insensitive search for all .txt files in current directory containing the string 'the' with the pattern text highlighted

- `sed 's/old/new/g' file` → global replace






