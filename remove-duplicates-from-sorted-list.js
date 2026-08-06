/**
 * Definition for singly-linked list.
 * function ListNode(val, next) {
 *     this.val = (val===undefined ? 0 : val)
 *     this.next = (next===undefined ? null : next)
 * }
 */
/**
 * @param {ListNode} head
 * @return {ListNode}
 */
var deleteDuplicates = function(head) {

    if (head === null) return head;
    let tempHead = head.next;
    let prevNode = head;
    
    while (tempHead !== null) {
        if (tempHead.val === prevNode.val) {
            prevNode.next = tempHead.next;
        } else {
            prevNode = tempHead;
        }
        tempHead = tempHead.next;
    }

    return head;
};
