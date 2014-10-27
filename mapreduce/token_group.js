function(document, tokens) {
    for(token in document.sentiment.tokens){

        if(!tokens[document.sentiment.tokens[token]]){
            tokens[document.sentiment.tokens[token]] = 1
        } else {
            tokens[document.sentiment.tokens[token]]++
        }
    }
};