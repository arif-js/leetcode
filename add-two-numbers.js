/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} l1
 * @param {ListNode} l2
 * @return {ListNode}
 */
var addTwoNumbers = function(l1, l2) {
        let b = new ListNode();
        let division = 0;
        let i = 0;
        let head = new ListNode();

        while (l1 || l2 || division > 0) {
            let l1_val = l1 ? l1.val : 0;
            let l2_val = l2 ? l2.val : 0;
            let n = l1_val + l2_val + division
            division = 0

            if (n > 9)
                division = n / 10 >> 0  

            a = b
            a.val = n % 10 >> 0;
            if (i === 0) {
                head = a;
                i++;
            }

            l1 = l1 ? l1.next : null
            l2 = l2 ? l2.next : null

            if (l1 !== null || l2 !== null || division > 0) {
                b = new ListNode()
                a.next = b;
                continue;
            } 
            a.next = null;
            return head;
        }
};


// addTwoNumbers([8,6], [6,4,8])
