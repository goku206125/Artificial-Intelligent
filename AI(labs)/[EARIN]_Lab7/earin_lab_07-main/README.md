# Word to Digit Conversion in Prolog

This Prolog program allows you to convert written numbers into their corresponding digit representation.

## Prerequisites

Make sure you have Prolog installed on your system. You can download and install Prolog from the official website: [Prolog Downloads](https://www.swi-prolog.org/Download.html)

## Usage

1. Open your Prolog interpreter or IDE.

2. Load the Prolog file containing the conversion rules. For example, if the file is named `word_to_digit.pl`, you can load it using the `consult/1` predicate:

   ```prolog
   ?- consult('word_to_digit.pl').
3. Once the file is loaded, you can start converting written numbers to digits by using the 
    `word_to_digit/2` predicate. Pass the written number as a string and a variable to store 
    the resulting digits. 
    For example:
                ?- word_to_digit("eight hundred thirty six", Digits).
        This query will convert the written number "eight hundred thirty six" to its digit 
        representation and bind the result to the variable Digits. The output will be 
         displayed on the screen.

        You can also use specific written numbers or variables to perform the conversion:
        ?- word_to_digit("two hundred  fifty", Digits).
        ?- word_to_digit("one thousand twenty", Digits).
        ?- word_to_digit("sixty nine", 69).



## Here's an example of running the program:
    ?- consult('word_to_digit.pl').
    true.

    ?- word_to_digit("eight hundred thirty six", Digits).
    Digits = 836.

    ?- word_to_digit("two hundred fifty", Digits).
    Digits = 250.

    ?- word_to_digit('zero', Digits).
    Digits = 0.

    ?- word_to_digit('five', Digits).
    Digits = 5.

    ?- word_to_digit('twenty', Digits).
    Digits = 20.

    ?- word_to_digit('twenty five', Digits).
    Digits = 25.

    ?- word_to_digit('ninety three', Digits).
    Digits = 93.

    ?- word_to_digit('eighty four', Digits).
    Digits = 84.

    ?- word_to_digit('three hundred', Digits).
    Digits = 300.

    ?- word_to_digit('seven hundred fifty', Digits).
    Digits = 750.

    ?- word_to_digit('nine hundred forty two', Digits).
    Digits = 942.

