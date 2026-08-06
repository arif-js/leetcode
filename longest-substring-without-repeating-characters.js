var lengthOfLongestSubstring = function(s) {
    var longestLength = 0;
    var strLen = s.length;
    var start = 0;
    var subLength = 0;
    var mappings = {};

    for (let i = 0; i < strLen; i++) {
        while (mappings[s[i]] > 0 && start <= start + 100) {
            if (s[start] === s[i]) {
                subLength = s.slice(start+1, i).length;
            }
            mappings[s[start]]--;
            start++;
        }
        mappings[s[i]] = mappings[s[i]] ? mappings[s[i]] + 1 : 1
        subLength++;

        if (subLength > longestLength) {
            longestLength = subLength;
        }
        if (longestLength === strLen) break;
    }

    return longestLength;
};
