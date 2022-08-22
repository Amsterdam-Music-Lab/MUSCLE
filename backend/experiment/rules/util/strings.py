# Convert regular spaces to non breaking spacing 
# on the given string
def non_breaking(s):
    non_breaking_space=chr(160)
    return s.replace(" ", non_breaking_space)