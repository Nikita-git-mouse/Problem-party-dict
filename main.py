import spacy


nlp = spacy.load('en_core_web_sm')
sentence = "It is better to burn out than to FADE AWAY."
doc = nlp(sentence)

# Print the parse tree
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
            [child for child in token.children])
