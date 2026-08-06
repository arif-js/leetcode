/**
 * @param {number[]} nums
 * @return {number[]}
 */
var distance = function(nums) {
    let count = {};
    let preSumCount = {};
    let i = 0;
    let arr = new Array(nums.length).fill(0);


    while (i < nums.length) {
        if (!count[nums[i]]) {
            count[nums[i]] = []
            preSumCount[nums[i]] = []
        }
        let ln = count[nums[i]].length;
        count[nums[i]][ln] = i;
        preSumCount[nums[i]][ln] = ln - 1 < 0 ? i : preSumCount[nums[i]][ln - 1] + i; 
        i++;
    }
    for (const [k, value] of Object.entries(count)) {
        if (value.length > 1) {
            for (l = 0; l < value.length; l++) {
                let sum1 = (l * count[k][l]) - (l-1 < 0 ? 0 : preSumCount[k][l-1]);
                let sum2 = (l + 1) < preSumCount[k].length ? (preSumCount[k][preSumCount[k].length - 1] - preSumCount[k][l]) - (count[k][l] * (preSumCount[k].length - l-1)) : 0;
                arr[count[k][l]] = sum1 + sum2;

                if (l === 2 ){
                    console.log(preSumCount[k][preSumCount[k].length - 1], count[k][l])
                }
            }
        }
    }

    return arr;
};
