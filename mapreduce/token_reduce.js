function(token, values) {
    var count = 0;
    values.forEach(function(v) {
        count += v;
    });
    return count;
};