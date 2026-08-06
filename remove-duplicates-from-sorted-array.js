/**
 * @param {number[]} nums
 * @return {number}
 */
var removeDuplicates = function(nums) {
    let d = 0;
    let currentIndex = 1;
    let numsLength = nums.length;
    if (numsLength === 0) return numsLength;

    for (let i = 1; i < nums.length; i++) {
        if (nums[i] !== nums[currentIndex-1]) {
            nums[currentIndex] = nums[i];
            currentIndex++;
        }
    }

    return currentIndex;
};
