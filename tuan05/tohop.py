import sys
from itertools import combinations

def generate_combinations(n, k, elements):
    """Generate all combinations of k elements from n elements"""
    if k > n:
        return []
    return list(combinations(elements[:n], k))

def read_from_file(filename):
    """Read n, k, and elements from file"""
    with open(filename, 'r') as f:
        first_line = f.readline().strip().split()
        if len(first_line) < 2:
            raise ValueError(f"File format error: Expected 'n k' on first line, got '{first_line}'")
        n = int(first_line[0])
        k = int(first_line[1])
        
        elements = []
        for line in f:
            element = line.strip()
            if element:
                elements.append(element)
    
    return n, k, elements

def print_combinations(combos):
    """Print combinations in formatted way"""
    print(f"Kết quả:")
    print(len(combos))
    for combo in combos:
        print(" ".join(combo))

def test1():
    """Test with sample data"""
    print("----- DOC FILE -----")
    n = 5
    k = 3
    th = ['A', 'B', 'C', 'D', 'E']
    print(f"n = {n}, k = {k}, th = {th}")
    combos = generate_combinations(n, k, th)
    print_combinations(combos)

def main():
    """Main function to process command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python tohop.py [--action test1|main] [--file filename]")
        return
    
    action = None
    filename = None
    
    # Parse arguments
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--action' and i + 1 < len(sys.argv):
            action = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--file' and i + 1 < len(sys.argv):
            filename = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if action == 'test1':
        test1()
    elif action == 'main' and filename:
        print("----- DOC FILE -----")
        n, k, elements = read_from_file(filename)
        print(f"n = {n}, k = {k}, th = {elements}")
        combos = generate_combinations(n, k, elements)
        print_combinations(combos)

if __name__ == '__main__':
    main()
