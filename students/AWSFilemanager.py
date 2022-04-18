import os



def checkfiletype(file,valid_extensions):
    if not os.path.splitext(file.name)[1] in valid_extensions:
        return "invalid format"
    else:
        return "valid format"