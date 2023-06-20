% Facts for word to digit conversion
word(zero, 0).
word(one, 1).
word(two, 2).
word(three, 3).
word(four, 4).
word(five, 5).
word(six, 6).
word(seven, 7).
word(eight, 8).
word(nine, 9).
word(ten, 10).
word(eleven, 11).
word(twelve, 12).
word(thirteen, 13).
word(fourteen, 14).
word(fifteen, 15).
word(sixteen, 16).
word(seventeen, 17).
word(eighteen, 18).
word(nineteen, 19).
word(twenty, 20).
word(thirty, 30).
word(forty, 40).
word(fifty, 50).
word(sixty, 60).
word(seventy, 70).
word(eighty, 80).
word(ninety, 90).
word(hundred, 100).
word(thousand, 1000).

% Rule to convert a written number to digits
word_to_digit(WrittenNumber, Digits) :-
    atomic_list_concat(Words, ' ', WrittenNumber),  % Split the written number into individual words
    convert_words(Words, 0, Digits).  % Call the helper predicate to convert the words to digits

% Rule to convert a list of words to digits
convert_words([], N, N).  % Base case: if the list is empty, return the accumulated value as digits
convert_words([Word], N, Digits) :-
    word(Word, Digit),  % Lookup the numeric value associated with the word
    Digits is N + Digit.  % Add the value to the accumulated sum
convert_words([hundred | Rest], N, Digits) :-
    convert_words(Rest, N * 100, Digits).  % Multiply the accumulated sum by 100 (hundred multiplier)
convert_words([thousand | Rest], N, Digits) :-
    convert_words(Rest, N * 1000, Digits).  % Multiply the accumulated sum by 1000 (thousand multiplier)
convert_words([Word1, and, Word2 | Rest], N, Digits) :-
    word(Word1, Value1),  % Lookup the numeric value of the first word
    word(Word2, _),  % Ignore the value of the second word
    NewN is N + Value1,  % Add the value of the first word to the accumulated sum
    convert_words(Rest, NewN, Digits).  % Recursively process the remaining words
convert_words([Word1, Word2 | Rest], N, Digits) :-
    word(Word1, Value1),  % Lookup the numeric value of the first word
    word(Word2, _),  % Ignore the value of the second word
    NewN is N + Value1,  % Add the value of the first word to the accumulated sum
    convert_words([Word2 | Rest], NewN, Digits).  % Recursively process the remaining words
convert_words([Word1, Word2, Word3 | Rest], N, Digits) :-
    word(Word1, Value1),  % Lookup the numeric value of the first word
    word(Word2, Value2),  % Lookup the numeric value of the second word
    word(Word3, _),  % Ignore the value of the third word
    NewN is N + Value1 * 100 + Value2,  % Add the product of the first word and 100 to the accumulated sum, then add the value of the second word
    convert_words(Rest, NewN, Digits).  % Recursively process the remaining words
