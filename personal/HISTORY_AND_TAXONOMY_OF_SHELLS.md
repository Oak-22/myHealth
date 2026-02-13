            
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


It starts with the Bourne shell (sh), written by Stephen Bourne in the late 1970s. This was the original Unix command interpreter and scripting language. Its syntax—pipelines, redirection, simple variables, control flow—became the foundation for almost every shell that followed. The original Bourne shell was proprietary and fairly minimal by modern standards.

As Unix spread and multiple vendors implemented their own Bourne-like shells, behavior began to diverge. To regain portability, POSIX sh was introduced—not as a new shell, but as a standardized specification describing a common, portable subset of Bourne-style shell behavior.  It does not describe advanced conveniences. Importantly, POSIX sh came after the Bourne shell and after early divergences; it is a contract, not an ancestor. POSIX sh defines what a script can rely on across systems, serving as a constraint layer applied to descendants, not a bourne-family shell branch itself.

From this base, several modern shells evolved:

Bash (Bourne Again SHell) is a free, open-source reimplementation of the Bourne shell created by the GNU project. The “again” is a pun, not a reversal. Bash conforms to POSIX sh when run in POSIX mode, but by default it extends POSIX with many additional features: arrays, [[ … ]] conditionals, brace expansion, arithmetic expressions, programmable completion, and more. Bash became the de facto standard shell on Linux systems for decades.

Zsh (Z shell) is another Bourne-family shell that also implements the POSIX baseline but diverges further in user-facing features and semantics. Zsh emphasizes powerful globbing, richer completion, spelling correction, and interactive ergonomics. It supports many bash-style extensions (including brace expansion) but also introduces behaviors that differ subtly, such as 1-indexed arrays by default. On modern macOS, zsh is the default interactive shell.

Other Bourne-derived shells exist as well, such as ksh (Korn shell), which influenced both bash and zsh, but they all share the same core ancestry.
