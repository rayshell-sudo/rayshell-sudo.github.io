//Create a random number generator

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