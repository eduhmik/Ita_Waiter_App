def validate_password(pwd):
    validated_password = []
    for p in pwd:
        special_chars = ['$','#','@']
        isupper = 0
        islower = 0
        isdigit = 0
        hasSpecialChar = 0

        for char in p:
            if char.isdigit():
                isdigit += 1
            elif char.islower():
                islower += 1
            elif char.isupper():
                isupper += 1
            elif char in special_chars:
                hasSpecialChar += 1
            else:
                pass

            if len(p) in  range(6,13) and isdigit >= 1 and islower >= 1 and isupper >= 1 and hasSpecialChar >=1:
                validated_password.append(p)
    return validated_password

print(validate_password(['ABd1234@1','a F1#','2w3E*','2We3345']))

