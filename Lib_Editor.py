import binascii
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def word_to_hex(word):
    """Convert a string (word) to its hex representation."""
    return binascii.hexlify(word.encode()).decode()

def replace_hex_in_file(input_file, output_file, search_word_hexes, search_words, replace_hexes):
    try:
        # Read the input file in binary mode
        with open(input_file, 'rb') as f:
            binary_data = f.read()

        # Convert the binary data to a hex string
        hex_data = binascii.hexlify(binary_data).decode()

        # Flag to check if any replacements were made
        any_replacements = False

        # Perform replacements for each word hex
        for search_word, search_word_hex, replace_hex in zip(search_words, search_word_hexes, replace_hexes):
            if search_word_hex in hex_data:
                hex_data = hex_data.replace(search_word_hex, replace_hex)
                print(f"{Fore.GREEN}Replaced '{Fore.YELLOW}{search_word}{Fore.GREEN}' => '{Fore.YELLOW}{search_word_hex}{Fore.GREEN}' with '{Fore.RED}{replace_hex}{Style.RESET_ALL}'")
                any_replacements = True
            else:
                print(f"{Fore.RED}'{search_word}' not found in the file.{Style.RESET_ALL}")

        # If no replacements were made, inform the user
        if not any_replacements:
            print(f"{Fore.YELLOW}No replacements made.{Style.RESET_ALL}")

        # Convert the modified hex data back to binary
        modified_binary_data = binascii.unhexlify(hex_data)

        # Write the modified binary data to the output file
        with open(output_file, 'wb') as f:
            f.write(modified_binary_data)

        print(f"{Fore.CYAN}Successfully modified the file {Fore.YELLOW}{input_file}{Fore.CYAN} and saved it as {Fore.YELLOW}{output_file}.{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

# Get input from the user
input_file = input(f"{Fore.CYAN}Enter the path to the lib file (e.g., libexample.so): {Style.RESET_ALL}")
output_file = input(f"{Fore.CYAN}Enter the output path for the modified file (e.g., libexample_modified.so): {Style.RESET_ALL}")
search_words = input(f"{Fore.CYAN}Enter the words to search for (comma-separated, e.g., ban, report, cheat): {Style.RESET_ALL}")

# Split the input into individual words
search_word_list = [word.strip() for word in search_words.split(',')]

# Convert each word to its hex representation
search_word_hexes = [word_to_hex(word) for word in search_word_list]

# Generate a hex string of zeros with the appropriate length for each word
replace_hexes = ["00" * (len(word_hex) // 2) for word_hex in search_word_hexes]

# Replace hex in the file
replace_hex_in_file(input_file, output_file, search_word_hexes, search_word_list, replace_hexes)