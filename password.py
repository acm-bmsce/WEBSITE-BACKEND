import urllib.parse

# REPLACE THIS with your actual password
raw_password = "Bmsce@2025" 

escaped_password = urllib.parse.quote_plus(raw_password)
print(f"Your safe password is: {escaped_password}")