# Correction: Python 2 .has_key() to Python 3 'in' operator

# ============================================
# LEARNED CORRECTION REFERENCE
# ============================================

"""
This file stores a learned correction pattern.
When this error occurs again, the processor can reference this solution.

PATTERN ID: has_key_to_in_operator
ERROR TYPE: AttributeError - 'dict' object has no attribute 'has_key'
PYTHON ISSUE: Python 2 to Python 3 migration
"""

# ============================================
# BROKEN CODE (Python 2 style)
# ============================================

# if config_dict.has_key("gateway"):
#     print("Gateway found")
#
# Why it breaks:
# - .has_key() method was removed in Python 3.0
# - Current runtime is Python 3
# - Result: AttributeError


# ============================================
# CORRECTED CODE (Python 3 style)
# ============================================

# Test dictionary
config_dict = {
    "gateway": "1.1.1.1",
    "port": 53,
    "timeout": 3.0
}

# Correct way to check dictionary keys in Python 3
if "gateway" in config_dict:
    print("Gateway found in configuration")
else:
    print("Gateway not found")

# Verify other keys
if "port" in config_dict:
    print(f"Port configured: {config_dict['port']}")

if "timeout" in config_dict:
    print(f"Timeout configured: {config_dict['timeout']}")


# ============================================
# WHY THIS WORKS
# ============================================

"""
The 'in' operator checks if a key exists in a dictionary.

Advantages:
1. Standard Python 3 method
2. More readable than .has_key()
3. More efficient (faster lookup)
4. Works across all Python 3 versions (3.0 through 3.12+)
5. Pythonic and idiomatic

Syntax:
    if key_name in dictionary:
        # key exists
    else:
        # key does not exist
"""


# ============================================
# REFERENCE PATTERN
# ============================================

def demonstrate_correction_pattern():
    """
    Shows the general pattern for replacing .has_key() with 'in' operator
    """
    
    # Any dictionary
    my_dict = {"a": 1, "b": 2, "c": 3}
    
    # OLD (Python 2 - BROKEN):
    # if my_dict.has_key("a"):
    #     do_something()
    
    # NEW (Python 3 - CORRECT):
    if "a" in my_dict:
        print("Key 'a' exists")
    
    # Can also check non-existence
    if "z" not in my_dict:
        print("Key 'z' does not exist")
    
    return True


if __name__ == "__main__":
    print("Demonstrating the corrected pattern...\n")
    demonstrate_correction_pattern()
