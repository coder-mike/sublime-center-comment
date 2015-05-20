# Sublime Center Comment

A plugin for Sublime Text to center C/C++ style comments such this:

    // ----------------------------- Section Here -----------------------------

This also works for C-like languages such as C#, Java, and JavaScript.


## Installation

To install use Sublime Text Package Control.


## Usage

The default shortcut key is `ctrl+shift+c` or `super+shift+c`, and will center commented text on lines under the current cursor(s).

Here are some examples, showing first the line on which the command was executed, and then the result:

    // Padded with spaces
    //                            Padded with spaces

    // -Dashes
    // ---------------------------------Dashes---------------------------------

    // - Extra Space
    // ----------------------------- Extra Space -----------------------------

    //-No space
    //--------------------------------No space--------------------------------

    // = Equals
    // ================================ Equals ================================

    // * Asterisks
    // ****************************** Asterisks ******************************

    // -
    // ------------------------------------------------------------------------

    // = Multi -- Part
    // ============================ Multi -- Part ============================

    /* - C Style */
    /* ------------------------------ C Style ------------------------------ */



