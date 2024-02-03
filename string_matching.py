import tkinter as tk
from smartcart import SmartCart

class StringMatching:
   @staticmethod
   def search_products(search_term, product_data):  # Search products with name matching
       # Build list of matches using KMP algorithm
       matches = [product[0] for product in product_data if StringMatching.match_product(search_term, product[0])]
       return matches

   @staticmethod
   def match_product(search_term, product_name):  # Check if product name matches search term
       # Converts both product name and search term to lower case
       return StringMatching.kmp_search(search_term.lower(), product_name.lower()) 

   @staticmethod
   def kmp_search(pattern, text):  # KMP string matching algorithm
       m, n = len(pattern), len(text)
       lps = StringMatching.compute_lps(pattern)  # Compute longest proper prefix array

       i, j = 0, 0  # Initialize indexes for text and pattern
       matches = []  # Initialize list of matches

       while i < n:  # Loop through text
           if pattern[j] == text[i]:  # If characters match
               i += 1  # Move to next character in text
               j += 1  # Move to next character in pattern

               if j == m:  # If end of pattern is reached
                   matches.append(text[i - j:i])  # Add match to list
                   j = lps[j - 1]  # Move to next possible match

           else:  # If characters don't match
               if j != 0:  # If not at beginning of pattern
                   j = lps[j - 1]  # Move to next possible match

       return matches  # Return list of matches

   @staticmethod
   def compute_lps(pattern):  # Compute longest proper prefix array for KMP algorithm
       m = len(pattern)
       lps = [0] * m
       j = 0

       i = 1
       while i < m:
           if pattern[i] == pattern[j]:
               lps[i] = j + 1
               i += 1
               j += 1
           elif j != 0:
               j = lps[j - 1]
           else:
               lps[i] = 0
               i += 1

       return lps

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCart(root)
    root.mainloop()
