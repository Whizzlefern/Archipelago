char_map = {
    "0": 0x00,
    "1": 0x01,
    "2": 0x02,
    "3": 0x03,
    "4": 0x04,
    "5": 0x05,
    "6": 0x06,
    "7": 0x07,
    "8": 0x08,
    "9": 0x09,
    "A": 0x0A,
    "B": 0x0B,
    "C": 0x0C,
    "D": 0x0D,
    "E": 0x0E,
    "F": 0x0F,
    "G": 0x10,
    "H": 0x11,
    "I": 0x12,
    "J": 0x13,
    "K": 0x14,
    "L": 0x15,
    "M": 0x16,
    "N": 0x17,
    "O": 0x18,
    "P": 0x19,
    "Q": 0x1A,
    "R": 0x1B,
    "S": 0x1C,
    "T": 0x1D,
    "U": 0x1E,
    "V": 0x1F,
    "W": 0x20,
    "X": 0x21,
    "Y": 0x22,
    "Z": 0x23,
    "a": 0x24,
    "b": 0x25,
    "c": 0x26,
    "d": 0x27,
    "e": 0x28,
    "f": 0x29,
    "g": 0x2A,
    "h": 0x2B,
    "i": 0x2C,
    "j": 0x2D,
    "k": 0x2E,
    "l": 0x2F,
    "m": 0x30,
    "n": 0x31,
    "o": 0x32,
    "p": 0x33,
    "q": 0x34,
    "r": 0x35,
    "s": 0x36,
    "t": 0x37,
    "u": 0x38,
    "v": 0x39,
    "w": 0x3A,
    "x": 0x3B,
    "y": 0x3C,
    "z": 0x3D,
    " ": 0x90,
    "%": 0x92,
    ";": 0x94,
    "'": 0x95,
    "「": 0x96,
    "」": 0x97,
    "?": 0x98,
    "!": 0x99,
    "-": 0x9C,
    "~": 0x9D,
    "/": 0x9E,
    "*": 0x9F,
    "(": 0xA0,
    ")": 0xA1,
    "+": 0xA2,
    ":": 0xA3,
    ",": 0xAB,
    ".": 0xB5,
    "&": 0xB6,
    "©": 0xB8
}

# 0x48-0x4F - blank
# 0x60-0x8C - blank
# 0xB9-0xCF - blank
special_chars = {
    "'s": 0x3E,
    "'m": 0x3F,
    "'r": 0x40,
    "'t": 0x41,
    "'v": 0x42,
    "'l": 0x43,
    "'d": 0x44,
    "*:": 0x45,
    "...": 0xA4,
    "<Book>": 0x50,
    "<Staff>": 0x51,
    "<???>": 0x52,
    "<Sword>": 0x53,
    "<Hourglass>": 0x54,
    "<Ring>": 0x55,
    "<Hat>": 0x56,
    "<House>": 0x57,
    "<Castle>": 0x58,
    "<Church>": 0x59,
    "<Cave>": 0x5A,
    "<Key>": 0x5B,
    "<World>": 0x5C,
    "<Tower>": 0x5D,
    "<Shield>": 0x5E,
    "<Lv>": 0xA5,
    "<Ex>": 0xA6,
    "<Male>": 0xA7,
    "<Female>": 0xA8,
    "<Up>": 0xA9,
    "<Quotation>": 0xAA,
    "<Star>": 0xAC,
    "<Down>": 0xAD,
    "<Left>": 0xAE,
    "<Right>": 0xAF,
    "<Up-Left>": 0xB0,
    "<Up-Right>": 0xB1,
    "<Down-Left>": 0xB2,
    "<Down-Right>": 0xB3,
    "<ZZ>": 0xB4,
    "..": 0x93
}

# "I": 0x46,
# "II": 0x47,
# close quotation marks?: 0x8D
# close star mark thing?: 0x8E
# thing that looks like like a period: 0x8F
# "<Cloud>": 0x91,
# weird period thing; 0x9A,
# dot thing?: 0x9b,
# weird "'" thing: 0xB7


def encode_text(text: str):
  encoded_text = bytearray()
  special = False
  symbol = False
  spec_char = ""
  
  for ind, char in enumerate(text):
    if special:
      if spec_char == "..":
        try:
          next_char = text[ind+1]
        except:
          encoded_text.append(special_chars[spec_char])
          special = False
          continue
        else:
          if next_char == ".":
            spec_char += char
            continue     
            
      encoded_text.append(special_chars[spec_char])
      special = False
      continue
    elif symbol:
      spec_char += char
      if char != ">":
        continue
      else:
        try:
          encoded_text.append(special_chars[spec_char])
        except:
          encoded_text.append(char_map[" "])
        finally:
          symbol = False
          continue
    
    if char in ["'", "*", ".", "<"]:
      try:
        next_char = text[ind+1]
      except:
          encoded_text.append(char_map[char])
      else:
        combined = char + next_char
        if combined in special_chars.keys():
          spec_char = combined
          special = True
        elif char == "<":
          spec_char = char
          symbol = True
        else:
          encoded_text.append(char_map[char])
    else:
      try:      
        encoded_text.append(char_map[char])
      except KeyError:
        raise KeyError(f"Invalid character in DQM2 script: '{char}'")
  print(", ".join(hex(b) for b in encoded_text))
  return encoded_text
