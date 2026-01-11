const calc = (a, b, p) => {
    if (a === undefined || b === undefined || p === undefined) {
        return "Please provide all parameters";
    }
    switch (p) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return a / b;
        default: return "Invalid operator";
    }
};
exports.calc = calc; //very important line
var dt = require('./mymodule');
console.log(dt.calc(10,20,'+'));
console.log(dt.calc(10,20,'-'));
console.log(dt.calc(10,20,'*'));