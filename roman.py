class Solution:
    def get_value(self, s: str) -> int:
        value_map = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
        }
        return value_map[s]

    def romanToInt(self, s: str) -> int:
        value_sum = 0
        element = [char for char in s]
        element.reverse()
        last_value = 0
        for char in element:
            value = self.get_value(char)
            if value >= last_value:
                value_sum += value
            else:
                value_sum -= value
            last_value = value
        return value_sum


if __name__ == '__main__':
    a = Solution()
    print(a.romanToInt('XIV'))

# I             1
# V             5
# X             10
# L             50
# C             100
# D             500
# M             1000
