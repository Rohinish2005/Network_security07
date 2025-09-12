def shift_encrypt(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            shift = 65 if char.isupper() else 97
            result += chr((ord(char) - shift + key) % 26 + shift)
        else:
            result += char
    return result

def shift_decrypt(text, key):
    return shift_encrypt(text, -key)


# Function for Vigenere Cipher
def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 97
            if char.isupper():
                result += chr((ord(char) - 65 + shift) % 26 + 65)
            else:
                result += chr((ord(char) - 97 + shift) % 26 + 97)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 97
            if char.isupper():
                result += chr((ord(char) - 65 - shift) % 26 + 65)
            else:
                result += chr((ord(char) - 97 - shift) % 26 + 97)
            key_index += 1
        else:
            result += char
    return result


# Main Program
def main():
    filename = "data.txt"

    # Step 1: Input data and write to file
    user_data = input("Enter some text: ")
    with open(filename, "w") as f:
        f.write(user_data)

    # Step 2: Read data from file
    with open(filename, "r") as f:
        data = f.read()
    print("\nOriginal Data from file:", data)

    # Step 3: Choose cipher
    choice = int(input("\nChoose cipher:\n1. Shift Cipher\n2. Vigenere Cipher\nEnter choice: "))

    if choice == 1:
        shift_key = 3
        encrypted = shift_encrypt(data, shift_key)
        decrypted = shift_decrypt(encrypted, shift_key)

        print("\n--- Shift Cipher ---")
        print("Encrypted:", encrypted)
        print("Decrypted:", decrypted)

    elif choice == 2:
        vigenere_key = "KEY"
        encrypted = vigenere_encrypt(data, vigenere_key)
        decrypted = vigenere_decrypt(encrypted, vigenere_key)

        print("\n--- Vigenere Cipher ---")
        print("Encrypted:", encrypted)
        print("Decrypted:", decrypted)

    else:
        print("Invalid choice! Please select 1 or 2.")


if __name__ == "__main__":
    main()
