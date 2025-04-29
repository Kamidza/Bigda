from typing import List


def find_maximal_subarray_sum(nums: List[int], k: int) -> int:
    max_sum = float('-inf')
    n = len(nums)

    for size in range(1, k + 1):
        current_sum = sum(nums[:size])
        max_sum = max(max_sum, current_sum)

        for i in range(size, n):
            current_sum += nums[i] - nums[i - size]
            max_sum = max(max_sum, current_sum)

    return max_sum