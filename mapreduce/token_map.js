function() {
    if(this.sentiment.tokens){
        for(var i = 0; i < this.sentiment.tokens.length; i++){
            emit(this.sentiment.tokens[i], 1)
        }
    }
};