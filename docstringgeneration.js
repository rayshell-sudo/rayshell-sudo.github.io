//Create a random number generator
//This function generates a random integer between the specified minimum and maximum values. The minimum value is inclusive, while the maximum value is exclusive. The function uses the Math.random() method to generate a random decimal number between 0 (inclusive) and 1 (exclusive), which is then scaled and shifted to fit the desired range of integers.
function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
/**
 * Generates a random integer between the specified minimum and maximum values.
 *
 * @param {number} min - The lower bound of the range (inclusive).
 * @param {number} max - The upper bound of the range (exclusive).
 * @returns {number} A random integer between min and max.
 */
}