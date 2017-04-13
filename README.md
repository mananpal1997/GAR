# GAR(Gmail Addresses Retriever)
A python command line utility to retrieve unknown valid gmail address in bulk, based on recent enumeration attack leak by x0rz - https://blog.0day.rocks/abusing-gmail-to-get-previously-unlisted-e-mail-addresses-41544b62b2

# TODO
Create a simple GUI that takes certain information on a user, and tries to find it's gmail address by brute-forcing different combinations of the data provided.

# Usage
```python main.py --filters [.,(97;1997)] --fname_path sample/firstnames.txt --lname_path sample/lastnames.txt```

(97;1997) means either the email can have permutations of 97 at end, or permutations of 1997 at end. Useful in case of getting email address of persons born in year 1997. They usually have their email-id like xyz97@gmail.com or xyz1997@gmail.com
