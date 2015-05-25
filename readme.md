# Sublime Center Comment

A plugin for Sublime Text to center comments like this:

    // ----------------------------- Section Here -----------------------------


This is particularly useful for headings and sections in code.


## Installation

To install use Sublime Text [Package Control](https://sublime.wbond.net/).


## Usage

The default shortcut key is `ctrl+shift+c` or `super+shift+c`, and will center commented text on lines under the current cursor(s).

Here are some examples in a C-like language such as C#, Java, and JavaScript, but this should work for other languages as well. Each example shows what it looks like before and after using the command:

    // Padded with spaces
    //                            Padded with spaces

    // -Dashes
    // --------------------------------Dashes---------------------------------

    // - Extra Space
    // ----------------------------- Extra Space -----------------------------

    //-No space
    //--------------------------------No space--------------------------------

    // = Equals
    // =============================== Equals ================================

    // * Asterisks
    // ****************************** Asterisks ******************************

    // -
    // -----------------------------------------------------------------------

    // = Multi -- Part
    // ============================ Multi -- Part ============================

    /* - Single-line block comment */
    /* -------------------- Single-line block comment --------------------- */



