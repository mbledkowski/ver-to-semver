import re


def toSemVer(version):
    # Remove anything in brackets
    version = re.sub(r"(\[.*\])|(\(.*\))", "", version).strip()

    # Remove v, ver and version prefixes
    version = re.sub(r"(^|\n| )[vV](|er|ersion)[-_*\\/!~@#$=.]?", "", version)

    # Replace strings starting with prerelease / beta / alpha with zeros
    version = re.sub(
        r"(^|\n| )([pP](re( )?[rR]elease)|[aA]lpha|PRE( )?RELEASE|ALPHA)[-_*\\/!~@#$=. ]?(?:\d+[._-]{0,2}(\d+))",
        r"0.0.",
        version,
    )
    version = re.sub(
        r"(^|\n| )([bB]eta|BETA|[bB]uild|BUILD)[-_*/!~@#$=. ]?(?:\d+[._-]){0,3}(\d+)",
        r"0.",
        version,
    )

    # Remove anything that starts with a word character
    version = re.sub(r"(^|\n| )[a-uw-zA-UW-Z][\w\d\.\-]*", "", version).strip()

    version = version.split(" ")[0]

    versionWithoutBuildMetadata, *buildMetadata = version.split("+")
    (
        versionWithoutPreReleaseAndBuildMetadata,
        *preRelease,
    ) = re.split("-|_", versionWithoutBuildMetadata)

    default_value = None
    x = versionWithoutPreReleaseAndBuildMetadata.split(".")
    major, minor, patch, *otherNumbers = [*x, *([default_value] * (3 - len(x)))]

    def destileAnyCharacters(x):
        if x is None:
            return [None, None]
        else:
            return [re.sub(r"[^0-9\s]", "", x), re.sub(r"[^a-zA-Z]", "", x)]

    major, majorstr = destileAnyCharacters(major)
    minor, minorstr = destileAnyCharacters(minor)
    patch, patchstr = destileAnyCharacters(patch)

    result = f'{int((major or "0").strip())}.{int((minor or "0").strip())}.{int((patch or "0").strip())}'

    strings_to_add = []
    if majorstr:
        strings_to_add.append(majorstr)
    if minorstr:
        strings_to_add.append(minorstr)
    if patchstr:
        strings_to_add.append(patchstr)

    if strings_to_add:
        result += f'-{"-".join(strings_to_add)}'

    if len(otherNumbers) > 0:
        result += f'-{".".join(otherNumbers)}'

    if len(preRelease) > 0:
        result += f'-{"-".join(preRelease)}'

    if len(buildMetadata) > 0:
        result += f'+{"+".join(buildMetadata)}'

    return result


if __name__ == "__main__":
    while True:
        print(toSemVer(input("Enter version: ")))
